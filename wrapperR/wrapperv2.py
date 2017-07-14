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
from functions.cor import *
from functions.dbscan import *
from functions.hierarchicalClustering import *
from functions.J48 import *
from functions.kmeans import *
from functions.lm import *
from functions.logisticRegression import *
from functions.naiveBayes import *
from functions.optics import *
from functions.rf import *
from functions.specClustering import *
from functions.superVectorMachine import *

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
#corParametros = {'x': 'dc://mtcars$mpg', 'y': 'dc://mtcars$disp', 'method': 'spearman', 'use': 'everything'}
#j48Parametros = {'formula': 'species~petal_width', 'data': '/home/ruben/Escritorio/openccml/datasets/iris.csv', 'na__action': 'na.exclude'}
#kmeansParametros = {'x': 'dc://mtcars', 'centers': '3', 'iter__max': '3000'}
#dbscanParametros = {'x': 'dc://mtcars', 'eps':' 8', 'minPts': '30'}
#opticsParametros = {'x': 'dc://mtcars', 'eps':' 8', 'minPts': '30'}
#specClusteringParametros = {'x': 'dc://mtcars', 'centers': '3'}
#hClustParametros = {'x': 'dc://mtcars'}
#lRegressionParametros = {'formula': 'species~petal_width', 'dataset': 'dc://iris'}
#svmParametros = {'formula': 'species~petal_width', 'dataset': 'dc://iris'}
#naiveBayesParametros = {'formula': 'species~petal_width', 'dataset': 'dc://iris'}

#p = core(naiveBayesParametros, "naiveBayes")
#p.naiveBayes()