import rpy2.robjects as ro

def cor (objectCore):
	cor = ro.r("""
		dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = cor({1})
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))