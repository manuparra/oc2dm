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
from Functions.cor import *
from Functions.dbscan import *
from Functions.hierarchicalClustering import *
from Functions.J48 import *
from Functions.kmeans import *
from Functions.lm import *
from Functions.logisticRegression import *
from Functions.naiveBayes import *
from Functions.optics import *
from Functions.rf import *
from Functions.specClustering import *
from Functions.superVectorMachine import *

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
		j48(self.parameter)

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

parametros = {'x': 'dc://mtcars$mpg', 'y': 'dc://mtcars$disp', 'method': 'spearman'}

#parametros = {'na__action':'na.omit', 'dataset': 'mtcars.csv', 'formula': 'mpg~disp', 'weights': 'NULL', 'subset': 'NULL'}
#dataset.cor()
#entrada = {'na__action':'na.omit', 'dataset': '/home/ruben/Escritorio/openccml/datasets/mtcars.csv', 'formula': 'mpg~disp+cyl/hp', 'weights': 'NULL', 'subset': 'NULL'}
#entrada = {'dataset': 'dc://mtcars', 'na__action':'na.exclude','formula': 'mpg~disp', 'subset': 'NULL', 'weights': 'NULL'}
#parametros = {'x': '/home/ruben/Escritorio/openccml/datasets/mtcars$mpg', 'y': '/home/ruben/Escritorio/openccml/datasets/mtcars$disp', 'method': 'spearman'}
#parametros = {'x': '/home/ruben/Escritorio/openccml/datasets/mtcars', 'centers': '3'}
#parametros = {'formula': 'species~.', 'dataset': '/home/ruben/Escritorio/openccml/datasets/iris.csv'}
p = core(parametros, "cor")

#dbscan(p)
#p.lm()
#specClustering()
#hClustering(p)
#naiveBayes(p)