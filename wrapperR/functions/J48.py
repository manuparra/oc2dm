import rpy2.robjects as ro

def J48(parameterCore):
	j48 = ro.r("""
        library("RWeka")
	    dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = J48({1}, data=dataset)
	    saveRDS(resultfit, "{2}")
    """.format(parameterCore.dataset['ruta'], parameterCore.parameters, parameterCore.outputPMML))