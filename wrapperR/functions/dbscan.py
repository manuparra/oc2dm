import rpy2.robjects as ro

def dbscan(parameterCore):
    dbscan = ro.r("""
        library("dbscan")
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = dbscan({1})
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))