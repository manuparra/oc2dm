from rpy2.robjects.packages import importr
import pandas as pd

import rpy2.robjects as ro

class Parameters():

	def __init__(self, dictionary):
		"""All information about the service are stored in the following:
        - ``self.input``: contains the input parameter parser
        - ``self.dataset``: contains the route of the dataset
        - ``self.outputRoute``: contains input
        - ``self.formula``: contains the formula to use"""
		self.input = self.__parser(dictionary)
		self.dataset = dictionary['dataset']
		self.outputRoute = self.__datasetParser(dictionary['dataset'])
		self.formula = dictionary['formula']


	def __parser (self, input_parameters):
		"""Parser for the input parameters. The function returns a string with the builded parameters.
		Besides the function checks for null values or a dataset key to not include it"""
		string = ''
		for key, value in input_parameters.items():
			if(value != 'NULL' and key != 'dataset'):
				string += key.replace("__", ".") + ' = ' + value + ', '
				#Exclude the last comma
		return string[:-2] 

	def __datasetParser (self, dataset):
		"""Return a route for the dataset. If the dataset has not route, the function returns a empty string what means the same route of the
		dataset but if the function has a route, then get the route where it is the dataset"""
		split = dataset.rsplit('/', 1)
		if len(split) > 1:
			return split[0]
		else:
			return ''

	def __readDataset(self):
		"""Read the dataset with pandas"""
		self.dataset = pd.read_csv(self.dataset,header=None, sep=" ")

	def getDataset(self):
		"""Return the dataset"""
		self.__readDataset()
		return self.dataset