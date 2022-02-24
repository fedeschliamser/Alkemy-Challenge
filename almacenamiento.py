"""Definimos la funcion almacenamiento_func a fines de descargar y almacenar las bases de datos
en el repositorio de acuerdo a lo solicitado en la consigna"""
def almacenamiento_func():
     from datetime import datetime
     import os
     import logging
     import pandas as pd
     import requests

     day = datetime.today().strftime('%d')
     year = datetime.today().strftime('%Y')
     month = datetime.today().strftime('%B')
     date = datetime.now().strftime("%D:%m:%y")

     """Creamos los directorios para almacenar posteriormente las 3 bases de datos:"""

     os.makedirs(f'museos/{year}-{month}', exist_ok=True)
     os.makedirs(f'cines/{year}-{month}', exist_ok=True)
     os.makedirs(f'bibliotecas/{year}-{month}', exist_ok=True)

     try:
         if os.path.isfile(f'museos-{day}-{month}-{year}.csv') is True:
            os.remove(f'museos-{day}-{month}-{year}.csv')

         if os.path.isfile(f'cines-{day}-{month}-{year}.csv') is True:
            os.remove(f'cines-{day}-{month}-{year}.csv')

         if os.path.isfile(f'bibliotecas-{day}-{month}-{year}.csv') is True:
            os.remove(f'bibliotecas-{day}-{month}-{year}.csv')
         logging.debug('no hay archivos coincidentes')
     except Exception as e:
         logging.exception(f'Ocurrio una excepcion {e}')

     """Descargamos las 3 bases de datos utilizando la libreria Requests:"""

     try:
         museos = requests.get('https://datos.cultura.gob.ar/dataset/' \
             '37305de4-3cce-4d4b-9d9a-fec3ca61d09f/' \
             'resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/' \
             'download/museos.csv')

         open(f'museos/{year}-{month}/ museos-{day}-{month}-{year}.csv',
             'wb').write(museos.content)

         cines = requests.get('https://datos.cultura.gob.ar/dataset/' \
            '37305de4-3cce-4d4b-9d9a-fec3ca61d09f/' \
            'resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv')
         open(f'cines/{year}-{month}/ cines-{day}-{month}-{year}.csv',
             'wb').write(cines.content)

         bibliotecas = requests.get('https://datos.cultura.gob.ar/dataset/' \
             '37305de4-3cce-4d4b-9d9a-fec3ca61d09f/' \
             'resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/' \
             'biblioteca_popular.csv')
         open(f"bibliotecas/{year}-{month}/ bibliotecas-{day}-{month}-{year}.csv",
             'wb').write(bibliotecas.content)
         logging.debug('Los dataset han sido descargados de manera correcta')
     except Exception as e:
         logging.exception(f'Ocurrio una excepcion {e}')

     museosdir=f'museos/{year}-{month}/ museos-{day}-{month}-{year}.csv'
     cinesdir=f'cines/{year}-{month}/ cines-{day}-{month}-{year}.csv'
     bibliotecasdir=f"bibliotecas/{year}-{month}/ bibliotecas-{day}-{month}-{year}.csv"

     """Observamos si están correctamente guardadas las 3 bases de datos"""

     museos_csv=pd.read_csv(museosdir, encoding="utf-8")
     print(museos_csv.head())

     cines_csv=pd.read_csv(cinesdir, encoding="utf-8")
     print(cines_csv.head())

     bibliotecas_csv=pd.read_csv(bibliotecasdir, encoding="utf-8")
     print(bibliotecas_csv.head())
     return 
