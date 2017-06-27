from sys import path

from falsy.falsy import FALSY

from config.config import turtle_folder, catalog_folder, sparql_parser_folder, wrapperR_folder,api_servername
from core.yaml_generator import YamlGenerator

# Add SparQL and WrapperR path 
path.append(sparql_parser_folder)
path.append(wrapperR_folder)

# Generate ML Catalog from Servides definition.
yml = YamlGenerator(turtle_folder, catalog_folder)

# Start OpenCCML Service
f = FALSY(static_dir='/core/static')
f.swagger('catalog/catalog.yml', ui=True, theme='impress',api_url=api_servername)
api = f.api
