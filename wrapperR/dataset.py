import os.path
import csv
import pandas as pd
import re
import numpy as np

class Dataset():
	def __init__(self, dictionary):
		self.dictionary = dictionary

		self.dataset = {}
		self.delimiter = {}
		self.parameters = {}
		self.splitDatasetParameters(dictionary)

		self.outputPMML = self.setOutput()
		self.columnParameterDataset = ""
		self.checkAll()		

	'''
		Comprueba que la ruta especificada del dataset exista
	'''
	def checkDatasetExists(self):
		if not os.path.isfile(self.dataset['ruta']):
			raise Exception("El fichero pasado no existe en la ruta")

	'''
		Comprueba que se tenga permisos de lectura
	'''
	def checkReadPermission(self):
		if not os.access(self.dataset['ruta'], os.R_OK) :
			raise Exception("No tenemos permisos de lectura")

	'''
		Comprobamos si tiene header el dataset
	'''
	def checkHeader(self):
		dataset = self.readDataset()
		for a in dataset.columns:
			if(not self.instring(a)):
				raise Exception("No tenemos header")

	'''
		Expresion regular que comprueba si los header leidos son string(el valor válido) o un numero entero o float(en cual caso no habria header)
	'''
	def instring (self, headerValue):
		if re.match ('^\d+$', headerValue) or re.match ('^\d+\.\d+$', headerValue):
			return False			
		else:
			return True

	'''
		Lee el dataset 
	'''
	def readDataset(self):
		return pd.read_csv(self.dataset['ruta'], delimiter = ',')

	'''
		Chequea todas las funciones
	'''
	def checkAll(self):
		try:
			self.checkDatasetExists()
			self.checkReadPermission()
			self.checkHeader()
			self.getParametersDataset()
			self.lmFunction()
			self.returnParsedParameters()
		except Exception:
			raise Exception("Fallo en el checkeo global")

	'''
		Parsea los parametros que tengan __ por . y construye los parametros con clave=valor
	'''
	def returnParsedParameters(self):
		d = ''
		for key, value in self.parameters.items():
			if value != 'NULL':
				d += key.replace("__", ".") + ' = ' + value + ','

		self.parameters = d[:-1]

	'''
		Desgrana el campo formula para que los nombres de las columnas puedan ser leidas en formato array
	'''
	def getParametersDataset(self):
		dataset = self.readDataset()
		formula = self.parameters['formula'].rsplit('~', 1)
		self.columnParameterDataset = formula


	'''
		Comprueba los campos que necesita la función en cuestion (Regresión Lineal) con los parametros pasados, 
		además comprobamos si estos parametros pueden o no pueden ser nulos y si son opcionales u obligatorios.
	'''
	def lmFunction(self):
		#Campos de la funcion LM
		campos = [
			('formula', 'obligatory', 'not null'),
			('subset', 'obligatory', 'null'),
			('weights', 'obligatory', 'null'),
			('na__action', 'obligatory', 'not null')
		]
		#lectura del dataset
		dataset = self.readDataset()

		for campo in campos:	
			#Si es obligatorio comprobamos los campos tanto en el dataset(formula), como en los parametros de entrada
			if campo[1] == 'obligatory':
				#Compruebo los campos de la funcion con los parametros pasados al servicio web
				if campo[0] not in self.parameters.keys():
					raise Exception ("No existe ese campo en los parametros pasados " , campo[0])

				#Si el campo es formula comprobamos que los campos internos de formula esten en el dataset pasado
				elif campo[0] == 'formula':
					algo = [False for a in self.columnParameterDataset if a not in dataset.columns]
					if False in algo:
						raise Exception ("No existen esas columnas")
			#Cuando es opcional comprobamos solo los parametros de entrada con los campos
			elif campo[1] == 'opcional':
				if campo[0] not in self.parameters.keys():
					raise Exception ("No existe ese campo en los parametros pasados " , campo[0])


			#Comprueba si los parametros pasados pueden ser null o no. En caso de no poderlo ser lanza una excepción
			if campo[2] == 'not null':
				if not self.parameters[campo[0]] or self.parameters[campo[0]] == 'NULL':
					raise Exception ("No puede ser el parametro " + campo[0] + " null ")

		if len(self.parameters) > len(campos):
			raise Exception ("Se enviaron mas parámetros de los que corresponden")

	'''
		ALmacena el nombre del dataset sin la extension y añadiendole la extension pmml donde se guardara el modelo 
	'''
	def setOutput(self):
		return os.path.splitext(self.dataset['ruta'])[0] + '.pmml'

	'''
		Devuelve el nombre del fichero de salida PMML
	'''
	def getOutput(self):
		return self.outputPMML

	'''
		Divide el diccionario enviado en dos partes: 
			- Dataset con la ruta y el delimitador 
			- Parametros de entrada
		Asigna cada uno de estos en el correspondiente atributo
	'''
	def splitDatasetParameters(self, dictionary):
		dataset = {}
		parameters = {}

		if 'dataset' in self.dictionary.keys():
			dataset['ruta'] = self.dictionary['dataset']
			del self.dictionary['dataset']
			if 'delimiter' in self.dictionary.keys():
				dataset['delimiter'] = self.dictionary['delimiter']
				del self.dictionary['delimiter']
			else:
				dataset['delimiter'] = ''
		else:
			raise Exception ("No existe un dataset " , campo[0])
		parameters = self.dictionary
		self.dataset = dataset
		self.parameters = parameters
		self.delimiter = dataset['delimiter']


#parametros = {'na__action': 'na.exclude', 'weights': 'NULL', 'formula': 'mpg~disp', 'subset': 'NULL', 'dataset': 'mtcars.csv', 'delimiter': ','}
#parametros = {'Dataset': {'ruta': 'mtcars.csv', 'separator': ','}, 'Parametros': {"formula": 'mpgd~disp', 'weights': 'NULL'}}
#parametros = {'Dataset': {'ruta': 'mtcars.csv', 'delimiter': ','}, 'Parametros': {'na__action': 'na.exclude', 'formula': 'mpg~disp', 'subset': 'NULL', 'weights': 'NULL'}}
#parametros = {'na__action':'na.omit', 'dataset': 'mtcars.csv', 'formula': 'mpg~disp', 'weights': 'NULL', 'subset': 'NULL'}
#dataset = Dataset(parametros)

#print(dataset.checkParametersDataset())