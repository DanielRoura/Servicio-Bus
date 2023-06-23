author = "Daniel Roura Sepúlveda"

import pymongo
import auxiliar.auxiliar as AUX
import auxiliar.env as ENV
from fastapi import APIRouter

uri = ENV.uri_bd
cliente = pymongo.MongoClient(uri)
db = cliente["bus"]

bdAPI = APIRouter()

"""def get_BD():
    # Nos conectamos a la BD
    uri = os.getenv('PY_URI')
    cliente = pymongo.MongoClient(uri)
    return cliente.bus"""

""" Buses """
def get_Buses_con_Hora_minima(hora_minima, codigo_linea):
    global db
    cursor = db.ubicacion.find({"fecha_actualizacion": { "$gte": hora_minima }, "codigo_linea": codigo_linea}, sort=[("fecha_actualizacion", pymongo.DESCENDING)])
    return AUX.simplificar_datos(cursor)

def get_Buses_con_Intervalo_y_codigo_bus_Sin_Posicionar(hora_minima, hora_maxima, codigo_linea):
    global db
    cursor = db.ubicacion.find({
        "$and": [
            {"codigo_linea": codigo_linea},
            {"codigo_proxima_parada": { "$exists": False }},
            {"$or": [
                {"fecha_actualizacion": {"$gte": hora_minima, "$lt": hora_maxima}},
                {"last_update": {"$gte": hora_minima, "$lt": hora_maxima}}
            ]}
        ]
    }).sort([("fecha_actualizacion", pymongo.ASCENDING), ("last_update", pymongo.ASCENDING)])
    return AUX.simplificar_datos(cursor)

def get_Buses_con_Intervalo_y_codigo_bus(hora_minima, hora_maxima, codigo_linea):
    global db
    cursor = db.ubicacion.find({
        "$and": [
            {"codigo_linea": codigo_linea},
            {"$or": [
                {"fecha_actualizacion": {"$gte": hora_minima, "$lt": hora_maxima}},
                {"last_update": {"$gte": hora_minima, "$lt": hora_maxima}}
            ]}
        ]
    }).sort([("fecha_actualizacion", pymongo.ASCENDING), ("last_update", pymongo.ASCENDING)])
    return AUX.simplificar_datos(cursor)

def get_Buses_con_Intervalo_y_codigo_bus_Posicionados(hora_minima, hora_maxima, codigo_linea):
    global db
    cursor = db.ubicacion.find({
        "$and": [
            {"codigo_linea": codigo_linea},
            {"codigo_proxima_parada": { "$exists": True }},
            {"$or": [
                {"fecha_actualizacion": {"$gte": hora_minima, "$lt": hora_maxima}},
                {"last_update": {"$gte": hora_minima, "$lt": hora_maxima}}
            ]}
        ]
    }).sort([("fecha_actualizacion", pymongo.ASCENDING), ("last_update", pymongo.ASCENDING)])
    return AUX.simplificar_datos(cursor)

def get_Buses_cercanos_Hora(codigo_linea, codigo_bus, fecha_pred_baja, fecha_pred_alta):
    global db
    cursor = db.ubicacion.find(
        {
            "codigo_linea": codigo_linea,
            "codigo_bus": codigo_bus,
            "codigo_proxima_parada": { "$exists": True },
            "fecha_actualizacion": {"$gte": fecha_pred_baja, "$lt": fecha_pred_alta}       
        }, sort=[("fecha_actualizacion", pymongo.ASCENDING)])
    return AUX.simplificar_datos(cursor)

def get_Ultimo_Log_con_Datos():
    global db
    cursor = db.ubicacion_logs.find_one({"cantidad": {"$gte": 0}}, sort=[("fecha", pymongo.DESCENDING)])
    return AUX.simplificar_datos(cursor)

def set_Buses(estado_datos, nuevos_buses, bus_recoleccion):
    global db
    if estado_datos:
        db.ubicacion.insert_many(nuevos_buses)
        db.ubicacion_logs.insert_one(bus_recoleccion)
    else:
        db.ubitest.insert_many(nuevos_buses)
        db.ubitest_logs.insert_one(bus_recoleccion)

    return "Ok"

""" Formas """
def get_Formas():
    global db
    cursor = db.formas.find({}, sort=[("fecha_actualizacion", pymongo.DESCENDING)])
    return AUX.simplificar_datos(cursor)

def get_Forma_mas_reciente_Filtrada(codigo_linea):
    global db
    cursor = db.formas.find_one({"codigo_linea": codigo_linea}, sort=[("fecha_actualizacion", pymongo.DESCENDING)])
    return [AUX.simplificar_datos(cursor)]

def set_Forma(forma_JSON):
    global db
    db.formas.insert_one(forma_JSON)
    return "Ok"

""" Lineas """
def get_Linea_mas_reciente(codigo_linea):
    global db
    cursor = db.lineas.find_one({"codigo_linea": codigo_linea}, sort=[("fecha_actualizacion", pymongo.DESCENDING)])
    return [AUX.simplificar_datos(cursor)]

""" Lineas """
def get_Lineas_disponibles():
    global db
    cursor = db.lineas.find(sort=[("codigo_linea", pymongo.ASCENDING)]).distinct("codigo_linea")
    return AUX.parse_json(cursor)

def set_Linea(linea_JSON):
    global db
    db.lineas.insert_one(linea_JSON)
    return "Ok"

""" Tiempos // Datos """
def set_Datos(datos, codigo_linea, fecha_datos):
    global db
    operaciones_en_masa = []
    for codigo_parada, dato in datos.items():
        filtro = {
            "codigo_parada": codigo_parada, 
            "codigo_linea": codigo_linea, 
            "fecha_datos": fecha_datos
        }
        operacion = pymongo.ReplaceOne(filtro, dato, upsert=True)
        operaciones_en_masa.append(operacion)
    result = db.datosPool.bulk_write(operaciones_en_masa)
    return result


def set_Mapa_Tiempos(fecha_inicio, codigo_linea, codigo_bus, mapa_tiempos):
    global db
    cursor = db.mapasTiempos.replace_one({
        "fecha_inicio": fecha_inicio, 
        "codigo_linea": codigo_linea, 
        "codigo_bus": codigo_bus},
        mapa_tiempos, 
        upsert=True) # a False no updatea datos
    return cursor


def get_Un_Dato_Cualquiera(codigo_linea, dia_semana, hora_inicial):
    global db
    cursor = db.datosPool.find_one(
        {
            "codigo_linea": codigo_linea,
            "dia_semana": dia_semana,
            "hora_inicial": hora_inicial
        }) 
    return AUX.simplificar_datos(cursor)


def get_Datos_Parada_Todas(codigo_linea, fecha_datos_inicial, fecha_limite):
    global db
    cursor = db.datosPool.find({
        "codigo_linea": codigo_linea,
        "dia_semana": fecha_datos_inicial.weekday(),
        "hora_inicial": fecha_datos_inicial.hour,
        "fecha_datos": {"$gte": fecha_limite}
    }).sort([("fecha_datos", pymongo.ASCENDING)]).limit(10000)
    return AUX.simplificar_datos(cursor)

def get_Datos_Parada_por_Fechas(codigo_linea, fecha_datos):
    global db
    cursor = db.datosPool.find({
        "codigo_linea": codigo_linea,
                "$or": [
            {"fecha_datos": {"$gte": fecha_datos - AUX.timedelta(hours=0), "$lt": fecha_datos + AUX.timedelta(hours=23)}},
            #{"dia_semana": 5}, # Tarda
            #{"dia_semana": 6} # tarda
        ]
    }).sort([("fecha_datos", pymongo.ASCENDING)]).limit(10000)
    return AUX.simplificar_datos(cursor)


def get_Datos_Parada_por_Fechas_Inverso(codigo_linea, fecha_datos):
    global db
    cursor = db.datosPool.find({
        "codigo_linea": codigo_linea,
                "$nor": [
            {"fecha_datos": {"$gte": fecha_datos - AUX.timedelta(hours=0), "$lt": fecha_datos + AUX.timedelta(hours=23)}},
            {"dia_semana": 5},
            {"dia_semana": 6}
        ]
    }).sort([("fecha_datos", pymongo.ASCENDING)]).limit(10000)
    return AUX.simplificar_datos(cursor)

def get_Linea_Analizada(codigo_linea, dia_semana, hora_inicial):
    global db
    cursor = db.lineasAnalizadas.find_one({
        "codigo_linea": codigo_linea,
        "dia_semana": dia_semana,
        "hora_inicial": hora_inicial,
        }) 
    return AUX.simplificar_datos(cursor)

def set_Linea_Analizada(linea_Analizada):
    global db
    cursor = db.lineasAnalizadas.replace_one({
        "codigo_linea": linea_Analizada["codigo_linea"],  
        "dia_semana": linea_Analizada["dia_semana"], 
        "hora_inicial": linea_Analizada["hora_inicial"], 
        },
        linea_Analizada, 
        upsert=True)
    return cursor


def set_Datos_Old(dato_analizado_json):
    global db
    if db.datos.find_one({"fecha_datos": dato_analizado_json["fecha_datos"]}) is None:
        cursor = db.datos.insert_one(dato_analizado_json)
    else:
        cursor = db.datos.replace_one({"fecha_datos": dato_analizado_json["fecha_datos"]}, dato_analizado_json)

    # Si arreglo update_one con upsert=True no tengo que usar esta chapuza
    return cursor
