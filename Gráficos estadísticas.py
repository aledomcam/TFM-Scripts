import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Resolución usada para los gráficos
DPI_GRÁFICOS = 300

def main():
	iteraciones = []
	líneasAbiertas = []
	líneasAVariar = []
	temperatura = []
	fitnessActual = []
	fitnessMejor = []
	probAceptación = []

	with open('stats_vnsrs.csv', newline = '') as entrada:
		reader = csv.reader(entrada, delimiter = ',')
		cabecera = True
		for fila in reader:
			if cabecera:
				cabecera = False
			else:
				iteraciones.append(int(fila[0]))
				líneasAbiertas.append(int(fila[1]))
				líneasAVariar.append(int(fila[2]))
				temperatura.append(float(fila[3]))
				fitnessActual.append(float(fila[4]))
				fitnessMejor.append(float(fila[5]))
				# La probabilidad de aceptación puede estar vacía
				probAceptación.append(None if fila[6] == "" else float(fila[6]))
		generarGráfico(iteraciones, líneasAbiertas, "step", "Líneas abiertas en cada iteración", "Iteración", "Líneas abiertas", "Líneas abiertas.png")
		valoresLíneasAVariar = np.unique(líneasAVariar)
		valoresLíneasAVariar = np.append(valoresLíneasAVariar, 0)
		generarGráfico(iteraciones, líneasAVariar, "step", "Entorno en cada iteración", "Iteración", "Líneas a variar", "Líneas a variar.png", valoresLíneasAVariar)
		generarGráfico(iteraciones, temperatura, "step", "Temperatura en cada iteración", "Iteración", "Temperatura", "Temperatura.png")
		generarGráfico(iteraciones, fitnessActual, "step", "Fitness en cada iteración", "Iteración", "Fitness", "Fitness actual.png")
		generarGráfico(iteraciones, fitnessMejor, "step", "Mejor fitness hasta el momento en cada iteración", "Iteración", "Fitness", "Fitness mejor.png")
		generarGráfico(iteraciones, probAceptación, "scatter", "Probabilidad de aceptación", "Iteración", "Probabilidad aceptación", "Prob aceptación.png")


"""
Genera un gráfico con los datos especificados. Por defecto, los ejes de coordenadas tendrán 11 marcas: El valor más bajo de su rango, el más alto y los 9
que haya de por medio.

x: Lista de valores a colocar en el eje X
y: Lista de valores a colocar en el eje Y
tipoGráfico: Tipo de gráfico a generar. Valores admitidos: "step", "scatter".
nombreGráfico: Nombre a mostrar en el gráfico
nombreEjeX: Nombre a mostrar en el eje X
nombreEjeY: Nombre a mostrar en el eje Y
nombreFichero: Nombre del fichero en el que se guardará la imagen del gráfico
rangoY: Si se especifica, éstos serán los valores que se marcarán en el eje Y. Si no se especifica, se usa el funcionamiento por defecto
"""
def generarGráfico(x, y, tipoGráfico, nombreGráfico, nombreEjeX, nombreEjeY, nombreFichero, rangoY = []):
	if tipoGráfico == "step":
		plt.step(x, y)
	elif tipoGráfico == "scatter":
		plt.scatter(x, y, s=2)
	else:
		raise ValueError("El tipo de gráfico \"" + tipoGráfico + "\" no existe o no está soportado.")
	plt.xticks(intervalo(x[0], x[-1], 10, False))
	if len(rangoY) == 0:
		# Calcular valor mínimo y máximo del conjunto, filtrando los "None" que pueda haber
		minY = min(valY for valY in y if valY is not None)
		maxY = max(valY for valY in y if valY is not None)
		plt.yticks(intervalo(minY, maxY, 10, True))
	else:
		plt.yticks(rangoY)
	plt.title(nombreGráfico)
	plt.xlabel(nombreEjeX)
	plt.ylabel(nombreEjeY)
	plt.savefig(nombreFichero, dpi=DPI_GRÁFICOS)
	plt.clf()


"""
Devuelve un array que contiene (numValores) valores equidistantes entre (valMin) y (valMax), ambos incluidos.

decimales: Si es true, los valores resultantes podrán ser decimales. Si no, se redondearán al entero más cercano.
"""
def intervalo(valMin, valMax, numValores, decimales):
	ret = []
	step = (valMax - valMin) / (numValores - 1)
	
	for i in range(0, numValores):
		if decimales:
			ret.append(valMin + step * i)
		else:
			ret.append(round(valMin + step * i))
	
	return ret


if __name__ == "__main__":
	main()