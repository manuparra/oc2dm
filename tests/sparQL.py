import unittest

from sparql_parser.sparql_parser import SPARQL_driver

class TestSparQLLibrary(unittest.TestCase):

    def test_readallservices(self):
        sqld=SPARQL_driver(turtle_file="linear_regression.ttl",test=True)
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()