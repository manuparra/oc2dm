import rpy2.robjects as ro

def J48(objectCore):
	j48 = ro.r("""
        library("RWeka")
	    dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = J48({1}, data=dataset)
	    saveRDS(resultfit, "{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))