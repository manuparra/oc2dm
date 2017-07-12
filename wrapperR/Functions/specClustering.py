import rpy2.robjects as ro

def specClustering(parameterCore):
	specc = ro.r("""
        library("kernlab")
        dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = specc({1})
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))