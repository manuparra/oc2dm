import rpy2.robjects as ro

def naiveBayes(parameterCore):
	naiveBayes = ro.r("""
		library("naivebayes")
	    dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = naive_bayes({1}, data=dataset)
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))
