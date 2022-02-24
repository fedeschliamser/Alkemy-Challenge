import pandas as pd
import numpy as np
import re

"""Definimos la función preprocesamiento_func a fines de realizar el preprocesamiento de los datos"""
def preprocesamiento_func(museosdir, bibliotecasdir, cinesdir):
    data_museos = pd.read_csv(museosdir)

    """Normalizamos las 3 bases de datos para poder trabajar con columnas con la misma nomenclatura, 
    a fines de evitar errores en el procesamiento de los datos"""
    data_museos.columns = map(str.lower, data_museos.columns)
    data_museos = data_museos.rename(columns=lambda x: re.sub(r'(id)', r'\1_', x))
    dictionary = {'cod_loc': 'cod_localidad', 'localid_ad': 'localidad', 'cp':  'código postal',
                  'categoria': 'categoría', 'teléfono': 'número de teléfono', 'telefono': 'número de teléfono',
                  'dirección': 'domicilio', 'direccion': 'domicilio'}
    data_museos = data_museos.rename(columns=dictionary)
    
    data_biblio = pd.read_csv(bibliotecasdir)
    data_biblio.columns = map(str.lower, data_biblio.columns)
    data_biblio = data_biblio.rename(columns=lambda x: re.sub(r'(id)', r'\1_', x))
    dictionary = {'cod_loc': 'cod_localidad', 'localid_ad': 'localidad', 'cp':  'código postal',
                  'Categoria': 'categoría', 'teléfono': 'número de teléfono', 'telefono': 'número de teléfono',
                  'dirección': 'domicilio', 'direccion': 'domicilio'}
    data_biblio = data_biblio.rename(columns=dictionary)
    
    data_cines = pd.read_csv(cinesdir)
    data_cines.columns = map(str.lower, data_cines.columns)
    data_cines = data_cines.rename(columns=lambda x: re.sub(r'(id)', r'\1_', x))
    dictionary = {'cod_loc': 'cod_localidad', 'localid_ad': 'localidad', 'cp':  'código postal',
                  'Categoria': 'categoría', 'teléfono': 'número de teléfono', 'telefono': 'número de teléfono',
                  'dirección': 'domicilio', 'direccion': 'domicilio'}
    data_cines = data_cines.rename(columns=dictionary)
    """Devolvemos las bases de datos preprocesadas al main"""
    return data_museos, data_biblio, data_cines
