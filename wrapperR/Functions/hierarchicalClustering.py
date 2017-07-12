import rpy2.robjects as ro

def hClustering(objectCore):
	hClustering = ro.r("""
        library("fastcluster")
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = hclust(dist({1}))
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))