from datetime import datetime, timedelta
from bson import json_util
import json
from haversine import haversine, Unit
import pytz
import requests
from math import sqrt

# Franja Horaria de Málaga, Deta Space está en otra franja
franja_horaria_malaga = pytz.timezone("Europe/Madrid")
tzinfo = pytz.utc

author = "Daniel Roura Sepúlveda"

# Transforma el json en diccionario
def parse_json(data):
    return json.loads(json_util.dumps(data))


def limpiar_datos(dato):
    del dato["_id"]
    if "fecha_actualizacion" in dato:
        try:
            dato["fecha_actualizacion"] = dato["fecha_actualizacion"]["$date"]
        except:
            pass
    elif "last_update" in dato:
        try:
            dato["last_update"] = dato["last_update"]["$date"]
        except:
            pass
    return dato


def simplificar_datos(datos):
    datos = parse_json(datos)
    if isinstance(datos, dict):  # datos corresponden a un solo elemento (¿línea, forma?)
        datos = limpiar_datos(datos)
    elif isinstance(datos, list):  # datos corresponden a una lista (de buses)
        for dato in datos:
            dato = limpiar_datos(dato)
    return datos


def simplificar_formas(datos):
    datos = parse_json(datos)
    del datos["_id"]
    datos["fecha_actualizacion"] = datos["fecha_actualizacion"]["$date"]
    return datos


def valorValido(valor, min, max):
    return valor >= min and valor <= max


""" ----------------------------------- TIEMPOS ----------------------------------- """
""" Para el get_Buses_Filtrados: coge los buses con la fecha más reciente """


def formalizar_Tiempo_Segundos(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60
    # return f"{horas:02d}h:{minutos:02d}m:{segundos:02d}s"
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def formalizar_Tiempo_Medio_Parada(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60
    if horas > 0:
        # return f"{horas:02d}h:{minutos:02d}m:{segundos:02d}s"
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    else:
        # return f"{minutos:02d}m:{segundos:02d}s"
        return f"{minutos:02d}:{segundos:02d}"


def ultimo_dia(hoy, dia_semana):
    intervalo = dia_semana - hoy.weekday()
    if intervalo >= 0:
        # Si dia_semana es mayor al día de hoy, tenemos
        # que buscar el día_semana de la semana pasada
        intervalo -= 7

    return hoy + timedelta(intervalo)


def get_Fecha_actual():
    return datetime.now(franja_horaria_malaga)

def get_Fecha_actual_sin_Zona_Horaria():
    return datetime.now()


""" Calcula el tiempo en segundos entre dos strings de datetimes """
def calcular_Tiempo_Segundos(str_hora_1, str_hora_2):
    hora_1 = transformar_String_a_Datetime_generico(str_hora_1)
    hora_2 = transformar_String_a_Datetime_generico(str_hora_2)
    tiempo_seg = (hora_2 - hora_1).total_seconds()
    return tiempo_seg

def calcular_Tiempo_Segundos_Datetime(hora_1, hora_2):
    tiempo_seg = (hora_2 - hora_1).total_seconds()
    return tiempo_seg

def sumar_Tiempo_Datetime_Segundos(str_fecha_inicial, segundos):
    fecha_inicial = transformar_String_a_Datetime_generico(str_fecha_inicial)
    return fecha_inicial + timedelta(seconds=segundos)

def sumar_Tiempo_Segundos(fecha_inicial, segundos):
    return fecha_inicial + timedelta(seconds=segundos)

def construir_Intervalo_Minutos(fecha_inicial, intervalo_minutos):
    return fecha_inicial - timedelta(minutes=intervalo_minutos), fecha_inicial + timedelta(minutes=intervalo_minutos)
    
def transformar_String_a_DateTime(str_fecha):
    return datetime.strptime(str_fecha, "%Y-%m-%dT%H:%M:%SZ")

def transformar_String_Prediccion_a_DateTime(str_fecha):
    return datetime.strptime(str_fecha, "%Y-%m-%dT%H:%M:%S")

def transformar_String_a_Datetime_generico(str_fecha):
    # formatos = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", '%Y-%m-%dT%H:%M:%S.%fZ']
    formatos = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", '%Y-%m-%dT%H:%M:%S.%fZ', "%Y-%m-%dT%H:%M:%S.%f"]
    for formato in formatos:
        try:
            fecha = datetime.strptime(str_fecha, formato)
            return fecha
        except ValueError:
            pass
    raise ValueError("Formato de fecha no reconocido: {}".format(str_fecha))

def es_Fecha_Antigua_Dias(fecha, dias):
    return fecha < get_Fecha_actual_sin_Zona_Horaria() - timedelta(days=dias)

def es_Fecha_Antigua_Segundos(fecha, segundos):
    return fecha < get_Fecha_actual_sin_Zona_Horaria() - timedelta(seconds=segundos)

def timestamp(fecha):
    return fecha.timestamp()

def from_timestamp(fecha_timestamp):
    return datetime.fromtimestamp(fecha_timestamp)

""" -----------------------------------  ----------------------------------- """


def filtrar_Buses_mas_recientes(buses):
    buses_filtrados = []

    fecha_bus_mas_reciente = buses[0]["fecha_actualizacion"]

    for bus in buses:
        fecha_bus = bus["fecha_actualizacion"]
        if fecha_bus == fecha_bus_mas_reciente:
            buses_filtrados.append(bus)

    return buses_filtrados


def get_datos(url):
    data = []
    try:
        response = requests.get(url)
        data = response.text
    except:
        print(f"Error al realizar el request: " + url)

    return data


""" Cálculos de distancias """
# Distancia más precisa
def calcular_Distancia_Haversine(coordenada_1, coordenada_2):
    distancia = haversine(coordenada_1, coordenada_2, Unit.METERS)
    return distancia

# Una distancia menos precisa pero más rápida que Haversine
def calcular_Distancia_Euclidea(coordenada_1, coordenada_2):
    x1, y1 = coordenada_1
    x2, y2 = coordenada_2
    distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2) * 100000  # da Km así que lo pongo en metros
    return distancia


""" Extrae el índice del segmento_mas_cercano del bus """
def extraer_Indice_Segmento_cercano_Bus(bus, segmentos):
    segmento = bus["segmento_mas_cercano"]
    indice_segmento = segmentos.index(segmento)
    return indice_segmento


""" Extrae el índice de la parada con su código """
def extraer_Indice_Parada(codigo_parada, paradas):
    for indice in range(len(paradas)):
        if paradas[indice]["codigo_parada"] == codigo_parada:
            return indice
    return -1


def extraer_Indice_Segmento_con_Orden(orden, sentido, segmentos):
    for indice in range(len(segmentos)):
        if segmentos[indice]["orden"] == orden and segmentos[indice]["sentido"] == sentido:
            return indice
    return -1


""" Getters con Órdenes """
def get_Segmento_con_Orden(orden, sentido, segmentos):
    for segmento in segmentos:
        if segmento["orden"] == orden and segmento["sentido"] == sentido:
            return segmento
    return None


def get_Parada_con_Codigo(codigo_parada, paradas):
    for parada in paradas:
        if parada["codigo_parada"] == codigo_parada:
            return parada
    return None


def get_Parada_con_Orden(orden, sentido, paradas):
    for parada in paradas:
        if parada["orden"] == orden and parada["sentido"] == sentido:
            return parada
    return None


def get_Parada_con_Orden_sin_Sentido(orden, paradas):
    for parada in paradas:
        if parada["orden"] == orden:
            return parada
    return None


def get_Orden_Parada_con_Seg(seg):
    if "orden_proxima_parada" in seg:
        return seg["orden_proxima_parada"]
    else:
        return seg["orden_parada"]


def calcular_Distancia_entre_Segmentos(orden_inicial, orden_final, sentido, segmentos):
    distancia = 0
    len_segmentos = len(segmentos)
    i = extraer_Indice_Segmento_con_Orden(orden_inicial, sentido, segmentos)

    while i < len_segmentos + i:
        seg_actual = segmentos[i % len_segmentos]

        if seg_actual["orden"] == orden_final:
            return distancia
        else:
            distancia += seg_actual["distancia"]

        i += 1

    return -1


""" Tomando dos órdenes y el sentido del primer segmento traza un camino entre ambos empezando por el primero """
def get_Camino_entre_Segmentos(orden_inicial, orden_final, sentido_inicial, segmentos):
    camino_segmentos = []
    i = extraer_Indice_Segmento_con_Orden(
        orden_inicial, sentido_inicial, segmentos)

    while i < len(segmentos) + i:
        seg_actual = segmentos[i % len(segmentos)]

        if seg_actual["orden"] == orden_final:
            # Quizás tenga que añadie el último segmento pero el camino entre dos segmentos debe ser []
            break
        else:
            camino_segmentos.append(seg_actual)

        i += 1

    return camino_segmentos


# Tomando un camino de segmentos y devuelve: DISTANCIA, ORDENES_SEGMENTO
def get_Atributos_Camino(camino_segmentos):
    ordenes_segmentos = []
    distancia_proxima_parada = 0

    for segmento in camino_segmentos:
        ordenes_segmentos.append(segmento["orden"])
        distancia_proxima_parada += segmento["distancia"]

    return distancia_proxima_parada, ordenes_segmentos


def crear_Diccionario_Orden_Parada(paradas):
    dict_paradas = {}

    for parada in paradas:
        dict_paradas[int(parada["orden"])] = parada["codigo_parada"]
    pass
    return dict_paradas


""" --------------------------------------------------- """
# Dada la lista de segmentos y las coordenadas de un objeto, busca el segmento más cercano
def buscar_Segmento_Cercano(sentido, segmentos, coordanas_objeto):
    distancia_minima = float("inf")
    segmento_mas_cercano = None

    for segmento in segmentos:
        if (segmento["sentido"] == sentido):
            lat_s = float(segmento['latitud_1'])
            lon_s = float(segmento['longitud_1'])

            distancia_objeto_segmento = calcular_Distancia_Euclidea(
                coordanas_objeto, (lat_s, lon_s))

            if distancia_objeto_segmento <= distancia_minima:
                distancia_minima = distancia_objeto_segmento
                segmento_mas_cercano = segmento
            pass
        pass
    pass

    return segmento_mas_cercano, distancia_minima