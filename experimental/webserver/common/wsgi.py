# Copyright 2017 DiCTIS UGR
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


"""
Utility methods for working with WSGI servers
"""


from __future__ import print_function

import errno
import functools
import os
import signal
import sys
import time

import eventlet
from eventlet.green import socket
from eventlet.green import ssl
import eventlet.greenio
import eventlet.wsgi

import routes
import routes.middleware
import six
import webob.dec
import webob.exc
from webob import multidict


from omlcc_catalog.common import config
from omlcc_catalog.common import exception



wsgi_opts = [
    cfg.StrOpt('secure_proxy_ssl_header',
               deprecated_for_removal=True,
               deprecated_reason=_('Use the http_proxy_to_wsgi middleware '
                                   'instead.'),
               help=_('The HTTP header used to determine the scheme for the '
                      'original request, even if it was removed by an SSL '
                      'terminating proxy. Typical value is '
                      '"HTTP_X_FORWARDED_PROTO".')),
]

LOG = logging.getLogger(__name__)

CONF = cfg.CONF
CONF.register_opts(bind_opts)
CONF.register_opts(socket_opts)
CONF.register_opts(eventlet_opts)
CONF.register_opts(wsgi_opts)


def set_eventlet_hub():
    try:
        eventlet.hubs.use_hub('poll')
    except Exception:
        try:
            eventlet.hubs.use_hub('selects')
        except Exception:
            msg = _("eventlet 'poll' nor 'selects' hubs are available "
                    "on this platform")
            raise exception.WorkerCreationFailure(
                reason=msg)


class Server(object):
    """Server class to manage multiple WSGI sockets and applications.
    This class requires initialize_glance_store set to True if
    glance store needs to be initialized.
    """
    def __init__(self, threads=1000, initialize_glance_store=False):
        os.umask(0o27)  # ensure files are created with the correct privileges
        self._logger = logging.getLogger("eventlet.wsgi.server")
        self.threads = threads
        self.children = set()
        self.stale_children = set()
        self.running = True
        # NOTE(abhishek): Allows us to only re-initialize glance_store when
        # the API's configuration reloads.
        self.initialize_glance_store = initialize_glance_store
        self.pgid = os.getpid()
        try:
            # NOTE(flaper87): Make sure this process
            # runs in its own process group.
            os.setpgid(self.pgid, self.pgid)
        except OSError:
            # NOTE(flaper87): When running glance-control,
            # (glance's functional tests, for example)
            # setpgid fails with EPERM as glance-control
            # creates a fresh session, of which the newly
            # launched service becomes the leader (session
            # leaders may not change process groups)
            #
            # Running glance-(api|registry) is safe and
            # shouldn't raise any error here.
            self.pgid = 0

    def hup(self, *args):
        """
        Reloads configuration files with zero down time
        """
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        raise exception.SIGHUPInterrupt

    def kill_children(self, *args):
        """Kills the entire process group."""
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.running = False
        os.killpg(self.pgid, signal.SIGTERM)

    def start(self, application, default_port):
        """
        Run a WSGI server with the given application.
        :param application: The application to be run in the WSGI server
        :param default_port: Port to bind to if none is specified in conf
        """
        self.application = application
        self.default_port = default_port
        self.configure()
        self.start_wsgi()

    def start_wsgi(self):
        workers = get_num_workers()
        if workers == 0:
            # Useful for profiling, test, debug etc.
            self.pool = self.create_pool()
            self.pool.spawn_n(self._single_run, self.application, self.sock)
            return
        else:
            LOG.info(_LI("Starting %d workers"), workers)
            signal.signal(signal.SIGTERM, self.kill_children)
            signal.signal(signal.SIGINT, self.kill_children)
            signal.signal(signal.SIGHUP, self.hup)
            while len(self.children) < workers:
                self.run_child()

    def create_pool(self):
        return get_asynchronous_eventlet_pool(size=self.threads)

    def _remove_children(self, pid):
        if pid in self.children:
            self.children.remove(pid)
            LOG.info(_LI('Removed dead child %s'), pid)
        elif pid in self.stale_children:
            self.stale_children.remove(pid)
            LOG.info(_LI('Removed stale child %s'), pid)
        else:
            LOG.warn(_LW('Unrecognised child %s') % pid)

    def _verify_and_respawn_children(self, pid, status):
        if len(self.stale_children) == 0:
            LOG.debug('No stale children')
        if os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
            LOG.error(_LE('Not respawning child %d, cannot '
                          'recover from termination') % pid)
            if not self.children and not self.stale_children:
                LOG.info(
                    _LI('All workers have terminated. Exiting'))
                self.running = False
        else:
            if len(self.children) < get_num_workers():
                self.run_child()

    def wait_on_children(self):
        while self.running:
            try:
                pid, status = os.wait()
                if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                    self._remove_children(pid)
                    self._verify_and_respawn_children(pid, status)
            except OSError as err:
                if err.errno not in (errno.EINTR, errno.ECHILD):
                    raise
            except KeyboardInterrupt:
                LOG.info(_LI('Caught keyboard interrupt. Exiting.'))
                break
            except exception.SIGHUPInterrupt:
                self.reload()
                continue
        eventlet.greenio.shutdown_safe(self.sock)
        self.sock.close()
        LOG.debug('Exited')

    def configure(self, old_conf=None, has_changed=None):
        """
        Apply configuration settings
        :param old_conf: Cached old configuration settings (if any)
        :param has changed: callable to determine if a parameter has changed
        """
        eventlet.wsgi.MAX_HEADER_LINE = CONF.max_header_line
        self.client_socket_timeout = CONF.client_socket_timeout or None
        self.configure_socket(old_conf, has_changed)
        if self.initialize_glance_store:
            initialize_glance_store()

    def reload(self):
        """
        Reload and re-apply configuration settings
        Existing child processes are sent a SIGHUP signal
        and will exit after completing existing requests.
        New child processes, which will have the updated
        configuration, are spawned. This allows preventing
        interruption to the service.
        """
        def _has_changed(old, new, param):
            old = old.get(param)
            new = getattr(new, param)
            return (new != old)

        old_conf = utils.stash_conf_values()
        has_changed = functools.partial(_has_changed, old_conf, CONF)
        CONF.reload_config_files()
        os.killpg(self.pgid, signal.SIGHUP)
        self.stale_children = self.children
        self.children = set()

        # Ensure any logging config changes are picked up
        logging.setup(CONF, 'glance')
        config.set_config_defaults()

        self.configure(old_conf, has_changed)
        self.start_wsgi()

    def wait(self):
        """Wait until all servers have completed running."""
        try:
            if self.children:
                self.wait_on_children()
            else:
                self.pool.waitall()
        except KeyboardInterrupt:
            pass

    def run_child(self):
        def child_hup(*args):
            """Shuts down child processes, existing requests are handled."""
            signal.signal(signal.SIGHUP, signal.SIG_IGN)
            eventlet.wsgi.is_accepting = False
            self.sock.close()

        pid = os.fork()
        if pid == 0:
            signal.signal(signal.SIGHUP, child_hup)
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            # ignore the interrupt signal to avoid a race whereby
            # a child worker receives the signal before the parent
            # and is respawned unnecessarily as a result
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            # The child has no need to stash the unwrapped
            # socket, and the reference prevents a clean
            # exit on sighup
            self._sock = None
            self.run_server()
            LOG.info(_LI('Child %d exiting normally'), os.getpid())
            # self.pool.waitall() is now called in wsgi's server so
            # it's safe to exit here
            sys.exit(0)
        else:
            LOG.info(_LI('Started child %s'), pid)
            self.children.add(pid)

    def run_server(self):
        """Run a WSGI server."""
        if cfg.CONF.pydev_worker_debug_host:
            utils.setup_remote_pydev_debug(cfg.CONF.pydev_worker_debug_host,
                                           cfg.CONF.pydev_worker_debug_port)

        eventlet.wsgi.HttpProtocol.default_request_version = "HTTP/1.0"
        self.pool = self.create_pool()
        try:
            eventlet.wsgi.server(self.sock,
                                 self.application,
                                 log=self._logger,
                                 custom_pool=self.pool,
                                 debug=False,
                                 keepalive=CONF.http_keepalive,
                                 socket_timeout=self.client_socket_timeout)
        except socket.error as err:
            if err[0] != errno.EINVAL:
                raise

        # waiting on async pools
        if ASYNC_EVENTLET_THREAD_POOL_LIST:
            for pool in ASYNC_EVENTLET_THREAD_POOL_LIST:
                pool.waitall()

    def _single_run(self, application, sock):
        """Start a WSGI server in a new green thread."""
        LOG.info(_LI("Starting single process server"))
        eventlet.wsgi.server(sock, application, custom_pool=self.pool,
                             log=self._logger,
                             debug=False,
                             keepalive=CONF.http_keepalive,
                             socket_timeout=self.client_socket_timeout)

    def configure_socket(self, old_conf=None, has_changed=None):
        """
        Ensure a socket exists and is appropriately configured.
        This function is called on start up, and can also be
        called in the event of a configuration reload.
        When called for the first time a new socket is created.
        If reloading and either bind_host or bind port have been
        changed the existing socket must be closed and a new
        socket opened (laws of physics).
        In all other cases (bind_host/bind_port have not changed)
        the existing socket is reused.
        :param old_conf: Cached old configuration settings (if any)
        :param has changed: callable to determine if a parameter has changed
        """
        # Do we need a fresh socket?
        new_sock = (old_conf is None or (
                    has_changed('bind_host') or
                    has_changed('bind_port')))
        # Will we be using https?
        use_ssl = not (not CONF.cert_file or not CONF.key_file)
        # Were we using https before?
        old_use_ssl = (old_conf is not None and not (
                       not old_conf.get('key_file') or
                       not old_conf.get('cert_file')))
        # Do we now need to perform an SSL wrap on the socket?
        wrap_sock = use_ssl is True and (old_use_ssl is False or new_sock)
        # Do we now need to perform an SSL unwrap on the socket?
        unwrap_sock = use_ssl is False and old_use_ssl is True

        if new_sock:
            self._sock = None
            if old_conf is not None:
                self.sock.close()
            _sock = get_socket(self.default_port)
            _sock.setsockopt(socket.SOL_SOCKET,
                             socket.SO_REUSEADDR, 1)
            # sockets can hang around forever without keepalive
            _sock.setsockopt(socket.SOL_SOCKET,
                             socket.SO_KEEPALIVE, 1)
            self._sock = _sock

        if wrap_sock:
            self.sock = ssl_wrap_socket(self._sock)

        if unwrap_sock:
            self.sock = self._sock

        if new_sock and not use_ssl:
            self.sock = self._sock

        # Pick up newly deployed certs
        if old_conf is not None and use_ssl is True and old_use_ssl is True:
            if has_changed('cert_file') or has_changed('key_file'):
                utils.validate_key_cert(CONF.key_file, CONF.cert_file)
            if has_changed('cert_file'):
                self.sock.certfile = CONF.cert_file
            if has_changed('key_file'):
                self.sock.keyfile = CONF.key_file

        if new_sock or (old_conf is not None and has_changed('tcp_keepidle')):
            # This option isn't available in the OS X version of eventlet
            if hasattr(socket, 'TCP_KEEPIDLE'):
                self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE,
                                     CONF.tcp_keepidle)

        if old_conf is not None and has_changed('backlog'):
            self.sock.listen(CONF.backlog)
