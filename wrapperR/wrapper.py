import csv
import pandas as pd
from rpy2.robjects.packages import importr
import rpy2.robjects as ro

class Core:

	datasetTFG = []
	inputTFG = {}
	outputTFG = {}
	def __init__(self):
		self.datasetTFG = []
		self.outputTFG = {}
		self.inputTFG = {}

	def readDataset(self,dataset):
	            df = pd.read_csv(dataset, header=None, sep=" ")
	            for i in range(0, df.shape[1]):
	                    self.datasetTFG.append(list(df[i]))

	def lm(self):
		lmfunction = LM()
		lmfunction.lm(self.datasetTFG)

class LM:
	def lm(self,dataset):
		stats = importr('stats')
		ctl = ro.FloatVector(dataset[0])
		trt = ro.FloatVector(dataset[1])
		ro.globalenv['ctl'] = ctl
		ro.globalenv['trt'] = trt
		ro.r('''
			f <- function() {

                library("r2pmml")
				group <- gl(2, 10, 20, labels = c("Ctl","Trt"))
				weight <- c(ctl, trt)
				lmprueba <- lm(weight ~ group - 1)
				
				r2pmml(lmprueba, "ets.pmml")
		}
		''')
		lms = ro.r['f']
		lms()

core = Core()
core.readDataset('dataset.csv')
core.lm()