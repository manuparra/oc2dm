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
    return 'http://192.168.10.56/'

def instance_id(instance_ip):
    payload = {'node_ip' : '{}'.format(instance_ip)}
    response = requests.post("http://10.10.0.7:5000/v1/nodes/get_instance_id", headers = headers, data = json.dumps(payload))
    return json.loads(response.text)

def initial_data(method, dataset):
    payload = {"job_id" : str(uuid.uuid4()), "status" : "RUNNING", "log_file" : "log_file", "time_start" : "", "time_finish" : "", "execution" : method, "dataset" : dataset}
    response = requests.post("http://10.10.0.7:5000/v1/nodes/jobs/insert_job", headers = headers, data = json.dumps(payload))

def start_job(method, dataset):
   ip = get_ip()
   i_id = instance_id(ip)
   initial_data(method, dataset)
