import sys
import random

"""
Dado un fichero que contenga una lista de líneas separadas por comas, genera otro que solo contenga un cierto porcentaje de las mismas al azar.
El porcentaje se especifica como argumento del programa (0-1)
"""
def main():
	if (len(sys.argv) != 2):
		raise ValueError("Error: Debe especificarse un único argumento que indique el porcentaje de líneas a mantener (0-1)")
	porcentaje = float(sys.argv[1])
	if porcentaje < 0 or porcentaje > 1:
		raise ValueError("Error: El porcentaje de líneas a mantener debe estar entre 0 y 1")
	
	with open('Líneas.txt', 'r', encoding = "utf-8") as fEntrada:
		líneas = fEntrada.read()
		líneas = líneas.replace(", ", ",")
		listaLíneas = líneas.split(",")
		numLíneasABorrar = round(len(listaLíneas) * (1 - porcentaje))
		while numLíneasABorrar > 0 and len(listaLíneas) > 0:
			pos = random.randrange(len(listaLíneas))
			listaLíneas.pop(pos)
			numLíneasABorrar -= 1
	
	# Escribir resultado en un nuevo fichero
	with open('Líneas aleatorias.txt', 'w', encoding = "utf-8") as fSalida:
		líneas = ",".join(listaLíneas)
		fSalida.write(líneas)


if __name__ == "__main__":
	main()