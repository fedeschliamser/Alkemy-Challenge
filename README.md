# Alkemy Challenge

El presente repositorio hace referencia al Challenge de Alkemy "Data Analytics and Python", en el cual el objetivo es descargar información de 3 bases de datos correspondientes a museos, cines y bibliotecas populares; procesar la información y crear 3 tablas de datos para luego generar una base de datos SQL

## Tecnologías utilizadas

Pandas: pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.

## Requerimientos a instalar

Se debe tener instalado en el sistema operativo Python3 (https://www.python.org) y la base de datos POSTGRESQL (https://www.postgresql.org/)

También se debe tener instalado virtualenv para crear un entorno virtual. En caso contrario, ejecutar en la terminal: $ pip install virtualenv

## Pasos a realizar

1. Crear el repositorio en donde se almacenará el proyecto, y clonar todos los archivos desde este repositorio de github
2. Crear y activar el entorno virtual, para ello deberá ejecutarse lo siguiente dentro del repositorio ya creado previamente:
   - $ virtualenv  venv -p python3 (crea el entorno virtual)
   - $ source venv/bin/activate (activa el entorno virtual)
3. Instalar las dependencias necesarias, ejecutando el código $ pip install -r requirements.txt
4. Conectar a la base de datos utilizando pgAdmin4 (Instalarlo de la web que explica el ítem "Requerimientos a instalar"), utilizando el usuario postgresql y contraseña postgresql
5. Ejecutar el código desde main.py


## Resultados obtenidos:

En el archivo visualizacion.ipynb, ejecuado en Jupyter Notebook, se pueden observar algunos resultados obtenidos con el procesamiento de los datos, utilizando las librerias Pandas y Matplotlib
