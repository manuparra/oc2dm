import rpy2.robjects as ro

def kmeans(parameterCore):
    kmean = ro.r("""
		dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = kmeans({1})
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))