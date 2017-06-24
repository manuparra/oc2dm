import os.path
import csv
import pandas as pd
import re
import numpy as np

class Dataset():
	def __init__(self, dictionary):
		self.dataset = dictionary['Dataset']
		self.outputPMML = self.setOutput()
		self.delimiter = dictionary['Dataset']
		self.parameters = dictionary['Parametros']
		self.columnParameterDataset = ""
		self.checkAll()
		

	#Comprueba que la ruta especificada del dataset exista
	def checkDatasetExists(self):
		if not os.path.isfile(self.dataset['ruta']):
			raise Exception("El fichero pasado no existe en la ruta")

	#Comprueba que se tenga permisos de lectura
	def checkReadPermission(self):
		if not os.access(self.dataset['ruta'], os.R_OK) :
			raise Exception("No tenemos permisos de lectura")

	#Comprobamos si tiene header el dataset
	def checkHeader(self):
		dataset = self.readDataset()
		for a in dataset.columns:
			if(not self.instring(a)):
				raise Exception("No tenemos header")

	#Expresion regular que comprueba si los header leidos son string(el valor válido) o un numero entero o float(en cual caso no habria header)
	def instring (self, headerValue):
		if re.match ('^\d+$', headerValue) or re.match ('^\d+\.\d+$', headerValue):
			return False			
		else:
			return True

	def readDataset(self):
		return pd.read_csv(self.dataset['ruta'], delimiter=',')

	def checkAll(self):
		try:
			self.checkDatasetExists()
			self.checkReadPermission()
			self.checkHeader()
			self.getParametersDataset()
			self.lmFunction()
			self.returnParsedParameters()
		except Exception:
			raise


	def returnParsedParameters(self):
		d = ''
		for key, value in self.parameters.items():
			if value != 'NULL':
				d += key.replace("__", ".") + ' = ' + value + ','

		self.parameters = d[:-1]

	def getParametersDataset(self):
		dataset = self.readDataset()
		formula = self.parameters['formula'].rsplit('~', 1)
		self.columnParameterDataset = formula

	def lmFunction(self):
		campos = [
			("formula", 'obligatory')
			
		]
		dataset = self.readDataset()

		for campo in campos:	
			if campo[1] == 'obligatory':
				#Compruebo los campos con los parametros pasados
				if campo[0] not in self.parameters.keys():
					raise Exception ("No existe ese campo en los parametros pasados")
				elif campo[0] == 'formula':
					algo = [False for a in self.columnParameterDataset if a not in dataset.columns]
					if False in algo:
						raise Exception ("No existen esas columnas")
			elif campo[1] == 'opcional':
				if campo[0] not in self.parameters.keys():
					raise Exception ("No existe ese campo en los parametros pasados " , campo[0])

		#if len(self.parameters) != len(campos):
		#	raise Exception ("Distintos tamaños de arrays enviados")

	def setOutput(self):
		return os.path.splitext(self.dataset['ruta'])[0] + '.pmml'

	def getOutput(self):
		return self.outputPMML

#parametros = {'Dataset': {'ruta': 'mtcars.csv', 'separator': ','}, 'Parametros': {"formula": 'mpgd~disp', 'weights': 'NULL'}}
#parametros = {'Dataset': {'ruta': 'mtcars.csv', 'delimiter': ','}, 'Parametros': {'na__action': 'na.exclude', 'formula': 'mpg~disp', 'subset': 'NULL', 'weights': 'NULL'}}
#parametros = {'na__action':'na.omit', 'dataset': 'mtcars.csv', 'formula': 'mpg~disp', 'weights': 'NULL', 'subset': 'NULL'}
#dataset = Dataset(parametros)

#print(dataset.checkParametersDataset())