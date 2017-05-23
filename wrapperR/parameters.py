from rpy2.robjects.packages import importr
import pandas as pd

import rpy2.robjects as ro

class Parameters():

	def __init__(self, dictionary):
		self.input = self.__parser(dictionary)
		self.dataset = dictionary['dataset']
		self.outputRoute = self.__datasetParser(dictionary['dataset'])
		self.formula = dictionary['formula']


	def __parser (self, input_parameters):
		string = ''
		for key, value in input_parameters.items():
			if(value != 'NULL' and key != 'dataset'):
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