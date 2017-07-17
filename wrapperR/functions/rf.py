import rpy2.robjects as ro

def rf (parameterCore):
	rf = ro.r("""
		library("randomForest")
		dataset = read.csv(file="{0}", header = TRUE, sep=',')
		fit = randomForest({1}, data=dataset)
		saveRDS(fit, "{2}")
		""".format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))