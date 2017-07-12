import rpy2.robjects as ro

def naiveBayes(objectCore):
	naiveBayes = ro.r("""
		library("naivebayes")
	    dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = naive_bayes({1}, data=dataset)
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))
