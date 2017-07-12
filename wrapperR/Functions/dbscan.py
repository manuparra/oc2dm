import rpy2.robjects as ro

def dbscan(objectCore):
    dbscan = ro.r("""
        library("dbscan")
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = dbscan({1})
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))