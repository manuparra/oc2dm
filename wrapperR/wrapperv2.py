# Copyright 2017 DiCITS UGR
# Author: Manuel Parra, Ruben Castro
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""RWrapper"""

import csv
import rpy2.robjects as ro
from parameters import *
from rpy2.robjects.packages import importr


class core(Parameters):

	"""
	Package CORE of R. Includes methods from the CORE of R, and not included on additional Packages
	"""
	

	def __init__(self, dictionary):
		self.parameter = Parameters(dictionary)
		print(self.parameter.input)
	
	def lm (self):
		"""
		Linear Regression Method
		"""
		#TAKS:
		# Extract Columns from the dataset
		# The input must be a **kwargs  and extract input parameters for the model (weight ~ group)
		# Analize formulae 
		values = self.parameter.getDataset()
		ro.globalenv["weight"] = ro.FloatVector(values[0]) # Or self.dataset[0] if header is not available
		ro.globalenv["group"] = ro.FloatVector(values[1]) # self.dataset[1] if header is not available

		R=ro.r
		R.library("r2pmml")

		lmfit=R.lm("weight ~ group")
		file = self.parameter.outputRoute + 'model.pmml'
		R.r2pmml(lmfit,file=file)

formula = "mpg~disp"
entrada = {'na__action': 'na.remove', 'dataset': 'dataset.csv', 'formula': 'a~b', 'weights': 'NULL', 'subset': 'NULL'}
p = core(entrada)
p.lm()	
