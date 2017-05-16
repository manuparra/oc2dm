import collections
import json
import os
from os import listdir
from pprint import pprint

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
        order_paths = "{}/raw_catalog.yml > {}/catalog.yml".format(output_path, output_path)
        os.system(order + order_paths)

    def generate_yaml(self):
        paths = {}
        for file in self.services_list:
            parameters = self.generate_input(file)
            end_point = file[:-4]
            method = {}
            method["get"] = {"operationID": "api." + end_point + ".execute", "parameters": parameters, "type": "array",
                             "summary": 'Execute a linear regression over the provided dataset'}
            paths["/" + end_point] = method
        self.final_yaml = collections.OrderedDict([('swagger', '2.0'),
                                                   ('title', 'OPENCCML API'),
                                                   ('version', '0.1'),
                                                   ('consumes', ['application/json']),
                                                   ('produces', ['application/json']),
                                                   ('paths', paths)])
        pprint(self.final_yaml)

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
                {'in': 'query', 'name': name, 'description': description, 'required': required, 'default': default})
        return parameters


YamlGenerator("../services_definition/turtle", "../catalog")
