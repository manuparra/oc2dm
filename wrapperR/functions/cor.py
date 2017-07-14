import rpy2.robjects as ro

def cor (parameterCore):
	cor = ro.r("""
		dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = cor({1})
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))