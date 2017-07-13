from wrapperR import wrapperv2
from config.config import turtle_folder, jsonld_folder


def execute(x, centers, iter__max):
    print(locals())
    result = wrapperv2.core(locals(), "kmeans")
    result.kmeans()


def execute_post(x, centers, iter__max):
    result = wrapperv2.core(locals(), "kmeans")
    result.kmeans()


def download(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/kmeansclustering.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/km.jsonld") as file:
            return file.read()


def download_post(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/kmeansclustering.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/km.jsonld") as file:
            return file.read()
