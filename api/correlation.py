from wrapperR import wrapperv2
from config.config import turtle_folder, jsonld_folder


def execute(x, y, method):
    locals()['dataset'] = '/home/jacortes/PycharmProjects/openccml/wrapperR/mtcars.csv'
    result = wrapperv2.core(locals(), "cor")
    result.cor()
    """
    file = result.parameter.getOutput()
    with open(file) as pmml:
        return pmml.read()
    """
def execute_post(use):
    data = "no data here"
    return {'data': data}


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
