﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
import random
import datetime
assert cf
import tracemalloc
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Caracterizar las reproducciones")
    print("3- Encontrar música para festejar")
    print("4- Encontrar música para estudiar")
    print("5- Estudiar géneros musicales")
    print("6- Indicar género musical mas escuchado en un horario")
    print("0- Salir")

catalog = None

#Funciones de requerimiento

def req_1(catalog,criterio,val_min,val_max):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    #Funciones de requerimiento
    pistas = catalog['Pistas']
    arbol = controller.ArbolDe(catalog,pistas,criterio)
    rep_art = controller.songsByValues(arbol,val_min,val_max)
    printReq1(rep_art,content,val_min,val_max)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return delta_time,delta_memory

def req_2(catalog,ene_min,ene_max,dan_min,dan_max):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    #Funciones de requerimiento
    pistas = catalog['Pistas']
    arbol_ene = controller.ArbolDe(catalog,pistas,'energy')
    arbol_dan = controller.filtradoenlista(om.values(arbol_ene,ene_min,ene_max),'danceability',dan_min, dan_max)
    printReq2_3(arbol_dan,"energy","danceability",ene_min,ene_max,dan_min,dan_max,2)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return delta_time,delta_memory

def req_3(catalog, instru_min,instru_max,tempo_min,tempo_max):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    #Funciones de requerimiento
    pistas = catalog['Pistas']
    arbol_spech = controller.ArbolDe(catalog,pistas, "tempo")
    filtradoinstrumental = controller.filtradoenlista(om.values(arbol_spech, tempo_min, tempo_max),"instrumentalness",instru_min,instru_max)
    printReq2_3(filtradoinstrumental,"instrumentalness","tempo",instru_min,instru_max,tempo_min,tempo_max,3)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return delta_time,delta_memory
    
def req_4(generosconsulta, catalog):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    #Funciones de requerimiento
    arboltempo = controller.ArbolDe(catalog, catalog['Pistas'], "tempo")
    generos = generosconsulta.split(",")
    rep = 0
    linea = ""
    for genero in generos:
        gen = genero.lower()
        rango = mp.get(catalog['Generos'], gen)
        rango = me.getValue(rango)
        individual = controller.songsByValues(arboltempo,rango[0],rango[1])
        lin_rep = preprintreq4(individual,gen,rango)
        rep+= lin_rep[1]
        linea+= '\n'+lin_rep[0]
    printReq4(rep,linea)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return delta_time,delta_memory
        
def req_5(catalog,hor_min,hor_max):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    #Funciones de requerimiento
    hora_min = datetime.datetime.strptime(hor_min, '%H:%M:%S')
    hora_max = datetime.datetime.strptime(hor_max, '%H:%M:%S')
    Filtrohora = controller.separarpistas(catalog,om.values(catalog['Registros_Eventos'], hora_min.time(), hora_max.time()))
    lista_generos = controller.recorridogenero(catalog,Filtrohora)
    size = lt.size(lista_generos)
    orden_generos = controller.order_generos(lista_generos,size)
    genero_top = lt.getElement(orden_generos,1)
    orden_canciones = controller.order_canciones(genero_top)
    Sval_canciones = controller.Svalues_songs(orden_canciones,catalog)
    #Sval retorna una tupla con 1. la lista de canciones del genero top con el svalor añadido. 2. el svalor promedio de todas las canciones
    printReq5(orden_generos,Sval_canciones,hor_min,hor_max)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return delta_time,delta_memory

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

#Funciones de impresión

def printReq1(rep_art,content,val_min,val_max):
    print('+'*10,' Resultados Req. #1...', '+'*10)
    linea = content + ' entre ' +str(val_min) +' y ' + str(val_max)
    respuesta = 'Reproducciones totales: ' + str(rep_art[0]) + ' Número de artistas únicos totales: ' + str(rep_art[1])
    print(linea)
    print(respuesta)

def printReq2_3(rep_art,crit1,crit2,val1_min,val1_max,val2_min,val2_max,req):
    track_list = rep_art[0]
    print('+'*10,' Resultados Req. #'+str(req) +'...', '+'*10)
    linea = crit1.title() + ' entre ' +str(val1_min) +' y ' + str(val1_max)
    linea2 = crit2.title() + ' entre ' +str(val2_min) +' y ' + str(val2_max)
    respuesta = 'Número de pistas únicas totales: ' + str(lt.size(track_list))
    print(linea)
    print(linea2)
    print(respuesta)
    print('\n'+ '-'*10,' Pistas únicas ', '-'*10)
    i = 0
    while i < 5:
        r = random.randint(0,lt.size(track_list))
        cancion = lt.getElement(track_list,r)
        track_id = cancion['track_id']
        crit_1 = cancion[crit1]
        crit_2 = cancion[crit2]
        rand = 'Pista '+ str(i+1) +': ' + track_id + ' con ' + str(crit1) +' de ' + crit_1 + ' y '\
            + crit2 + ' de ' + str(crit_2)
        print(rand)
        i+=1

def preprintreq4(lista,gen,ran)->None:
    i=0
    rep = 0
    linea = '='*10+' ' +gen.upper()+' '+'='*10+'\nPara '+gen.title()+' el tempo está entre '+str(ran[0])+' y '+str(ran[1])+' BPM\nReproducciones de '+gen.title()+': '\
        +str(lista[0])+' con '+str(lista[1])+' artistas diferentes\n'+'-'*5+ ' Algunos artistas de '+str(gen.title())+'-'*5+'\n'
    rep += lista[0]
    while i<10:
        r = random.randint(0,lt.size(lista[3]))
        cancion = lt.getElement(lista[3],r)
        art_id = cancion['artist_id']
        rand = 'Artista '+ str(i+1) +': ' + art_id +'\n'
        linea+=rand
        i+=1
    return linea,rep

def printReq4(rep,lin):
    print('+'*10,' Resultados Req. #4...', '+'*10)
    print('Número total de reproducciones:',rep)
    print(lin)

def printReq5(lista_generos,lista_canciones,hora_min,hora_max):
    tot_reproducciones = 0
    for num in range(0,lt.size(lista_generos)):
        gen = lt.getElement(lista_generos,num)
        tot_reproducciones+=gen[0]
    print('+'*10,' Resultados Req. #5...', '+'*10)
    horas = 'Hay un total de '+str(tot_reproducciones)+' reproducciones entre '+hora_min+' y '+hora_max
    title = '='*20+' Generos organizados por reproducciones '+'='*20
    print(horas)
    print(title)
    i = 1
    while i <= lt.size(lista_generos):
        genero = lt.getElement(lista_generos,i)
        top = 'TOP '+str(i)+': '+genero[2]+' con '+str(genero[0])+' reproducciones'
        print(top)
        i+=1
    print('...')
    genero = lt.getElement(lista_generos,1)
    top_title = 'El genero TOP es '+genero[2]+' con '+str(genero[0])+' reproducciones'
    title = '='*20+' Análisis de sentimiento en '+genero[2]+' '+'='*20
    print(top_title)
    print(title)
    lista_canciones_temporal = genero[1]
    pistas = genero[2]+' tiene '+str(lt.size(lista_canciones_temporal))+' pistas únicas...'
    print(pistas)
    pistas = 'El TOP 10 de estas pistas es...'
    print(pistas)
    j = 1
    while j <= 10:
        cancion = lt.getElement(lista_canciones[0],j)
        num_hash = lt.size(cancion['hashtags'])
        top = 'TOP '+str(j)+' track: '+cancion['track_id']+' con '+str(num_hash)+' hashtags y un VADER de: '+str(round(cancion['VaderProm'],1))
        print(top)
        j+=1

def print_events(catalog):
    eventos = catalog['Eventos']
    size = lt.size(eventos)
    if size:
        print('Estos son los primeros 5 eventos cargados')
        i = 0
        while i <5:
            print("-"*237)
            primera_linea = "{0:<2}{1:^20}{2:^20}{3:^20}{4:^20}{5:^20}{6:^20}{7:^20}{8:^20}{9:^20}{10:^20}\
                ".format(str(i+1)+('.'),'ID del evento','Instrumentalidad','Viveza','Habla','Danzabilidad','Valencia','Ruido','Tempo','Acusticidad','Energía')
            print(primera_linea)
            evento = lt.getElement(eventos,i)
            event_id = evento['id']
            inst = evento['instrumentalness']
            live = evento['liveness']
            spe = evento['speechiness']
            dance = evento['danceability']
            val = evento['valence']
            loud = evento['loudness']
            temp = evento['tempo']
            aco = evento['acousticness']
            ene = evento['energy']            
            info_video = "{0:<2}{1:^20}{2:^20}{3:^20}{4:^20}{5:^20}{6:^20}{7:^20}{8:^20}{9:^20}{10:^20}".format(' ',event_id,inst,live,spe,dance,val,loud,temp,aco,ene)
            print(info_video)

            segunda_linea = "{0:^20}{1:^20}{2:^10}{3:^25}{4:^40}{5:^40}\
                ".format('Modo','Tonalidad','Lenguaje','Lugar de creacion','Zona horaria','ID de la pista')
            print(segunda_linea)
            mode = evento['mode']
            key = evento['key']
            lang = evento['tweet_lang']
            cre_at = evento['created_at']
            time_zone = evento['time_zone']
            track_id = evento['track_id']            
            info2_video = "{0:^20}{1:^20}{2:^10}{3:^25}{4:^40}{5:^40}".format(mode,key,lang,cre_at,time_zone,track_id)
            print(info2_video)
            i+=1
        print('\nY estos son los últimos 5 eventos cargados\n')
        j=lt.size(catalog['Eventos'])
        while j > lt.size(catalog['Eventos'])-5:
            print("-"*237)
            primera_linea = "{0:<8}{1:^20}{2:^20}{3:^20}{4:^20}{5:^20}{6:^20}{7:^20}{8:^20}{9:^20}{10:^20}\
                ".format(str(j)+('.'),'ID del evento','Instrumentalidad','Viveza','Habla','Danzabilidad','Valencia','Ruido','Tempo','Acusticidad','Energía')
            print(primera_linea)
            evento = lt.getElement(eventos,j)
            event_id = evento['id']
            inst = evento['instrumentalness']
            live = evento['liveness']
            spe = evento['speechiness']
            dance = evento['danceability']
            val = evento['valence']
            loud = evento['loudness']
            temp = evento['tempo']
            aco = evento['acousticness']
            ene = evento['energy']            
            info_video = "{0:<8}{1:^20}{2:^20}{3:^20}{4:^20}{5:^20}{6:^20}{7:^20}{8:^20}{9:^20}{10:^20}".format(' ',event_id,inst,live,spe,dance,val,loud,temp,aco,ene)
            print(info_video)

            segunda_linea = "{0:^20}{1:^20}{2:^10}{3:^25}{4:^40}{5:^40}\
                ".format('Modo','Tonalidad','Lenguaje','Lugar de creacion','Zona horaria','ID de la pista')
            print(segunda_linea)
            mode = evento['mode']
            key = evento['key']
            lang = evento['tweet_lang']
            cre_at = evento['created_at']
            time_zone = evento['time_zone']
            track_id = evento['track_id']            
            info2_video = "{0:^20}{1:^20}{2:^10}{3:^25}{4:^40}{5:^40}".format(mode,key,lang,cre_at,time_zone,track_id)
            print(info2_video)
            j-=1
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        tipo = int(input("Ingrese 1 si desea manejar las colisiones con el método chaining o 2 para linear probing: "))
        #tipo = 2
        load_factor = float(input("Ingrese el factor de carga con el que desea trabajar: "))
        #load_factor = 0.5
        print("Cargando información de los archivos...")
        #cambio medida tiempo y memoria
        catalog = controller.init(tipo,load_factor)
        answer = controller.loadData(catalog,tipo)
        print('El total de registros de eventos de escucha cargados es de: ' + str(lt.size(catalog['Eventos'])))
        print('El total de artistas únicos cargados es de: '+ str(lt.size(catalog['Artistas'])))
        print('El total de pistas de audio únicas cargadas es de: ' + str(mp.size(catalog['Pistas'])))
        print_events(catalog)
        print("Cargado correctamente")
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    elif int(inputs[0]) == 2:
        #content = 'instrumentalness'
        content = input('Ingrese la característica sobre la que desea hacer la consulta: ').lower()
        #val_min = 0.5
        val_min = float(input("Ingrese el valor mínimo de esta característica: "))
        #val_max = 0.75
        val_max = float(input("Ingrese el valor máximo de esta característica: "))
        answer = req_1(catalog,content,val_min,val_max)
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    elif int(inputs[0]) == 3:
        #ene_min = 0.5
        ene_min = float(input("Ingrese el valor mínimo de energía de la canción: "))
        #ene_max = 0.75
        ene_max = float(input("Ingrese el valor máximo de energía de la canción: "))
        #dan_min = 0.75
        dan_min = float(input("Ingrese el valor mínimo de danzabilidad de la canción: "))
        #dan_max = 1.00
        dan_max = float(input("Ingrese el valor máximo de danzabilidad de la canción: "))
        answer = req_2(catalog,ene_min,ene_max,dan_min,dan_max)
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    elif int(inputs[0]) == 4:
        #instru_min = 0.6
        instru_min =  float(input("Ingrese el valor mínimo de instrumentalidad de la canción: "))
        #instru_max = 0.9
        instru_max =    float(input("Ingrese el valor máximo de instrumentabilidad de la canción: "))
        #tempo_min = 40.0
        tempo_min = float(input("Ingrese el valor mínimo de tempo de la canción: "))
        #tempo_max = 60.0
        tempo_max = float(input("Ingrese el valor máximo de tempo de la canción: "))
        answer = req_3(catalog, instru_min,instru_max, tempo_min,tempo_max)
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    elif int(inputs[0]) == 5:
        eleccion = "8"
        generosconsulta = ""
        #i = 1
        while int(eleccion[0]) != 3:
            eleccion = input("-Presione 1 para escribir los generos a estudiar ya guardados\n-Presione 2 para añadir uno \n-Presione 3 para confirmar la lista de generos a estudiar\n")
            '''
            if i == 1:
                eleccion = '1'
            else:
                eleccion = '3'
            ''' 
            if int(eleccion[0])==1:
                generosconsulta += input("Escriba los generos a consultar separados por comas:\n")
                #generosconsulta = 'Reggae,Hip-Hop,Pop'
            if int(eleccion[0]) == 2:
                nombre = input("Ingrese un nombre unico para el nuevo genero:\n").lower()
                tempo_min = float(input("Ingrese el BPM minimo: "))
                tempo_max = float(input("Ingrese el BPM maximo: "))
                mp.put(catalog['Generos'],nombre,(tempo_min,tempo_max))
                generosconsulta+= ","+nombre
            if int(eleccion[0]) == 3:
                answer = req_4(generosconsulta,catalog)
                print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
                "Memoria [kB]: ", f"{answer[1]:.3f}")
            #i += 2
    elif int(inputs[0]) == 6:
        hora_min = input("Hora inicial (hh:mm:ss): ")
        #hora_min = '07:15:00'
        hora_max = input("Hora final (hh:mm:ss): ")
        #hora_max = '09:45:00'
        answer = req_5(catalog,hora_min,hora_max)
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    elif int(inputs[0]) == 0:
        sys.exit(0)
sys.exit(0)
