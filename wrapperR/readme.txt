Para la incoporación de un nuevo metodo al wrapper debemos de incoporar lo siguiente:

	- Fichero .py en la carpeta Functions con el metodo en cuestion, pasandole la ruta del dataset, los parametros y la salida a guardar el modelo (generando un Rdata o un pmml).
	- En dataset.py definimos ahora los siguientes campos. La primera funcion a crear es la que define los parametros obligatorios y opcionales que tiene ese método, para el chequeo de parametros en el dataset y demás acciones que se realizan. Añadimos una entrada con la salida que va a devolver, ya sea .pmml o .Rdata. Por último añadimos otra entrada en el chequeo de parametros recibidos como dataset, header, columnas, etc. Normalmente se dispone de dos tipos de construccion de este chequeo vease el ejemplo montado de cor y de lm.
		