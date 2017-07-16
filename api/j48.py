from config.config import turtle_folder, jsonld_folder
from wrapperR import wrapperv2


def execute(na__action, data, formula):
    print(locals())
    result = wrapperv2.core(locals(), "j48")
    result.j48()
    file = result.parameter.getOutput()


def execute_post(na__action, data, formula):
    result = wrapperv2.core(locals(), "j48")
    result.j48()
    file = result.parameter.getOutput()


def download(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/j48.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/j48.jsonld") as file:
            return file.read()


def download_post(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/j48.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/j48.jsonld") as file:
            return file.read()
