import rpy2.robjects as ro

def lm (objectCore):
	lm = ro.r("""
		library("r2pmml")
		dataset = read.csv(file="{0}", header = TRUE, sep=',')
	    resultfit = lm({1}, data=dataset)
	    r2pmml(resultfit,file="{2}")
    """.format(objectCore.parameter.dataset['ruta'], objectCore.parameter.parameters, objectCore.parameter.outputPMML))