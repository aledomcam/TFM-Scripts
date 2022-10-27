import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Resolución usada para los gráficos
DPI_GRÁFICOS = 300

# Nombres de ficheros de entrada
FICHERO_ENTRADA_FITNESS = "sensibilidad_fitness.csv"
FICHERO_ENTRADA_RANKING = "sensibilidad_ranking.csv"

"""
Representa información acerca de una solución del análisis de sensibilidad a lo largo de las diferentes iteraciones del análisis de sensibilidad
"""
class DatosSolución:
	"""
	Instancia la clase.
	
	nombreSolución: Nombre de la solución
	valores: Datos de la solución obtenidos en cada iteración
	"""
	def __init__(self, nombreSolución):
		self.nombreSolución = nombreSolución
		self.valores = []

	"""
	Añade un nuevo dato al array de datos de esta solución
	"""
	def añadirDato(self, dato):
		self.valores.append(float(dato))
	
	def __str__(self):
		return "(" + self.nombreSolución + ") " + str(self.valores);
	
	def __repr__(self):
		return self.__str__()


def main():
	datosFitness = cargarDatos(FICHERO_ENTRADA_FITNESS)
	datosRanking = cargarDatos(FICHERO_ENTRADA_RANKING)
	
	generarSalida(datosFitness, "fitness", "Fitness", False, False)
	generarSalida(datosRanking, "ranking", "Ranking", True, True)


"""
Carga uno de los ficheros CSV de salida del análisis de sensibilidad y devuelve un array que contiene los datos de cada una de las soluciones consideradas en el análisis.
Los datos de cada solución se almacenan en instancias de la clase DatosSolución.

nombreFichero: Nombre del fichero CSV a abrir
return: Array con los datos de todas las soluciones, cada uno representado con una instancia de DatosSolución.
"""
def cargarDatos(nombreFichero):
	ret = []
	
	with open(nombreFichero, newline = '') as entrada:
		reader = csv.reader(entrada, delimiter = ',')
		cabecera = True
		for fila in reader:
			if cabecera:
				for nombreSolución in fila:
					ret.append(DatosSolución(nombreSolución))
				cabecera = False
			else:
				for i, valor in enumerate(fila):
					datosSolución = ret[i]
					datosSolución.añadirDato(valor)
	return ret


"""
Genera un fichero CSV y dos gráficas mostrando los datos especificados para cada solución considerada en el análisis de sensibilidad.
El CSV será una tabla que contendrá la información más importante (valor medio, mínimo, máximo, percentiles principales...), mientras que las imágenes mostrarán
el rango en el que se mueven los valores para cada solución, así como la probabilidad acumulada de cada uno.

datosSoluciones: Datos de las diferentes soluciones
sufijo: String que añadir como sufijo a los nombres de los ficheros generados
nombreEje: Nombre del eje Y en el diagrama de cajas y del eje X en el gráfico de probabilidad acumulada
forzarInts: Si es true, los valores resultantes serán enteros. Si no, serán floats.
ranking: Si es true, se usará una representación de ranking. Los ejes que listen posiciones de ranking solo mostrarán enteros, y se colocarán al revés si son un eje Y.
Además, al representar la función de distribución, se mostrarán todos los valores posibles en el eje X.
"""
def generarSalida(datosSoluciones, sufijo, nombreEje, forzarInts, ranking):
	# Generar tabla resumen en un CSV
	with open('salida_' + sufijo + '.csv', 'w', newline = '', encoding = "utf-8") as salida:
		writer = csv.writer(salida, delimiter = ',')
		writer.writerow(["Solución", "Valor original", "Media", "Min", "P25", "P50", "P75", "Max", "Std"])
		
		for datosSolución in datosSoluciones:
			valores = datosSolución.valores
			row = [datosSolución.nombreSolución]
			row.append(intCondicional(valores[0], forzarInts))
			row.append(sum(valores) / len(valores))
			row.append(intCondicional(min(valores), forzarInts))
			row.append(intCondicional(np.percentile(valores, 25), forzarInts))
			row.append(intCondicional(np.percentile(valores, 50), forzarInts))
			row.append(intCondicional(np.percentile(valores, 75), forzarInts))
			row.append(intCondicional(max(valores), forzarInts))
			row.append(np.std(valores))
			
			writer.writerow(row)
	
	# Generar diagrama de cajas para cada solución
	datos = []
	nombres = []
	
	for datosSolución in datosSoluciones:
		datos.append(datosSolución.valores)
		nombres.append(datosSolución.nombreSolución)
	
	plt.boxplot(datos, labels = nombres)
	plt.xlabel("Soluciones")
	plt.ylabel(nombreEje)
	if ranking:
		plt.gca().yaxis.get_major_locator().set_params(integer = True)
		plt.gca().invert_yaxis()
	plt.savefig(sufijo + '_boxplot.png', dpi = DPI_GRÁFICOS)
	plt.clf()

	# Generar gráfica con la distribución de probabilidad acumulada para cada solución
	if ranking:
		plt.hist(datos, label = nombres, density = True, histtype = "step", cumulative = "True", bins = len(datosSoluciones))
		plt.gca().xaxis.get_major_locator().set_params(integer = True)
	else:
		plt.hist(datos, label = nombres, density = True, histtype = "step", cumulative = "True", bins = 30)
	plt.xlabel(nombreEje)
	plt.ylabel("Probabilidad")
	plt.legend()
	plt.savefig(sufijo + '_distribución.png', dpi = DPI_GRÁFICOS)
	plt.clf()


"""
Si "convertir" es true, convierte el valor a entero. Si no, lo devuelve tal cual.
"""
def intCondicional(valor, convertir):
	if convertir:
		return int(valor)
	else:
		return valor


"""
Devuelve un array que contiene (numValores) valores equidistantes entre (valMin) y (valMax), ambos incluidos.

decimales: Si es true, los valores resultantes podrán ser decimales. Si no, se redondearán al entero más cercano.
"""
def intervalo(valMin, valMax, numValores, decimales):
	ret = []
	step = (valMax - val_min) / (numValores - 1)
	
	for i in range(0, numValores):
		if decimales:
			ret.append(valMin + step * i)
		else:
			ret.append(round(valMin + step * i))
	
	return ret


if __name__ == "__main__":
	main()