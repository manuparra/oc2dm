import rpy2.robjects as ro

def svm(objectCore):
	svm = ro.r("""
        library("e1071")
	    dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = svm({1}, data=dataset)
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))