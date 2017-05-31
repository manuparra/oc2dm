from sys import path

from falsy.falsy import FALSY

from config.config import turtle_folder, catalog_folder, sparql_parser_folder
from core.yaml_generator import YamlGenerator

path.append(sparql_parser_folder)
yml = YamlGenerator(turtle_folder, catalog_folder)
f = FALSY(static_dir='/core/static')
f.swagger('catalog/catalog.yml', ui=True, theme='impress')
api = f.api
