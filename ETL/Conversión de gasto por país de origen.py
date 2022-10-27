import csv

# -- Constantes referidas a valores en el fichero de entrada --
# Las líneas que tengan este valor como país de origen se tratarán como datos para el resto de países
VALOR_OTROS = "Resto del Mundo"
# Las líneas que tengan este valor como país de origen se considerarán datos totales
VALOR_TOTAL = "Total"

# -- Constantes usadas para generar el fichero de salida --
# Código del país al que pertenecen los datos
CÓDIGO_PAÍS = "ESP"

# -- Otras constantes --
# Diccionario usado para convertir nombres de países tal y como aparecen en el csv de entrada en valores válidos para la BD
# La relación puede ser uno a muchos, así que el segundo elemento es una lista de códigos de países
EQUIVALENCIAS_PAÍSES = {
	"Reino Unido": ["GBR"],
	"Países Nórdicos": ["DNK", "FIN", "ISL", "NOR", "SWE"],
	"Alemania": ["DEU"],
	"Francia": ["FRA"],
	"Italia": ["ITA"]
}


def main():
	with open('GastoTuristasINE.csv', newline = '') as entrada:
		with open('GastoTuristas.csv', 'w', newline = '') as salida:
			reader = csv.reader(entrada, delimiter = ';')
			writer = csv.writer(salida, delimiter = ',')
			
			for fila in reader:
				país = fila[0]
				fecha_separada = fila[1].split('M')
				año = int(fecha_separada[0])
				mes = int(fecha_separada[1])
				gasto = int(fila[2])
			
				if país == VALOR_TOTAL:
					# Ignorar
					pass
				elif país == VALOR_OTROS:
					writer.writerow(["", CÓDIGO_PAÍS, año, mes, gasto])
				else:
					try:
						for val in EQUIVALENCIAS_PAÍSES[país]:
							writer.writerow([val, CÓDIGO_PAÍS, año, mes, gasto])
					except KeyError as key_error:
						raise KeyError("El país \"" + país + "\" no tiene especificado un nombre de salida") from key_error


if __name__ == "__main__":
	main()