import rpy2.robjects as ro

def optics(parameterCore):
	optics = ro.r("""
        library("dbscan")
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = optics({1})
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))