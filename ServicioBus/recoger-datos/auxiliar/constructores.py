author = "Daniel Roura Sepúlveda"

""" Constructores JSON """
def construir_Parada_JSON(codigo_parada, codigo_linea, nombre_parada, orden, sentido, latitud, longitud):
    parada_JSON = {
        "codigo_parada": codigo_parada,
        "codigo_linea": codigo_linea,
        "nombre_parada": nombre_parada,
        "orden": orden,
        "sentido": sentido,
        "latitud": latitud,
        "longitud": longitud,
    }

    return parada_JSON

def construir_Linea_JSON(codigo_linea, nombre_linea, cabecera_Ida, cabecera_vuelta, paradas, fecha_actualizacion):
    linea_JSON = {
        "codigo_linea": codigo_linea,
        "nombre_linea": nombre_linea,
        "cabecera_Ida": cabecera_Ida,
        "cabecera_vuelta": cabecera_vuelta,
        "fecha_actualizacion": fecha_actualizacion,
        "paradas": paradas
    }

    return linea_JSON

def construir_Segmento_JSON(orden, sentido, latitud_1, longitud_1, latitud_2, longitud_2, distancia):
    segmento_json = {
        "orden": orden,
        "sentido": sentido,
        "latitud_1": latitud_1,
        "latitud_2": latitud_2,
        "longitud_1": longitud_1,
        "longitud_2": longitud_2,
        "distancia": distancia
    }
    if (segmento_json["distancia"] == 0):
        return None
    # Euclídea dice que son 27.026m entre todos los segmentos, Haversine opina que 24.759m, la real es mucho más parecida a Haversine
    return segmento_json

def construir_Forma_Ida_Vuelta_JSON(sentido, latitud, longitud, orden):
    forma_ida_json = {
        "sentido": sentido,
        "latitud": latitud,
        "longitud": longitud,
        "orden": orden
    }
    return forma_ida_json


def construir_Forma_JSON(linea_filtrada, segmentos, fecha_actualizacion):
    formas_linea_json = {
        "codigo_linea": linea_filtrada,
        "fecha_actualizacion": fecha_actualizacion,
        "segmentos": segmentos
    }
    return formas_linea_json

def construir_Datos_JSON(media_aritmetica, desviacion_tipica, codigo_linea, dia_semana, hora_inicial, fecha_datos, fecha_actualizacion):
    datos_analizados_json = {
        "media_aritmetica": media_aritmetica,
        "desviacion_tipica": desviacion_tipica,
        "codigo_linea": codigo_linea,
        "dia_semana": dia_semana,
        "hora_inicial": hora_inicial,
        "fecha_datos": fecha_datos,
        "fecha_actualizacion": fecha_actualizacion
    }
    return datos_analizados_json

def construir_Bus_JSON(codigo_bus, codigo_linea, sentido, latitud, 
                       longitud, codigo_parada_inicial, fecha_actualizacion):
    bus_JSON = {
        "codigo_bus": codigo_bus,
        "codigo_linea": codigo_linea,
        "sentido": sentido,
        "latitud": latitud,
        "longitud": longitud,
        "codigo_parada_inicial": codigo_parada_inicial,
        # "last_update": fecha_actualizacion,
        "fecha_actualizacion": fecha_actualizacion
    }
    return bus_JSON

def construir_Bus_recoleccion_JSON(cantidad_buses, fecha, origen):
    bus_recoleccion_JSON = {
        "cantidad": cantidad_buses,
        "fecha": fecha,
        "origen": origen,
    }
    return bus_recoleccion_JSON