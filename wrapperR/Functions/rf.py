import rpy2.robjects as ro

def rf (objectCore):	
	rf = ro.r("""
		library("randomForest")
		library("r2pmml")
		dataset = read.csv(file="{0}", header = TRUE, sep=',')
		fit = randomForest({1}, data=dataset)
		r2pmml(fit,file="{2}")
		""".format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))