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

from wrapperR.dataset import *
from wrapperR.functions.cor import *
from wrapperR.functions.dbscan import *
from wrapperR.functions.hierarchicalClustering import *
from wrapperR.functions.J48 import *
from wrapperR.functions.kmeans import *
from wrapperR.functions.lm import *
from wrapperR.functions.logisticRegression import *
from wrapperR.functions.naiveBayes import *
from wrapperR.functions.optics import *
from wrapperR.functions.rf import *
from wrapperR.functions.specClustering import *
from wrapperR.functions.superVectorMachine import *

class core:

	def __init__(self, dictionary, method):
		self.parameter = Dataset(dictionary, method)
	
	def lm(self):
		lm(self.parameter)

	def cor(self):
		cor(self.parameter)

	def dbscan(self):
		dbscan(self.parameter)

	def hierarchicalClustering(self):
		hierarchicalClustering(self.parameter)

	def j48(self):
		#print(self.parameter.parameters)
		J48(self.parameter)

	def kmeans(self):
		kmeans(self.parameter)

	def logisticRegression(self):
		logisticRegression(self.parameter)

	def naiveBayes(self):
		naiveBayes(self.parameter)

	def optics(self):
		optics(self.parameter)

	def rf(self):
		rf(self.parameter)

	def specClustering(self):
		specClustering(self.parameter)

	def superVectorMachine(self):
		svm(self.parameter)
#rfParametros = {'formula': 'species~petal_width', 'na__action':'na.pass', 'dataset': 'dc://iris', 'subset':'NULL', 'ntree':'3'}
#corParametros = {'x': 'dc://mtcars$mpg', 'y': 'dc://mtcars$disp', 'method': 'spearman', 'use': 'everything'}
#j48Parametros = {'formula': 'species~petal_width', 'data': '/home/ruben/Escritorio/openccml/datasets/iris.csv', 'na__action': 'na.exclude'}
#kmeansParametros = {'x': 'dc://mtcars', 'centers': '3', 'iter__max': '3000'}
#dbscanParametros = {'x': 'dc://mtcars', 'eps':' 8', 'minPts': '30'}
#opticsParametros = {'x': 'dc://mtcars', 'eps':' 8', 'minPts': '30'}
#specClusteringParametros = {'x': 'dc://mtcars', 'centers': '3', 'na__action':'na.omit'}
#hClustParametros = {'x': 'dc://mtcars', 'method':'NULL'}
#lRegressionParametros = {'formula': 'species~petal_width', 'dataset': 'dc://iris'}
#svmParametros = {'formula': 'species~petal_width', 'dataset': 'dc://iris', 'na__action':'na.omit'}
#naiveBayesParametros = {'formula': 'species~petal_width', 'na__action':'na.pass', 'dataset': 'dc://iris'}

#p = core(rfParametros, "rf")
#p.rf()