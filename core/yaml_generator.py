import collections
import json
import os
from os import listdir

import ruamel.yaml

from sparql_parser import sparql_parser


class YamlGenerator:
    def __init__(self, input_path, output_path):
        ruamel.yaml.representer.RoundTripRepresenter.add_representer(collections.OrderedDict,
                                                                     ruamel.yaml.representer.RoundTripRepresenter.represent_ordereddict)
        self.services_list = listdir(input_path)
        self.final_yaml = None
        self.generate_yaml()

        out_file = open(output_path + "/raw_catalog.yml", 'w')
        ruamel.yaml.dump(self.final_yaml, out_file, Dumper=ruamel.yaml.RoundTripDumper)
        order = "sed 's/^.\{,2\}//' "
        order_paths = "{}/raw_catalog.yml > {}/catalog_a.yml".format(output_path, output_path)
        os.system(order + order_paths)
        order = """ sed 's/\"//g' """
        order_paths = "{}/catalog_a.yml > {}/catalog.yml".format(output_path, output_path)
        os.system(order + order_paths)
        os.remove(output_path + "/raw_catalog.yml")
        os.remove(output_path + "/catalog_a.yml")

    def generate_yaml(self):
        paths = {}
        for file in self.services_list:
            parameters = self.generate_input(file)
            end_point = file[:-4]
            method = {}
            method["get"] = {"operationId": "api." + end_point + ".execute", "parameters": parameters, "type": "string",
                             "summary": 'Execute a linear regression over the provided dataset', 'response': {200: {
                    'description': 'Output of the service contains Model or ModelEvaluation or Data'}}}
            paths["'/" + end_point + "'"] = method
        method = {}
        method["get"] = {"operationId": "api.catalog.execute", "type": "string",
                         "summary": 'Returns the complete catalog', 'response': {200: {
                'description': 'JSON containing the catalog.'}}}
        paths["'/catalog'"] = method
        self.final_yaml = collections.OrderedDict([('swagger', '2.0'),
                                                   ('info', None),
                                                   ('title', 'OPENCCML API'),
                                                   ('version', '0.1'),
                                                   ('consumes', ['application/json']),
                                                   ('produces', ['application/json']),
                                                   ('basePath', "'/openccml'"),
                                                   ('paths', paths)])

    def generate_input(self, input_file):
        parser = sparql_parser.SPARQL_driver(input_file)
        parser._extract_inputparameters()
        data = json.loads(parser.inputparameters.decode("utf-8"))
        parameters = []
        for parameter in data['results']['bindings']:
            name = parameter["mlinputtitle"]["value"]
            description = parameter["mlinputdescription"]["value"]
            required = parameter["mlinputmandatory"]["value"]
            default = parameter["mlinputdefault"]["value"]
            parameters.append(
                {'in': 'query', 'name': name, 'description': description, 'required': required, 'default': default,
                 'type': 'string'})
        return parameters


YamlGenerator("../services_definition/turtle", "../catalog")
