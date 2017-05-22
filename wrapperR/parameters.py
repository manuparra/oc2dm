from rpy2.robjects.packages import importr
import pandas as pd

import rpy2.robjects as ro

class Parameters():

	def __init__(self, dataset, formula, input_parameter):
		self.input = self.__parser(input_parameter)
		self.dataset = dataset
		self.outputRoute = self.__datasetParser(dataset)
		self.formula = formula


	def __parser (self, input_parameters):
		string = ''
		for key, value in input_parameters.items():
			if(value != 'NULL'):
				string += key.replace("__", ".") + ' = ' + value + ', '
		return string[:-2] 

	def __datasetParser (self, dataset):
		split = dataset.rsplit('/', 1)
		if len(split) > 1:
			return split[0]
		else:
			return ''

	def __readDataset(self):
		self.dataset = pd.read_csv(self.dataset,header=None, sep=" ")

	def getDataset(self):
		self.__readDataset()
		return self.dataset