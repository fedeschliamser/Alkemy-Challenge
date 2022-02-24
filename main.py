import pandas as pd
import numpy as np
import logging
import psycopg2 
import requests
import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, Integer, Text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re
from almacenamiento import almacenamiento_func
from preprocesamiento import preprocesamiento_func

"""Importamos la función almacenamiento_func del archivo almacenamiento.py con la cual descargamos las bases
correspondientes a cines, museos y bibliotecas populares; luego importamos la función preprocesamiento_func
mediante la cual normalizamos las columnas de las tres bases de datos previamente mencionadas"""

logging.basicConfig(filename="app.log",level=logging.DEBUG,
format="%(asctime)s:%(levelname)s:%(message)s")

day = datetime.today().strftime("%d")
year = datetime.today().strftime('%Y')
month = datetime.today().strftime('%B')
date = datetime.now().strftime("%D:%m:%y")

"""Una vez normalizadas las columnas de las bases, las concatenamos para obtener las tablas solicitadas mediante
la función concatenacion:"""
def concatenacion(data_cines,data_biblio,data_museos):
     print (data_museos)
     print (data_cines)
     print (data_biblio)
     data_concat=pd.concat([data_cines,data_biblio,data_museos])
     print (data_concat.head())

     data_concat = data_concat.loc[:,['cod_localidad','id_provincia','id_departamento','categoría','provincia','localidad',
                       'nombre','domicilio','código postal', 'mail', 'web', 'número de teléfono', 'fuente']]
     
     print("Tabla con datos de museos, bibliotecas y cines concatenados:")
     
     print (data_concat.head())
     logging.debug(f'Se realizó con éxito la concatenación de las 3 bases de datos')
     return data_concat

"""Realizamos la función totales_categoria mediante la cual agrupamos los registros por categoria:"""
def totales_categoria(data_total):
     registros_categoria = data_total.groupby('categoría').size()
     print(registros_categoria)
     return registros_categoria


"""Observamos la cantidad de registros según la columna fuente mediante la función totales_fuente:"""
def totales_fuente(data_total):
     registros_fuente = data_total.groupby('fuente').size()
     print(registros_fuente)
     return registros_fuente


"""Observamos la cantidad de registros segun provincia y categoria, utilizando la función
totales_por_categoria_provincia:"""
def totales_por_categoria_provincia(data_total):
     registros_categoria_provincia = data_total.groupby(['categoría', 'provincia']).size()
     print(registros_categoria_provincia)

     categorias = data_total.groupby('categoría').size()
     fuentes = data_total.groupby('fuente').size()

     cat_prov_fuente = pd.concat([categorias, fuentes, registros_categoria_provincia], axis=1)
     columnas = ['Registros por categoria', 'Registros por fuente', 'Registros por categoria y provincia']
     cat_prov_fuente.columns = columnas
     print("Tabla con los registros por categoría, fuente y categoría por provincia:")
     print(cat_prov_fuente)

     return cat_prov_fuente

"""Creamos la función tabla_cines para realizar una tabla con la información de la base de cines:"""
def tabla_cines(data_cines):
     data_cines.info()
     data_cines['espacio_incaa']= data_cines['espacio_incaa'].fillna(0)
     data_cines['espacio_incaa'] = data_cines['espacio_incaa'].replace('si',1)
     data_cines['espacio_incaa'] = data_cines['espacio_incaa'].replace('SI',1)
     print(data_cines['espacio_incaa'].value_counts())

     data_cines['espacio_incaa'] = data_cines['espacio_incaa'].astype(int)

     data_cines_table=pd.pivot_table(data_cines,index='provincia',aggfunc='sum',values=['pantallas','butacas','espacio_incaa']).sort_values(ascending=False,by='pantallas')
     print("Información de cines de acuerdo a provincia, cantidad de pantallas, butacas y espacio INCAA:")
     print(data_cines_table)
     logging.debug(f'Se realizo con exito la Tabla correspondiente a la base de datos de cines')
     return data_cines_table

"""Creamos la función tablas_to_sql con la cual realizamos la conexión con la base Postgresql y creamos
las 3 tablas solicitadas en la consigna"""

def tablas_to_sql(data_total,data_cines_table,cat_prov_fuente):
      try:
           connection = {
           'host': 'localhost',
           'port': '5432',
           'user': 'postgres',
           'password': 'postgresql',
           'database': 'postgres'
      }
    
      except:
            print("No pudo conectarse con la base")
            return False

      conn = psycopg2.connect(**connection)
      cur = conn.cursor()

      """Confirmamos conexion imprimendo la version"""
      cur.execute('SELECT version()')
      version = cur.fetchone()
      print(version)

      file = open('bases.sql').read()
      rows = file.split(';')[:-1]  

      """Ejecutamos los comandos en script.sql"""
      for row in rows:
           cur.execute(row)
           conn.commit()

      conn.close()

      engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
      Base = declarative_base()
      Session = sessionmaker(blind=engine)
     
      data_total.to_sql(name='concatenada_table', con=engine, if_exists='replace', index=False)
      cat_prov_fuente.to_sql(name='registros_table', con=engine, if_exists='replace', index=False)
      data_cines_table.to_sql(name='cines_table', con=engine, if_exists='replace', index=False)

      return True

if __name__ == '__main__':
     almacenamiento_func()
     museosdir=f'museos/{year}-{month}/ museos-{day}-{month}-{year}.csv'
     cinesdir=f'cines/{year}-{month}/ cines-{day}-{month}-{year}.csv'
     bibliotecasdir=f"bibliotecas/{year}-{month}/ bibliotecas-{day}-{month}-{year}.csv"
     data_museos, data_biblio, data_cines=preprocesamiento_func(museosdir, bibliotecasdir, cinesdir)
     data_total=concatenacion(data_cines,data_biblio,data_museos)
     totales_categoria(data_total)
     totales_fuente(data_total)
     data_categorias  = totales_por_categoria_provincia(data_total)
     data_cines_table=tabla_cines(data_cines)
     tablas_to_sql(data_total,data_cines_table,data_categorias)
    