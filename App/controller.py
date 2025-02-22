﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import time
import tracemalloc
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init(tipo: int, factor:float):
    """
    Llama la funcion de inicializacion  del modelo.
    """
    if tipo == 1:
        tipo = "CHAINING"
    else:
        tipo = "PROBING"
    # catalog es utilizado para interactuar con el modelo
    catalogo = model.NewCatalog(tipo,factor)
    return catalogo

def loadData(catalogo, tipolista):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadEventos(catalogo)
    loadSvalues(catalogo)
    loadRegistros(catalogo)
    loadContent(catalogo)
    loadGenerosiniciales(catalogo)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    tupla = (delta_time, delta_memory)
    return tupla
    
# Funciones para la carga de datos

def loadEventos(catalogo):
    pistafile = cf.data_dir + 'context_content_features-5pct.csv'
    input_file = csv.DictReader(open(pistafile, encoding='utf-8'),delimiter = ',')
    for pista in input_file:
        model.addPista(catalogo, pista)
        model.addEvento(catalogo,pista)


def loadSvalues(catalogo):
    sfile = cf.data_dir + 'sentiment_values.csv'
    input_file = csv.DictReader(open(sfile, encoding='utf-8'),delimiter = ',')
    for svalue in input_file:
        model.addSvalue(catalogo,svalue)
        
def loadRegistros(catalogo):
    eventofile = cf.data_dir + 'user_track_hashtag_timestamp-5pct.csv'
    input_file = csv.DictReader(open(eventofile, encoding='utf-8'),delimiter = ',')
    for evento in input_file:
        model.addRegistro(catalogo,evento)

def loadContent(catalogo):
    model.addContent(catalogo)

def loadGenerosiniciales(catalogo):
    model.addGenerosniciales(catalogo)
# Funciones de ordenamiento

def order_generos(generos,size):
    return model.orden_generos(generos,size)

def separarpistas(catalogo, lista):
    pistaslistas = model.separarpistas(catalogo,lista)
    return pistaslistas

def recorridogenero(catalogo,pistas):
    tupla = model.recorridogeneros(catalogo,pistas)
    return tupla

def order_canciones(Sval_canciones):
    return model.orden_canciones(Sval_canciones)
    
# Funciones de consulta sobre el catálogo

def ArbolDe(catalog,pistas, criterio):
    arbol = model.Arbolde(catalog,pistas,criterio)
    return arbol

def filtradoenlista(lista,criterio, min_, max_):
    derivado = model.filtradoenlista(lista, criterio, min_, max_)
    return derivado

def songsByValues(arbol,val_min,val_max):
    return model.songsByValues(arbol,val_min,val_max)

def Svalues_songs(orden_generos,catalog):
    return model.cancionestop(orden_generos,catalog)

#FUNCIONES TIEMPO
def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

