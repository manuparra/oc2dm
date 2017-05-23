from wrapperR import wrapperv2
def execute(subset, weights, na__action, dataset, formula):
    result = wrapperv2.core(locals())
    file = result.lm()
    with open(file) as pmml:
        return pmml.read()
