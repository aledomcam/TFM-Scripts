import re

"""
Dada una salida de una consulta de Neo4J que contiene una serie de líneas, genera un archivo reformateado que las convierte al formato IATA1-IATA2, todas en una línea.
"""
def main():
	líneasConvertidas = []
	with open('export.csv', 'r', encoding = "utf-8") as fEntrada:
		primera = True
		for línea in fEntrada:
			if primera:
				# Cabecera
				primera = False
			else:
				match = re.match("\"\[(\w+),(\w+)\]\"" , línea)
				if match:
					iataAeropuerto1 = match.group(1)
					iataAeropuerto2 = match.group(2)
					líneasConvertidas.append(iataAeropuerto1 + "-" + iataAeropuerto2)
				else:
					raise RuntimeError("La línea \" " + línea + " \" no tiene el formato correcto")

	# Escribir resultado en un nuevo fichero
	primera = True
	with open('Líneas convertidas.txt', 'w', encoding = "utf-8") as fSalida:
		for strLínea in líneasConvertidas:
			if primera:
				primera = False
			else:
				fSalida.write(",")
			fSalida.write(strLínea)


if __name__ == "__main__":
	main()