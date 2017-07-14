import rpy2.robjects as ro

def logisticRegression(parameterCore):
	lRegression = ro.r("""
        library("RWeka")
	    dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = Logistic({1}, data=dataset)
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))
