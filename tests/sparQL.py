import unittest
import json

from sparql_parser.sparql_parser import SPARQL_driver

class TestSparQLLibrary(unittest.TestCase):

    def test_base_service_vars(self):
        sqld=SPARQL_driver(turtle_file="linear_regression.ttl",test=True)
        sqld._extract_base()
        # Convert to Dict
        dictjson=json.loads(sqld.base)
        self.assertTrue(len(dictjson['head']['vars'])>0 and len(dictjson['results']['bindings'])>0)

    def test_base_service_binding(self):
        sqld=SPARQL_driver(turtle_file="linear_regression.ttl",test=True)
        sqld._extract_base()
        # Convert to Dict
        dictjson=json.loads(sqld.base)
        self.assertTrue(len(dictjson['results']['bindings'])>0)




if __name__ == '__main__':
    unittest.main()