from config.config import turtle_folder, jsonld_folder
from wrapperR import wrapperv2


def execute(x, method):
    print(locals())
    result = wrapperv2.core(locals(), "hclust")
    result.hierarchicalClustering()
    file = result.parameter.getOutput()
    with open(file) as pmml:
        return pmml.read()


def execute_post(x, centers, iter__max):
    print(locals())
    result = wrapperv2.core(locals(), "hclust")
    result.hierarchicalClustering()
    file = result.parameter.getOutput()
    with open(file) as pmml:
        return pmml.read()


def download(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/hierarchical_clustering.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/km.jsonld") as file:
            return file.read()


def download_post(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/hierarchical_clustering.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/km.jsonld") as file:
            return file.read()
