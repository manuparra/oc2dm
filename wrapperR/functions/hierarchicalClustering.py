import rpy2.robjects as ro

def hierarchicalClustering(parameterCore):
	hClustering = ro.r("""
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = hclust(dist({1}))
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))