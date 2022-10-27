import csv

# -- Constantes referidas a valores en el fichero de entrada --
# Las líneas que tengan este valor como provincia se tratarán como datos a nivel nacional
VALOR_NACIONAL = "Total nacional"
# Nombre que tienen los datos referidos al número de visitantes por motivos turísticos
STRING_MOTIVO_TURISMO = "Ocio, recreo y vacaciones"
# Nombre que tienen los datos referidos al número de visitantes totales
STRING_MOTIVO_TOTAL = "Total de motivos del viaje"

# -- Constantes usadas para generar el fichero de salida --
# Código del país al que pertenecen los datos
CÓDIGO_PAÍS = "ESP"

# -- Otras constantes --
# Diccionario usado para convertir nombres de regiones tal y como aparecen en el csv de entrada en valores válidos para la BD
EQUIVALENCIAS_REGIÓN = {
	"01 Andalucía": "Andalusia, Spain",
	"02 Aragón": "Aragon, Spain",
	"03 Asturias, Principado de": "Asturias, Spain",
	"04 Balears, Illes": "Baleares, Spain",
	"05 Canarias": "Canarias, Spain",
	"06 Cantabria": "Cantabria, Spain",
	"07 Castilla y León": "Castilla y Leon, Spain",
	"08 Castilla - La Mancha": "Castilla - La Mancha, Spain",
	"09 Cataluña": "Catalonia, Spain",
	"10 Comunitat Valenciana": "C. Valenciana, Spain",
	"11 Extremadura": "Extremadura, Spain",
	"12 Galicia": "Galicia, Spain",
	"13 Madrid, Comunidad de": "Madrid, Spain",
	"14 Murcia, Región de": "Murcia, Spain",
	"15 Navarra, Comunidad Foral de": "Navarra, Spain",
	"16 País Vasco": "Pais Vasco, Spain",
	"17 Rioja, La": "La Rioja, Spain"
}

def main():
	with open('VisitantesINE.csv', newline = '') as entrada:
		with open('Visitantes.csv', 'w', newline = '') as salida:
			reader = csv.reader(entrada, delimiter = ';')
			writer = csv.writer(salida, delimiter = ',')
			región_actual = None
			
			for fila in reader:
				if fila[0] != región_actual:
					# Hemos cambiado de región, terminamos de procesar la anterior (si la hay) y reiniciamos las variables que corresponda
					if región_actual != None:
						# Convertir las dos listas en una sola con los datos ya formateados
						datos_combinados = combinar_datos_visitantes(datos_turistas, datos_total_visitantes, región_actual)
						
						# Insertar una fila en el csv de salida por cada valor en los datos combinados
						for dato_combinado in datos_combinados:
							writer.writerow([CÓDIGO_PAÍS, convertir_región(región_actual), \
								dato_combinado["año"], dato_combinado["mes"], dato_combinado["porcentaje"]])
						
					región_actual = fila[0]
					# Estas dos listas contienen los datos de visitantes por motivos turísticos y totales para la región actual.
					# Cada elemento es a su vez un diccionario que contiene la fecha y el valor.
					# Los dos sub-elementos son strings sacadas tal cual del csv de entrada.
					datos_turistas = []
					datos_total_visitantes = []
					
				# Comprobamos qué tipo de dato estamos leyendo
				if fila[1] == STRING_MOTIVO_TURISMO:
					datos_turistas.append({"fecha": fila[2], "valor": fila[3]})
				elif fila[1] == STRING_MOTIVO_TOTAL:
					datos_total_visitantes.append({"fecha": fila[2], "valor": fila[3]})


# Combina dos listas que contienen datos de visitantes por turismo y totales en una sola que contiene el porcentaje de turistas
def combinar_datos_visitantes(datos_turistas, datos_total_visitantes, región_actual):
	# Comprobar la validez de los datos
	if len(datos_turistas) != len(datos_total_visitantes):
		raise RuntimeError("Los datos para la región \"" + región_actual + \
			"\" no tienen el mismo número de valores de visitantes totales y visitantes turistas")
	
	# Recorrer entradas, combinándolas en una sola lista.
	# Cada elemento de la lista de salida contendrá un diccionario con 3 valores: año (int), mes (int) y porcentaje de turistas (float).
	lista_salida = []
	for i, dato_turistas in enumerate(datos_turistas):
		dato_total = datos_total_visitantes[i]
		
		if dato_turistas["fecha"] != dato_total["fecha"]:
			raise ValueError("La entrada nº " + i + " en los datos de la región " + región_actual + \
				" no tiene la misma fecha para los datos de turistas (" + dato_turistas["fecha"] + ") y de visitantes totales (" + \
				dato_total["fecha"] + ")")
		else:	
			fecha_separada = dato_turistas["fecha"].split('M')
			año = int(fecha_separada[0])
			mes = int(fecha_separada[1])
			
			try:
				porcentaje = float(dato_turistas["valor"]) / float(dato_total["valor"])
			except ValueError:
				# Faltan datos, nos saltamos esta entrada
				porcentaje = None
			
			if porcentaje != None:
				lista_salida.append({"año": año, "mes": mes, "porcentaje": porcentaje})
	
	return lista_salida


# Convierte el nombre de una región tal y como aparece en el csv de entrada al formato de región requerido por la BD.
# Utiliza el diccionario EQUIVALENCIAS_REGIÓN para ello.
def convertir_región(región):
	if región == VALOR_NACIONAL:
		return ""
	try:
		return EQUIVALENCIAS_REGIÓN[región]
	except KeyError as key_error:
		raise KeyError("La región \"" + región + "\" no tiene especificado un nombre de salida") from key_error


if __name__ == "__main__":
	main()