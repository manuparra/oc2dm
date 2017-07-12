import rpy2.robjects as ro

def kmeans(objectCore):
    kmean = ro.r("""
		dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = kmeans({1})
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))