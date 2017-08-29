"""
Configuration file
"""
from os import path

# API ServerName, is used when OpenCCML is used behind a firewall or proxy (nginx)
#  Use None if usng openccml in localhost
api_servername="http://docker.ugr.es:8203"

# Project Base Folder. Application code home
project_base_folder = path.join('/home', 'tfg_user', 'openccml')

# Folder with the Services Definition in Turtle format
turtle_folder = path.join(project_base_folder, 'services_definition', 'turtle')

# Folder with the Services Definition in JSON-LD format
jsonld_folder = path.join(project_base_folder, 'services_definition', 'jsonLD')

# SparQL folder
sparql_parser_folder = path.join(project_base_folder, 'sparql_parser')

# Main and CORE Folder of OpenCCML
core_folder = path.join(project_base_folder, 'core')

# Folder containing Machine Learning Services Definition
catalog_folder = path.join(project_base_folder, 'catalog')

# Folder of the Wrappers: R
wrapperR_folder = path.join(project_base_folder, 'wrapperR')

# Dicits Storage Objects
dc_storage = path.join(project_base_folder, 'datasets')

# R functions
functions_folder = path.join(wrapperR_folder, 'Functions')

# Job controller folder
job_controller_folder = path.join(project_base_folder, 'job_controller')
