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
from dataset import *
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import pandas as pd


class core:

	"""
	Package CORE of R. Includes methods from the CORE of R, and not included on additional Packages
	"""
	

	def __init__(self, dictionary, method):
		self.parameter = Dataset(dictionary, method)
	
	def lm (self):
		lm = ro.r("""
			library("r2pmml")
			dataset = read.csv(file="{0}", header = TRUE, sep=',')
	        resultfit = lm({1}, data=dataset)
	        r2pmml(resultfit,file="{2}")
     	""".format(self.parameter.dataset['ruta'], self.parameter.parameters, self.parameter.outputPMML))

	def cor (self):
		cor = ro.r("""
			library("r2pmml")
			dataset = read.csv(file="{0}", header = TRUE, sep=',')
	        resultfit = cor({1})
	        saveRDS(resultfit, "{2}")
	        print(resultfit)
     	""".format(self.parameter.dataset['ruta'], self.parameter.parameters, self.parameter.outputPMML))

	def arima(self):
		pass

parametros = {'x': 'dataset$mpg', 'y': 'dataset$disp', 'method': 'spearman', 'dataset': 'mtcars.csv'}

#parametros = {'na__action':'na.omit', 'dataset': 'mtcars.csv', 'formula': 'mpg~disp', 'weights': 'NULL', 'subset': 'NULL'}
dataset = core(parametros, "cor")
dataset.cor()
#entrada = {'na__action':'na.omit', 'dataset': 'mtcars.csv', 'formula': 'mpg~disp', 'weights': 'NULL', 'subset': 'NULL'}
#p = core(entrada)
#p.lm()	
