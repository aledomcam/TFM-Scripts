# TFM-Scripts
Este repositorio contiene una serie de scipts auxiliares empleados durante la realización de mi Trabajo de Fin de Máster, que se puede consultar [en el Archivo Digital de la UPM](https://oa.upm.es/71403/).

Los scripts están implementados en Python, y se usan para convertir datos o generar información de salida útil en diversas fases del trabajo.

En concreto, los scripts incluidos son los siguientes:

- `Conversor salida Neo4J.py`: Dado un fichero que contenga el resultado de una consulta a la base de datos de Neo4J usada durante la realización del TFM, crea un nuevo archivo con los datos en otro formato.
- `Gráficos estadísticas.py`: Script utilizado para generar gráficas que muestran cómo evoluciona una ejecución de la metaheurística implementada en el TFM. Recibe como entrada un fichero CSV con las estadísticas de la ejecución, que se obtiene al ejecutar la metaheurística con el plugin principal del trabajo.
- `Gráficos sensibilidad.py`: Genera gráficas que muestran los resultados del análisis de sensibilidad de pesos que se puede ejecutar desde el plugin principal del trabajo.
- `Selección líneas aleatorias.py`: Script básico usado para obtener un subconjunto de elementos al azar dado un fichero de entrada que los lista todos.
- `ETL/Conversión de gasto por país de origen.py` y `ETL/Conversión de visitantes por motivo.py`: Scripts empleados para convertir un fichero CSV con datos de turismo del INE a otro formato que permita su importación en la base de datos con la que se trabajó durante el TFM.

La carpeta `ETL` también contiene dos ficheros CSV como ejemplo de los datos que reciben como entrada los scripts ETL.

Véase también el [repositorio principal del proyecto](https://github.com/aledomcam/TFM-EarlyWarn).