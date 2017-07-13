import os.path
import csv
import pandas as pd
import re
import numpy as np
import sys
sys.path.append('../')
from config.config import dc_storage

class Dataset():
	def __init__(self, dictionary, method):
		self.dictionary = dictionary
		self.method = method
		self.dataset = {}
		self.delimiter = {}
		self.parameters = {}

		self.outputPMML = ""
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
			if self.method == "lm":
				self.splitDatasetParameters('dataset')

				self.checkDatasetExists()
				self.checkReadPermission()
				self.checkHeader()
				
				self.getParametersDataset('formula')
				self.LMFunction()
				self.returnParsedParameters()

			if self.method == "cor":
				cols = ['x', 'y']
				for col in cols:
					self.splitDatasetParameters(None)
					self.splitDatasetColumn(col, '$')
					self.checkDatasetExists()
					self.checkReadPermission()
					self.checkHeader()
				self.corFunction()
				self.returnParsedParameters()

			if self.method == "arima":
				self.getParametersDataset('formula')
				self.arimaFunction()
				self.returnParsedParameters()
			if self.method == "rf":
				self.splitDatasetParameters('data')
				self.checkDatasetExists()
				self.checkReadPermission()
				self.checkHeader()

				self.getParametersDataset('formula')
				self.rfFunction()
				self.returnParsedParameters()
			if self.method == "kmeans":
				cols = ['x']
				for col in cols:
					self.splitDatasetParameters(None)
					self.splitDatasetColumn(col, None)
					self.checkDatasetExists()
					self.checkReadPermission()
					self.checkHeader()
				self.kmeansFunction()
				self.returnParsedParameters()
			if self.method == "dbscan":
				cols = ['x']
				for col in cols:
					self.splitDatasetParameters(None)
					self.splitDatasetColumn(col, None)
					self.checkDatasetExists()
					self.checkReadPermission()
					self.checkHeader()
				self.dbscanFunction()
				self.returnParsedParameters()

			if self.method == "optics":
				cols = ['x']
				for col in cols:
					self.splitDatasetParameters(None)
					self.splitDatasetColumn(col, None)
					self.checkDatasetExists()
					self.checkReadPermission()
					self.checkHeader()
				self.opticsFunction()
				self.returnParsedParameters()
			if self.method == "specClust":
				cols = ['x']
				for col in cols:
					self.splitDatasetParameters(None)
					self.splitDatasetColumn(col, None)
					self.checkDatasetExists()
					self.checkReadPermission()
					self.checkHeader()
				self.specClustFunction()
				self.returnParsedParameters()

			if self.method == "hclust":
				cols = ['x']
				for col in cols:
					self.splitDatasetParameters(None)
					self.splitDatasetColumn(col, None)
					self.checkDatasetExists()
					self.checkReadPermission()
					self.checkHeader()
				self.hclustFunction()
				self.returnParsedParameters()

			if self.method == "j48":
				self.splitDatasetParameters('data')
				self.checkDatasetExists()
				self.checkReadPermission()
				self.checkHeader()

				self.getParametersDataset('formula')
				self.j48Function()
				self.returnParsedParameters()

			if self.method == "lRegression":
				self.splitDatasetParameters('dataset')
				self.checkDatasetExists()
				self.checkReadPermission()
				self.checkHeader()

				self.getParametersDataset('formula')
				self.j48Function()
				self.returnParsedParameters()

			if self.method == "svm":
				self.splitDatasetParameters('dataset')
				self.checkDatasetExists()
				self.checkReadPermission()
				self.checkHeader()

				self.getParametersDataset('formula')
				self.svmFunction()
				self.returnParsedParameters()

			if self.method == "naiveBayes":
				self.splitDatasetParameters('dataset')
				self.checkDatasetExists()
				self.checkReadPermission()
				self.checkHeader()

				self.getParametersDataset('formula')
				self.svmFunction()
				self.returnParsedParameters()

			self.outputPMML = self.setOutput()

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
	def getParametersDataset(self, field):
		dataset = self.readDataset()
		formula = re.split('-|/|~|\+', self.parameters[field])
		return formula


	'''
		Comprueba los campos que necesita la función en cuestion (Regresión Lineal) con los parametros pasados, 
		además comprobamos si estos parametros pueden o no pueden ser nulos y si son opcionales u obligatorios.
	'''
	def generalFunction(self, campos):
		#Campos de la funcion LM
		
		#lectura del dataset
		dataset = self.readDataset()
		
		firstColCampos = []
		for campo in campos:
			firstColCampos.append(campo[0])
			#Si es obligatorio comprobamos los campos tanto en el dataset(formula), como en los parametros de entrada
			if campo[1] == 'obligatory':
				#Compruebo los campos de la funcion con los parametros pasados al servicio web
				if campo[0] not in self.parameters.keys():
					raise Exception ("No existe ese campo en los parametros pasados " + campo[0])

				#Si el campo es formula comprobamos que los campos internos de formula esten en el dataset pasado
				elif campo[0] == 'formula':
					param = self.getParametersDataset('formula')
					algo = [False for a in param if a not in dataset.columns]
					if False in algo:
						raise Exception ("No existen esas columnas")
			#Cuando es opcional comprobamos solo los parametros de entrada con los campos
			#elif campo[1] == 'opcional':
			#	if campo[0] not in self.parameters.keys():
			#		raise Exception ("No existe ese campo en los parametros pasados " , campo[0])
			#Comprueba si los parametros pasados pueden ser null o no. En caso de no poderlo ser lanza una excepción
			if campo[2] == 'not null':
				if not self.parameters[campo[0]] or self.parameters[campo[0]] == 'NULL':
					raise Exception ("No puede ser el parametro " + campo[0] + " null ")
			#Entre comilla el campo indicado
			if campo[3] == 'quote':
				self.parameters[campo[0]] = '"' + self.parameters[campo[0]] + '"'


		al = set(list(self.parameters.keys())) == set(firstColCampos) & set(list(self.parameters.keys()))
		if not al:
			raise Exception ("Se enviaron unos parametros que no corresponden con lo que se requiere")
			
		if len(self.parameters) > len(campos):
			raise Exception ("Se enviaron mas parámetros de los que corresponden")

	'''
		Almacena el nombre del dataset sin la extension y añadiendole la extension pmml donde se guardara el modelo 
	'''
	def setOutput(self):
		if self.method == "lm":
			return os.path.splitext(self.dataset['ruta'])[0] + '.pmml'
		elif self.method == "cor":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "arima":
			return os.path.splitext(self.dataset['ruta'])[0] + '.pmml'
		elif self.method == "rf":
			return os.path.splitext(self.dataset['ruta'])[0] + '.pmml'
		elif self.method == "kmeans":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "dbscan":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "optics":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "specClust":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "hclust":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "j48":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "lRegression":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "svm":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'
		elif self.method == "naiveBayes":
			return os.path.splitext(self.dataset['ruta'])[0] + '.Rdata'

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
	def splitDatasetParameters(self, nameDataset):
		dataset = {}
		parameters = {}
		#Comprueba si el nombre de dataset no esta None y además esta en los parametros pasados
		if nameDataset and nameDataset in self.dictionary.keys():
			#Obtiene la ruta del dataset
			dataset['ruta'] = self.dictionary[nameDataset]
			#Borramos ese registro ya que de ahi saldran los parametros a pasarle al metodo y estos no suelen tener referencia alguna al dataset
			del self.dictionary[nameDataset]

			self.dataset = dataset
			#Traduce la ruta pasada por dc:// por la ruta absoluta leida del fichero config.py del main
			self.translateDC()
			#En caso de tener delimitador lo obtenemos tambien y lo separamos de los parametros
			if 'delimiter' in self.dictionary.keys():
				dataset['delimiter'] = self.dictionary['delimiter']
				del self.dictionary['delimiter']
			else:
				dataset['delimiter'] = ''
		#En caso de que no se tenga dataset, ya que en el paso de parametros no esté la ruta del dataset especificada que no haga nada, si está pero no se encuentra en los parametros pasados que lance excepcion
		else:
			if nameDataset:
				raise Exception ("No existe un dataset ")
		#Parametros sin el dataset
		parameters = self.dictionary
		#Almacenamiento del dataset y parametros
		self.dataset = dataset
		self.parameters = parameters
		
		#self.delimiter = dataset['delimiter']

	#Definición de campos de la regresíon lineal
	def LMFunction(self):
		campos = [
			('formula', 'obligatory', 'not null', 'unquote'),
			('subset', 'obligatory', 'null', 'unquote'),
			('weights', 'obligatory', 'null', 'unquote'),
			('na__action', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos de la correlación
	def corFunction(self):
		campos = [
			('x', 'obligatory', 'not null', 'unquote'),
			('y', 'obligatory', 'null', 'unquote'),
			('method', 'obligatory', 'not null', 'quote'),
			('use', 'obligatory', 'not null', 'quote'),
		]
		self.generalFunction(campos)

	#Definición de campos de arima
	def arimaFunction(self):
		campos = [
			('x', 'obligatory', 'not null', 'unquote'),
			('order', 'obligatory', 'null', 'unquote')			
		]
		self.generalFunction(campos)

	#Definición de campos del random forest
	def rfFunction(self):
		campos = [
			('formula', 'obligatory', 'not null', 'unquote'),
			('na__action', 'optional', 'null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del kmeans
	def kmeansFunction(self):
		campos = [
			('x', 'obligatory', 'not null', 'unquote'),
			('centers', 'obligatory', 'not null', 'unquote'),
			('iter__max', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del DBSCAN
	def dbscanFunction(self):
		campos = [
			('x', 'obligatory', 'not null', 'unquote'),
			('eps', 'obligatory', 'not null', 'unquote'),
			('minPts', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del OPTICS
	def opticsFunction(self):
		campos = [
			('x', 'obligatory', 'not null', 'unquote'),
			('eps', 'obligatory', 'not null', 'unquote'),
			('minPts', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del Spectral Clustering
	def specClustFunction(self):
		campos = [
			('x', 'obligatory', 'not null', 'unquote'),
			('centers', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del Hierarchical Clustering
	def hclustFunction(self):
		campos = [
			('x', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del J48
	def j48Function(self):
		campos = [
			('formula', 'obligatory', 'not null', 'unquote'),
			('na__action', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del Linear Regression
	def lRegressionFunction(self):
		campos = [
			('formula', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del Super Vector Machine
	def svmFunction(self):
		campos = [
			('formula', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	#Definición de campos del naiveBayes
	def naiveBayesFunction(self):
		campos = [
			('formula', 'obligatory', 'not null', 'unquote')
		]
		self.generalFunction(campos)

	'''
		Guarda la ruta y parsea la estructura con la que viene la ruta por la nueva ruta que va a ser leída por R.
		Por ejemplo: x = pruebaDataset.csv   quedaría por x = dataset siendo el nombre dataset usando en el wrapper
		ya que se lee el dataset y se almacena sobre una variable llamada dataset, esta debe de ser igual a la que 
		obtiene la variable de ejemplo x
	'''
	def splitDatasetColumn(self, col, delimiter):
		#Si tiene delimitador
		if delimiter != None:
			#Divide por el delimitador proporcionado en la funcion. Ej: /home/ruben/Escritorio/openccml/datasets/mtcars$mpg
			formula = self.parameters[col].split(delimiter)
			#Guarda la ruta con el formato de este que se presupone es csv
			self.dataset['ruta'] = formula[0] + '.csv'
			#Reemplazamos el dataset pasado por la estructura nueva de este. Ej: x = pruebaDataset.csv quedaría por x = dataset
			self.parameters[col] = self.parameters[col].replace(formula[0], 'dataset')
			#Traduce la ruta pasada por dc:// por la ruta absoluta leida del fichero config.py del main
			self.translateDC()
			#Leemos el dataset
			dataset = self.readDataset()
			#Comprueba que en el spliteo del dataset y la columna, esta columna esté como una columna del dataset
			if formula[1] not in dataset.columns:
				raise Exception ("La columna no existe nano")
		else:
			#Guarda la ruta con el formato de este que se presupone es csv
			self.dataset['ruta'] = self.parameters[col] + '.csv'
			#Reemplazamos el dataset pasado por la estructura nueva de este. Ej: x = pruebaDataset.csv quedaría por x = dataset
			self.parameters[col] = self.parameters[col].replace(self.parameters[col], 'dataset')
			#Traduce la ruta pasada por dc:// por la ruta absoluta leida del fichero config.py del main
			self.translateDC()

	def translateDC(self):
		#Obtenemos los 5 primeros caracteres de la ruta que son los que definiran si tiene dc://
		dicits = self.dataset['ruta'][:5]
		#Si coincide esa ruta en lo leido
		if 'dc://' in dicits:
			ext = self.dataset['ruta'][-4:]
			if not '.csv' in ext:
				self.dataset['ruta'] = self.dataset['ruta'] + '.csv'
			#Obtenemos de config la ruta absoluta de dc:// y le añadimos el resto de lo proporcionado
			self.dataset['ruta'] = dc_storage + '/'+ self.dataset['ruta'][5:]


#parametros = {'x': 'dataset$mpg', 'y': 'dataset$disp', 'method': 'spearman', 'dataset': 'mtcars.csv'}
#parametros = {'Dataset': {'ruta': 'mtcars.csv', 'separator': ','}, 'Parametros': {"formula": 'mpgd~disp', 'weights': 'NULL'}}
#parametros = {'Dataset': {'ruta': 'mtcars.csv', 'delimiter': ','}, 'Parametros': {'na__action': 'na.exclude', 'formula': 'mpg~disp', 'subset': 'NULL', 'weights': 'NULL'}}
#parametros = {'na__action':'na.omit', 'dataset': 'mtcars.csv', 'formula': 'mpg~disp', 'weights': 'NULL', 'subset': 'NULL'}
#dataset = Dataset(parametros)

#print(dataset.checkParametersDataset())
