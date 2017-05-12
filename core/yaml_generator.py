import collections

import ruamel.yaml

from experimental.queringjsonld import queryexample


class YamlGenerator:
    ruamel.yaml.representer.RoundTripRepresenter.add_representer(collections.OrderedDict,
                                                                 ruamel.yaml.representer.RoundTripRepresenter.represent_ordereddict)

    def __init__(self, input_file, output_file):
        qres_base, qres_inputparams = queryexample.turtle_query(input_file)
        parameters = []

        for row in qres_inputparams:
            name = row[0][:]
            description = row[1][:]
            if row[2] == 'optional':
                required = False
            else:
                required = True
            default = row[3][:]
            parameters.append(
                {'in': 'query', 'name': name, 'description': description, 'required': required, 'default': default})
        data = collections.OrderedDict([('swagger', '2.0'),
                                        ('title', 'OPENCCML API'),
                                        ('version', '0.1'),
                                        ('consumes', ['application/json']),
                                        ('produces', ['application/json']),
                                        ('paths',
                                         {'/linear_regression': {'get': {'operationId': 'linear_regression.execute',
                                                                         'parameters': parameters,
                                                                         'type': 'array',
                                                                         'summary': 'Execute a linear regression over the provided dataset',
                                                                         'tags': ['Method']}}})])
        out_file = open('base.yml', 'w')
        ruamel.yaml.dump(data, out_file, default_flow_style=False, Dumper=ruamel.yaml.RoundTripDumper, indent=2)


YamlGenerator("cor.ttl", "asd")
