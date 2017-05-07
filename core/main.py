from falsy.falsy import FALSY

f = FALSY()
f.swagger('../catalog/linear_regression.yml', ui=True, theme='impress')
api = f.api