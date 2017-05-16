from falsy.falsy import FALSY

f = FALSY(static_dir='/core/static')
f.swagger('catalog/catalog.yml', ui=True, theme='impress')
api = f.api
