import rpy2.robjects as ro

def specClustering(objectCore):
	specc = ro.r("""
        library("kernlab")
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = specc({1})
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))