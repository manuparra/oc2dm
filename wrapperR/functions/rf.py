import rpy2.robjects as ro

def rf (parameterCore):	
	rf = ro.r("""
		library("randomForest")
		library("r2pmml")
		dataset = read.csv(file="{0}", header = TRUE, sep=',')
		fit = randomForest({1}, data=dataset)
		r2pmml(fit,file="{2}")
		""".format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))