from config.config import turtle_folder, jsonld_folder
from wrapperR import wrapperv2


def execute(x, y, method, use):
    print(locals())
    result = wrapperv2.core(locals(), "cor")
    result.cor()
    file = result.parameter.getOutput()
    print(file)
    with open(file, 'rb') as pmml:
        return pmml


def execute_post(x, y, method, use):
    result = wrapperv2.core(locals(), "cor")
    result.cor()


def download(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/correlation.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/cor.jsonld") as file:
            return file.read()


def download_post(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/correlation.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/cor.jsonld") as file:
            return file.read()
