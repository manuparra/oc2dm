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

from dataset import *
from functionsR import *

class core:

	def __init__(self, dictionary, method):
		self.parameter = Dataset(dictionary, method)
	
	
'''parametros = {'x': 'dataset$mpg', 'y': 'dataset$disp', 'method': 'spearman', 'dataset': 'mtcars.csv'}
dataset = core(parametros, "cor")
cor(dataset)'''

#parametros = {'na__action':'na.omit', 'dataset': 'mtcars.csv', 'formula': 'mpg~disp', 'weights': 'NULL', 'subset': 'NULL'}
#dataset.cor()
#entrada = {'na__action':'na.omit', 'dataset': 'mtcars.csv', 'formula': 'mpg~disp', 'weights': 'NULL', 'subset': 'NULL'}
#p = core(entrada)
#p.lm()	
