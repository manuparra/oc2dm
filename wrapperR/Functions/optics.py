import rpy2.robjects as ro

def optics(objectCore):
	optics = ro.r("""
        library("dbscan")
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = optics({1})
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))