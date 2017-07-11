import collections
import json
import os
import sys
from os import listdir

import ruamel.yaml

from config.config import turtle_folder
from core.sparql_parser import sparql_parser

class YamlGenerator:
    def __init__(self, input_path, output_path):
        """
        Creates the catalog file in the specified directory using the definitions stored in the input path.
        
        :param input_path: a path containing all the services definitions
        :param output_path: the path where the catalog will be stored
        """
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
        order = "sed -i '1d' "
        order_paths = "{}/catalog.yml".format(output_path)
        os.system(order + order_paths)
        os.remove(output_path + "/raw_catalog.yml")
        os.remove(output_path + "/catalog_a.yml")

    def generate_yaml(self):
        """
        Builds the YAML catalog using the given data
        :return: the catalog in YAML format
        """
        paths = {}
        for file in self.services_list:
            parameters = self.generate_input(file)
            description = self.generate_base(file)
            end_point = file[:-4]
            method = {}
            method["get"] = {"operationId": "api." + end_point + ".execute", "parameters": parameters, "type": "string",
                             "summary": description, 'response': {200: {
                    'description': 'Output of the service contains Model or ModelEvaluation or Data'}}}
            method["post"] = {"operationId": "api." + end_point + ".execute_post", "parameters": parameters,
                              "type": "string",
                              "summary": description, 'response': {200: {
                    'description': 'Output of the service contains Model or ModelEvaluation or Data'}}}
            paths["'/" + end_point + "'"] = method
            # -> Download end-point
            method = {}
            method["get"] = {"operationId": "api." + end_point + ".download", 'produces': ['application/binary'],
                             "parameters": [
                                 {'in': 'query', 'name': 'file_format', 'description': 'asdasd', 'required': 'true',
                                  'default': 'ttl',
                                  'type': 'string'}], "type": "string",
                             "summary": 'Returns the service definition in the specified format.', 'response': {200: {
                    'description': 'Output of the service contains Model or ModelEvaluation or Data'}}}
            method["post"] = {"operationId": "api." + end_point + ".download_post", 'produces': ['application/binary'],
                              "parameters": [
                                  {'in': 'query', 'name': 'file_format', 'description': 'asdasd', 'required': 'true',
                                   'default': 'ttl',
                                   'type': 'string'}],
                              "type": "string",
                              "summary": 'Returns the service definition in the specified format.', 'response': {200: {
                    'description': 'The Turtle file.'}}}
            paths["'/" + end_point + "/download'"] = method
            # <- Download end-point
        method = {}
        method["get"] = {"operationId": "api.catalog.execute", "type": "string", 'produces': ['application/json'],
                         "summary": 'Returns the complete catalog', 'response': {200: {
                'description': 'JSON containing the catalog.'}}}

        paths["'/catalog'"] = method
        self.final_yaml = collections.OrderedDict([('swagger', '2.0'),
                                                   ('info', None),
                                                   ('title', 'OPENCCML API'),
                                                   ('version', '0.1'),
                                                   ('consumes', ['application/json']),
                                                   ('produces', ['text/xml']),
                                                   ('basePath', "'/openccml'"),
                                                   ('paths', paths)])

    def generate_base(self, input_file):
        """
        Extract the "base" from the definition file and convert it to an usable dictionary
        :param input_file: the service definition file name
        :return: basic data and description of the given service
        """
        parser = sparql_parser.SPARQL_driver(input_file)
        base = json.loads(parser.base.decode("utf-8"))
        description = base['results']['bindings']
        return description[0]['mldescription']['value']

    def generate_input(self, input_file):
        """
        Extract the "input" from the definition file and convert it to an usable dictionary
        :param input_file: the service definition file name
        :return: input parameters of the given service
        """
        parser = sparql_parser.SPARQL_driver(input_file)
        input_parameters = json.loads(parser.inputparameters.decode("utf-8"))
        input = json.loads(parser.input.decode("utf-8"))
        base = json.loads(parser.base.decode("utf-8"))
        parameters = []
        for parameter in input_parameters['results']['bindings']:
            name = parameter["mlinputtitle"]["value"]
            description = parameter["mlinputdescription"]["value"]
            required = parameter["mlinputmandatory"]["value"]
            if 'optional' in required:
                required = False
            else:
                required = True
            default = parameter["mlinputdefault"]["value"]
            parameters.append(
                {'in': 'query', 'name': name, 'description': description, 'required': required, 'default': default,
                 'type': 'string'})
        for parameter in input['results']['bindings']:
            name = parameter['mldatasettitle']['value'].lower()
            description = parameter['mldatasetdescr']['value']
            required = parameter["mlmandatory"]["value"]
            if 'optional' in required:
                required = False
            else:
                required = True
            parameters.append(
                {'in': 'query', 'name': name, 'description': description, 'required': required, 'default': default,
                 'type': 'string'})
        return parameters


def main():
    YamlGenerator("../services_definition/turtle", "../catalog")


if __name__ == '__main__':
    sys.path.append('~/openccml')
    from core.sparql_parser import sparql_parser

    main()
