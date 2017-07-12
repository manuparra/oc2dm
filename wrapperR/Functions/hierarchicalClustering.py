import rpy2.robjects as ro

def hClustering(parameterCore):
	hClustering = ro.r("""
        library("fastcluster")
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = hclust(dist({1}))
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))