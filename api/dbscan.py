from wrapperR import wrapperv2
from config.config import turtle_folder, jsonld_folder


def execute(x, minpts, eps):
    print(locals())
    result = wrapperv2.core(locals(), "dbscan")
    result.dbscan()
    file = result.parameter.getOutput()


def execute_post(x, minpts, eps):
    result = wrapperv2.core(locals(), "dbscan")
    result.dbscan()
    file = result.parameter.getOutput()


def download(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/dbscan.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/dbscan.jsonld") as file:
            return file.read()


def download_post(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/dbscan.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/dbscan.jsonld") as file:
            return file.read()
