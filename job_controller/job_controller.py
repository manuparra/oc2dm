# Obtain node IP - Done
# Obtain associated instance_id - Done
# Insert job starting data (generate job_id)
# Wait for the job to finish
# Add job finishing data
# Add node-job entry
import socket
import requests
import json
import uuid

headers = {'Content-type' : 'application/json'}

def get_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return '10.10.0.16'

def instance_id(instance_ip):
    payload = {'node_ip' : '{}'.format(instance_ip)}
    response = requests.post("http://10.10.0.7:5000/v1/nodes/get_instance_id", headers = headers, data = json.dumps(payload))
    return json.loads(response.text)

def initial_data(method, dataset):
    job_id = str(uuid.uuid4())
    payload = {"job_id" : job_id,  "status" : "RUNNING", "log_file" : "log_file", "time_start" : "", "time_finish" : "", "execution" : method, "dataset" : dataset}
    response = requests.post("http://10.10.0.7:5000/v1/nodes/jobs/insert_job", headers = headers, data = json.dumps(payload))
    print(response.content)
    return job_id

def start_job(method, dataset):
   ip = get_ip()
   i_id = instance_id(ip)
   job_id = initial_data(method, dataset)
   return job_id

def finish_job(job_id):
    payload = {'job_id': job_id, 'status':'FINISHED', 'time_finish': ""}
    response = requests.post("http://10.10.0.7:5000/v1/nodes/jobs/update_job", headers = headers, data = json.dumps(payload))

def error_job(job_id):
    payload = {'job_id': job_id, 'status':'ERROR', 'time_finish': ""}
    response = requests.post("http://10.10.0.7:5000/v1/nodes/jobs/update_job", headers = headers, data = json.dumps(payload))

def node_job(job_id):
    i_id = instance_id(get_ip())
    payload = {'job_id': job_id, 'instance_id': i_id}
    response = requests.post("http://10.10.0.7:5000/v1/nodes/jobs/insert_nodejobs", headers = headers, data = json.dumps(payload))
