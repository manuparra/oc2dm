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
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.packages import importr


class DataSet:
	"""
	Read dataset with Pandas
	"""
	def __init__(self, dataset_path="dataset.csv",header=False,sep=","):
		self.dataset_path=dataset_path
		self.dataset=None
		self.header=header
		self.sep=sep

	def __readdataset(self):
		"""
		Reading the CSV data file
		"""
		self.dataset=pd.read_csv(self.dataset,header=self.header, sep=self.sep)
		
	def get(self):
		"""
		Return Dataset Pandas Object
		"""
		self.__readdataset()
		return self.dataset
		


class core:
	"""
	Package CORE of R. Includes methods from the CORE of R, and not included on additional Packages
	"""
	
	def __init__(self,dataset=None,input_params=None, output_params=None):
		self.dataset=dataset
		self.input=input_params
		self.output=output_params
	
	def lm (self):
		"""
		Linear Regression Method
		"""
		
		#TAKS:
		# Extract Columns from the dataset
		# The input must be a **kwargs  and extract input parameters for the model (weight ~ group)
		# Analize formulae 
		
		
		ro.globalenv["weight"] = self.dataset['weight'] # Or self.dataset[0] if header is not available
		ro.globalenv["group"] = self.dataset['group'] # self.dataset[1] if header is not available

		R=ro.r
		
		lmfit=R.lm("weight ~ group")
		R.r2pmml(lmfit,file=self.output_params)
		
		
		

	def corr(self,input):
		"""
		Correlation Method
		"""
		pass
		
		
class randomForest:
	"""
	Random Forest Package
	"""
	
	def __init__(self,dataset):
		self.dataset=dataset
		
	def randomForest(self):
		"""
		Main Method
		"""
		pass
		
		
input_params=...		
ouput_params=...
ds=DataSet(dataset_path='/tmp/dataset.csv',header=False,sep=" ")
execute=core(ds.get(),input_params, output_params)
execute.lm()

	