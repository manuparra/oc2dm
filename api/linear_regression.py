from config.config import turtle_folder, jsonld_folder
from wrapperR import wrapperv2
from job_controller.job_controller import start_job, finish_job, error_job, node_job

def execute(subset, weights, na__action, dataset, formula):
    data = locals()
    job_id = start_job("linear_regression", dataset)
    node_job(job_id)
    try:
     result = wrapperv2.core(data, "lm")
     result.lm()
    except Exception as e:
        error_job(job_id)
        return {'Error: ': e}
    finish_job(job_id)
    file = result.parameter.getOutput()
    with open(file) as pmml:
        return pmml.read()

def execute_post(subset, weights, na__action, dataset, formula):
    data = locals()
    job_id = start_job("linear_regression", dataset)
    node_job(job_id)
    try:
     result = wrapperv2.core(data, "lm")
     result.lm()
    except Exception as e:
        error_job(job_id)
        return {'Error: ': e}
    finish_job(job_id)
    file = result.parameter.getOutput()
    with open(file) as pmml:
        return pmml.read()


def download(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/linear_regression.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/lr.jsonld") as file:
            return file.read()


def download_post(file_format):
    if 'turtle' in file_format:
        with open(turtle_folder + "/linear_regression.ttl") as file:
            return file.read()
    else:
        with open(jsonld_folder + "/lr.jsonld") as file:
            return file.read()
