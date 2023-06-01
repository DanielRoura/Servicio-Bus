author = "Daniel Roura Sepúlveda"

from datetime import timedelta, datetime
import auxiliar.auxiliar as AUX
import auxiliar.BD as BD
from statistics import mean, stdev
from scipy.interpolate import interp1d
import numpy as np

""" Llamado por set_datos para dividir las distancias recorridas en tiempos en cada parada """
def crear_Diccionario_Pares_Buses_y_Paradas(buses, segmentos, paradas, datosUtiles):
    dict_paradas = AUX.crear_Diccionario_Orden_Parada(paradas)
    dict_buses = crear_Diccionario_Segmentos_con_Buses(
        buses, paradas, segmentos)
    dict_buses = crear_Diccionario_Buses_Pares(dict_buses, segmentos)
    dict_buses = unir_Diccionario_Paradas_JSON(
        dict_buses, dict_paradas, datosUtiles)
    return dict_buses


def crear_Diccionario_Segmentos_con_Buses(buses, paradas, segmentos):
    dict_buses_seg = {}

    for bus in buses:
        codigo_bus = bus["codigo_bus"]

        # Si el código del bus del bus actual no está en el diccionario...
        if dict_buses_seg.get(codigo_bus) == None:
            # Lo añadimos
            dict_buses_seg[codigo_bus] = []
        pass

        # valores = ((bus.get("latitud"), bus.get("longitud")), (bus.get("last_update").minute * 60 + bus.get("last_update").second), bus.get("sentido"))
        if "fecha_actualizacion" in bus:
            fecha_actualizacion = bus["fecha_actualizacion"]
        else:
            fecha_actualizacion = bus["last_update"]

        sentido = bus["sentido"]

        if len(bus["ordenes_segmentos"]) == 0:
            orden_segmento = AUX.get_Parada_con_Codigo(
                bus["codigo_proxima_parada"], paradas)["orden_segmento"]
        else:
            orden_segmento = bus["ordenes_segmentos"][0]

        seg = AUX.get_Segmento_con_Orden(orden_segmento, sentido, segmentos)

        seg_aux = {
            "fecha_actualizacion": fecha_actualizacion,
            "sentido": sentido,
            "orden_segmento": orden_segmento,
            "orden_parada_cercana": AUX.get_Orden_Parada_con_Seg(seg)
        }

        dict_buses_seg[codigo_bus].append(seg_aux)
    pass

    return dict_buses_seg


def crear_Diccionario_Buses_Pares(dict_buses, segmentos):
    dict_buses_pares = {}

    for codigo_bus in dict_buses:
        lista_buses = dict_buses[codigo_bus]

        # Lista de pares
        pares = []

        # Creamos los pares de elementos adyacentes
        for j in range(0, len(lista_buses) - 1):
            # par = [lista_buses[j], lista_buses[j+1]]
            dato_seg_1 = lista_buses[j]
            dato_seg_2 = lista_buses[j+1]

            tiempo_transcurrido = AUX.calcular_Tiempo_Segundos(
                dato_seg_1["fecha_actualizacion"], dato_seg_2["fecha_actualizacion"])

            if tiempo_transcurrido > 0 and tiempo_transcurrido < 180:
                distancia_recorrida = AUX.calcular_Distancia_entre_Segmentos(
                    dato_seg_1["orden_segmento"], dato_seg_2["orden_segmento"], lista_buses[j]["sentido"], segmentos)

                if distancia_recorrida >= 0:
                    ordenes_segmentos = [
                        dato_seg_1["orden_segmento"], dato_seg_2["orden_segmento"]]
                    sentidos_segmentos = [
                        dato_seg_1["sentido"], dato_seg_2["sentido"]]

                    ordenes_paradas = [
                        dato_seg_1["orden_parada_cercana"], dato_seg_2["orden_parada_cercana"]]

                    # if (orden_p2 > orden_p1 and seg_1["sentido"] == seg_2["sentido"]):
                    # break

                    par_JSON = {
                        "fecha_inicio": dato_seg_1["fecha_actualizacion"],
                        "tiempo_transcurrido": tiempo_transcurrido,
                        "distancia_recorrida": distancia_recorrida,
                        "ordenes_segmentos": ordenes_segmentos,
                        "sentidos_segmentos": sentidos_segmentos,
                        "ordenes_paradas": ordenes_paradas
                    }

                    pares.append(par_JSON)
                pass
            pass
        pass

        dict_buses_pares[codigo_bus] = pares
    pass

    return dict_buses_pares


def unir_Diccionario_Paradas_JSON(dict_buses, dict_paradas, datosUtiles):
    dict_datos_paradas = {}

    for codigo_bus in dict_buses:
        lista_pares = dict_buses[codigo_bus]

        pares_parados_consecutivos = []
        fecha_parada = None

        # Creamos los pares de elementos adyacentes
        for par in lista_pares:
            dato_JSON = {
                "fecha_inicio": par["fecha_inicio"],
                "tiempo_transcurrido": par["tiempo_transcurrido"],
                "distancia_recorrida": par["distancia_recorrida"],
                # "sentido": par["sentidos_segmentos"][0],
                # "orden_segmento": par["ordenes_segmentos"][0],
            }

            codigo_parada_1 = dict_paradas[par["ordenes_paradas"][0]]
            dict_datos_paradas, pares_parados_consecutivos, fecha_parada = unir_Dato_Par_Codigo_JSON(
                codigo_parada_1, dato_JSON, dict_datos_paradas, datosUtiles, pares_parados_consecutivos, fecha_parada)

            """ - ANALIZAR - """
            if par["ordenes_paradas"][0] != par["ordenes_paradas"][1]:
                codigo_parada_2 = dict_paradas[par["ordenes_paradas"][1]]
                dict_datos_paradas, pares_parados_consecutivos, fecha_parada = unir_Dato_Par_Codigo_JSON(
                    codigo_parada_2, dato_JSON, dict_datos_paradas, datosUtiles, pares_parados_consecutivos, fecha_parada)
            pass
        pass
    pass

    return dict_datos_paradas


def unir_Dato_Par_Codigo_JSON(codigo_parada, par, dict_datos_paradas, datosUtiles, pares_parados_consecutivos, fecha_parada):
    grupo_datos_JSON = dict_datos_paradas.get(codigo_parada)

    if grupo_datos_JSON == None:
        grupo_datos_JSON = {
            "codigo_parada": codigo_parada,
            "codigo_linea": datosUtiles[0],
            "fecha_datos": datosUtiles[1],
            "fecha_actualizacion": datosUtiles[3],
            "dia_semana": datosUtiles[1].weekday(),
            "hora_inicial": datosUtiles[1].hour,
            "duracion_minutos": datosUtiles[2],
            "cantidad_datos": 1,
            "cantidad_datos_parados": 1 if par["distancia_recorrida"] == 0 else 0,
            "lista_datos": [par],
            # "tiempos_parados": [], # Útil para calcular la duración de los parados
            "fechas_paradas": []
            # -------------------------------- ESTO NO ME DICE CUántas veces pasa por la parada --> Arreglar
        }
        dict_datos_paradas[codigo_parada] = (grupo_datos_JSON)

    else:
        grupo_datos_JSON["cantidad_datos"] = grupo_datos_JSON["cantidad_datos"] + 1

        # Apuntar los tiempos en los que el bus estuvo en parada (pueden ser menores a ese tiempo)
        if par["distancia_recorrida"] == 0 and fecha_parada == None:
            fecha_parada = par["fecha_inicio"]
        elif par["distancia_recorrida"] > 0 and fecha_parada != None:
            grupo_datos_JSON["fechas_paradas"].append(
                [fecha_parada, par["fecha_inicio"]])
            fecha_parada = None

        if par["distancia_recorrida"] == 0:
            grupo_datos_JSON["cantidad_datos_parados"] = grupo_datos_JSON["cantidad_datos_parados"] + 1
            # pares_parados_consecutivos.append(par["tiempo_transcurrido"])
        # elif len(pares_parados_consecutivos) > 0:
            # grupo_datos_JSON["tiempos_parados"].append(pares_parados_consecutivos)
            # pares_parados_consecutivos = []

        lista_datos = grupo_datos_JSON["lista_datos"]
        lista_datos.append(par)
        # grupo_datos_JSON["lista_datos"] = lista_datos

    return dict_datos_paradas, pares_parados_consecutivos, fecha_parada


def analizar_Datos(lista_datos, cantidad_datos):
    distancias = [dato["distancia_recorrida"] for dato in lista_datos]
    tiempos = [dato["tiempo_transcurrido"] for dato in lista_datos]

    media_aritmetica = mean(distancias[i]/tiempos[i]
                            for i in range(len(lista_datos)))
    desviacion_tipica = stdev(distancias[i]/tiempos[i]
                              for i in range(len(lista_datos)))

    return round(media_aritmetica, 1), round(desviacion_tipica, 1)


def analizar_Tiempos_Paradas(cantidad_datos_parados, cantidad_datos, fechas_paradas):
    # print([cantidad_datos_parados, cantidad_datos, len(fechas_paradas)])
    if cantidad_datos_parados == 0:
        proporcion_en_parada = 0
        tiempo_medio_parada = 0

    else:
        tiempo_medio_parada = 0

        for fecha_parada in fechas_paradas:
            tiempo_medio_parada += (AUX.transformar_String_a_DateTime(
                fecha_parada[1]) - AUX.transformar_String_a_DateTime(fecha_parada[0])).total_seconds()

        tiempo_medio_parada /= cantidad_datos_parados
        tiempo_medio_parada = int(tiempo_medio_parada)

        proporcion_en_parada = round(
            cantidad_datos_parados / cantidad_datos * 100, 2)

    tiempos_paradas = {
        "proporcion_en_parada": proporcion_en_parada,
        "tiempo_medio_parada": tiempo_medio_parada,
        "str_tiempo_medio_parada": AUX.formalizar_Tiempo_Medio_Parada(tiempo_medio_parada) if tiempo_medio_parada != 0 else "< 1 min"
    }

    return tiempos_paradas


""" Añade los datos de la parada a la propia parada y al bus """
def set_Velocidades_Parada(parada, media_a, desv_tipica, datos_paradas):
    parada["velocidad_media_aritmetica"] = media_a
    parada["velocidad_desviacion_tipica"] = desv_tipica
    parada["tiempo_medio_parada"] = datos_paradas["tiempo_medio_parada"]
    parada["str_tiempo_medio_parada"] = datos_paradas["str_tiempo_medio_parada"]
    parada["proporcion_en_parada"] = datos_paradas["proporcion_en_parada"]
    parada["tiempo_proxima_parada"] = round(parada["distancia_proxima_parada"] / parada["velocidad_media_aritmetica"], 1)
    parada["distancia_proxima_parada"] = round(parada["distancia_proxima_parada"], 2)

    # --------------------------------------------------------------------------------------------------------------------------
    parada["error"] = None
    parada["tendencia"] = None
    parada["diferencia_prediccion"] = None

    return parada


def analizar_Tiempos_Linea(linea_Analizada):
    for parada in linea_Analizada["paradas"]:
        tiempo_proxima_parada = int(
            parada["distancia_proxima_parada"] / parada["velocidad_media_aritmetica"])
        parada["tiempo_proxima_parada"] = tiempo_proxima_parada

    return linea_Analizada


def construir_Mapa_Tiempos(bus, linea_Analizada):
    paradas = linea_Analizada["paradas"]
    len_paradas = len(paradas)
    fecha_actualizacion = bus["fecha_actualizacion"]
    paradas_ordenadas = []

    parada_actual = AUX.get_Parada_con_Codigo(bus["codigo_proxima_parada"], paradas)

    tiempo_acumulado = int(bus["distancia_proxima_parada"] / parada_actual["velocidad_media_aritmetica"])
    parada_actual = actualizar_Parada_en_Mapa_Tiempos(parada_actual, tiempo_acumulado, fecha_actualizacion)

    if tiempo_acumulado == 0 and parada_actual["fecha_llegada_real"] == None:
        parada_actual["fecha_llegada_real"] = parada_actual["fecha_llegada"]

    paradas_ordenadas.append(parada_actual)

    orden_inicial = parada_actual["orden"]

    NUM_MAX_PARADAS = 15
    num_paradas = 0

    for orden in range(orden_inicial + 1, len_paradas + orden_inicial):
        orden_actual = orden if orden <= len_paradas else orden % len_paradas
        parada_actual = AUX.get_Parada_con_Orden_sin_Sentido(orden_actual, paradas)
        
        tiempo_acumulado += int(parada_actual["tiempo_proxima_parada"])
        parada_actual = actualizar_Parada_en_Mapa_Tiempos(
            parada_actual, tiempo_acumulado, fecha_actualizacion)
        paradas_ordenadas.append(parada_actual)

        num_paradas += 1
        if num_paradas == NUM_MAX_PARADAS:
            break
    pass

    linea_Analizada["paradas"] = paradas_ordenadas   
    linea_Analizada["fecha_actualizacion"] = fecha_actualizacion
    linea_Analizada["fecha_actualizacion_real"] = AUX.get_Fecha_actual()
    
    return linea_Analizada


def actualizar_Parada_en_Mapa_Tiempos(parada, tiempo_acumulado, fecha_actualizacion):
    parada["tiempo_acumulado"] = tiempo_acumulado
    parada["fecha_llegada"] = AUX.sumar_Tiempo_Datetime_Segundos(fecha_actualizacion, tiempo_acumulado)
    parada["fecha_llegada_real"] = None
    return parada


""" Tendencias """
def estudiar_Tendencia(linea_analizada, ultima_linea_analizada, codigo_parada_objetivo):
    for parada in linea_analizada["paradas"]:
        prediccion_anterior = AUX.get_Parada_con_Codigo(parada["codigo_parada"], ultima_linea_analizada["paradas"])

        if prediccion_anterior is not None:            
            fecha_p_ant = AUX.transformar_String_a_Datetime_generico(prediccion_anterior["fecha_llegada"])
            
            parada["fecha_llegada_anterior"] = prediccion_anterior["fecha_llegada"]

            
            fecha_p_new = parada["fecha_llegada"]
            
            diferencia_prediccion = AUX.calcular_Tiempo_Segundos_Datetime(fecha_p_new, fecha_p_ant)

            parada["diferencia_prediccion"] = diferencia_prediccion

            diferencia_anterior = prediccion_anterior["diferencia_prediccion"]
            if diferencia_anterior is not None:
                
                # print("Dif ant no nula", diferencia_anterior)
                
                tendencia = None
                if diferencia_prediccion < 0 and diferencia_prediccion < diferencia_anterior:
                    # Poner -1 y en el front se transforma en string -> Adelantando
                    tendencia = -1
                elif diferencia_prediccion > 0 and diferencia_prediccion > diferencia_anterior:
                    # Poner 1 y en el front se transforma en string -> Atrasando
                    tendencia = 1
                pass
                parada["tendencia"] = tendencia

            prediccion_anterior = None
        # if
    # for
    return linea_analizada


""" Cálculo de fecha_llegada_real """
def fusionar_Lineas_Analizadas(codigo_bus, linea_analizada, ultima_linea_analizada, segmentos):
    paradas = linea_analizada["paradas"]
    nuevas_paradas = []

    """ Quito el tiempo acumulado --> se ha pasado la parada """
    for parada_ant in ultima_linea_analizada["paradas"]:
        if AUX.get_Parada_con_Codigo(parada_ant["codigo_parada"], paradas) is None:
            parada_ant["tiempo_acumulado"] = None
            nuevas_paradas.append(parada_ant)

    linea_analizada["paradas"] = nuevas_paradas + paradas

    """ Calculo las fechas de llegadas """
    for parada in linea_analizada["paradas"]:
        if parada["tiempo_acumulado"] == None and parada["fecha_llegada_real"] == None:
            fecha_llegada_real = llamar_Fecha_llegada(linea_analizada["codigo_linea"], codigo_bus, parada, [linea_analizada["paradas"], segmentos])
            
            if fecha_llegada_real is not None:
                fecha_llegada_real = fecha_llegada_real.replace(microsecond=0)
                
                if parada["error"] is None:
                    parada["error"] = AUX.calcular_Tiempo_Segundos_Datetime(AUX.transformar_String_a_Datetime_generico(parada["fecha_llegada"]), fecha_llegada_real)
                    
            parada["fecha_llegada_real"] = fecha_llegada_real
                        
    return linea_analizada


""" Calcula la fecha de llegada más real posible de un bus a una parada """
def llamar_Fecha_llegada(codigo_linea, codigo_bus, parada_objetivo, paradas_y_segmentos):
    fecha_prediccion = AUX.transformar_String_Prediccion_a_DateTime(parada_objetivo["fecha_llegada"])
    fecha_pred_baja, fecha_pred_alta = AUX.construir_Intervalo_Minutos(fecha_prediccion, intervalo_minutos=5)
    buses_aproximados = BD.get_Buses_cercanos_Hora(codigo_linea, codigo_bus, fecha_pred_baja, fecha_pred_alta)

    if len(buses_aproximados) == 0:
        return None

    fecha_llegada = get_Fecha_llegada(parada_objetivo, buses_aproximados, paradas_y_segmentos[0], paradas_y_segmentos[1])
        
    if fecha_llegada == None:
        fecha_llegada = get_Fecha_llegada_interpolada(parada_objetivo, buses_aproximados, paradas_y_segmentos[0], paradas_y_segmentos[1])
        
    return fecha_llegada

def get_Fecha_llegada_interpolada(parada_objetivo, buses_aproximados, paradas, segmentos):
    try:
        fecha_llegada_inter = None
        """print("interpolar")"""
    
        codigo_parada_inicial = buses_aproximados[0]["codigo_proxima_parada"]
        codigo_parada_final = buses_aproximados[len(buses_aproximados)-1]["codigo_proxima_parada"]
            
        lista_paradas_intermedias = []
            
        for i in range(len(paradas)*2):
            parada = paradas[i % len(paradas)]
            
            if parada["codigo_parada"] == codigo_parada_inicial:
                lista_paradas_intermedias.append(parada)
            elif len(lista_paradas_intermedias) > 0 and parada["codigo_parada"] == codigo_parada_final:
                lista_paradas_intermedias.append(parada)
                break
            elif len(lista_paradas_intermedias) > 0:
                lista_paradas_intermedias.append(parada)
            
        lista_distancias = []
        lista_datetimes = []
        
        distancia_parada_objetivo = AUX.calcular_Distancia_entre_Segmentos(buses_aproximados[0]["orden_segmento"], 
                                                                        parada_objetivo["orden_segmento"], 
                                                                        buses_aproximados[0]["sentido"], 
                                                                        segmentos)
        """print("Dist: " + str(distancia_parada_objetivo))"""
        distancia_acumulada = 0
        for i in range(0, len(buses_aproximados) - 1):
            distancia_acumulada += AUX.calcular_Distancia_entre_Segmentos(buses_aproximados[i]["orden_segmento"],
                                                                        buses_aproximados[i+1]["orden_segmento"],
                                                                        buses_aproximados[i]["sentido"],
                                                                        segmentos)
            
            lista_distancias.append(distancia_acumulada)
            lista_datetimes.append(AUX.timestamp(AUX.transformar_String_a_Datetime_generico(buses_aproximados[i]["fecha_actualizacion"])))
        
        array_distancias = np.array(lista_distancias, dtype=float)
        array_datetimes = np.array(lista_datetimes, dtype=float)
        # array_velocidades = np.array(lista_velocidades, dtype=float)
            
        # Crear la función de interpolación
        funcion_interpolacion = interp1d(array_distancias, array_datetimes)
        valor_interpolado = int(funcion_interpolacion(distancia_parada_objetivo))

        fecha_llegada_inter = AUX.from_timestamp(valor_interpolado)
    
        return AUX.sumar_Tiempo_Segundos(fecha_llegada_inter, segundos=60)
    
    except:
        return None


def get_Fecha_llegada(parada_objetivo, buses_aproximados, paradas, segmentos):
    bus_llegando = None
    bus_saliendo = None
    bus_Aux = None

    for bus in buses_aproximados:
        if bus["codigo_proxima_parada"] == parada_objetivo["codigo_proxima_parada"]:
            bus_saliendo = bus
            bus_llegando = bus_Aux
            break
        else:
            bus_Aux = bus

    if bus_llegando is None or bus_saliendo is None:
        return None
    else:
        fecha_llegando = AUX.transformar_String_a_DateTime(
            bus_llegando["fecha_actualizacion"])
        fecha_saliendo = AUX.transformar_String_a_DateTime(
            bus_saliendo["fecha_actualizacion"])

        # Coger punto intermedio entre ambos buses
        if (len(bus_llegando["ordenes_segmentos"]) > 0):
            orden_segmento_llegando = bus_llegando["ordenes_segmentos"][0]
        else:
            orden_segmento_llegando = AUX.get_Parada_con_Codigo(
                bus_llegando["codigo_proxima_parada"], paradas)["orden_segmento"]

        if (len(bus_saliendo["ordenes_segmentos"]) > 0):
            orden_segmento_saliendo = bus_saliendo["ordenes_segmentos"][0]
        else:
            orden_segmento_saliendo = AUX.get_Parada_con_Codigo(
                bus_saliendo["codigo_proxima_parada"], paradas)["orden_segmento"]

        distancia_1 = AUX.calcular_Distancia_entre_Segmentos(
            orden_segmento_llegando, parada_objetivo["orden_segmento"], bus_llegando["sentido"], segmentos)
        distancia_2 = AUX.calcular_Distancia_entre_Segmentos(
            parada_objetivo["orden_segmento"], orden_segmento_saliendo, parada_objetivo["sentido"], segmentos)
        
        proporcion_recorrido = distancia_1 / (distancia_1 + distancia_2)
        tiempo_entre_buses = AUX.calcular_Tiempo_Segundos_Datetime(fecha_llegando, fecha_saliendo)
        
        # ----------------------------------------------------------------------------------------------------------------------------------------- #
        """tiempo_parada = parada_objetivo["tiempo_medio_parada"]
        
        if tiempo_entre_buses > tiempo_parada:
            # usar la velocidad a la baja o normal
            pass
        elif tiempo_entre_buses <= tiempo_parada:
            # usar velocidad a la alta
            pass"""
         
        fecha_llegada_Real = fecha_llegando + timedelta(seconds=(tiempo_entre_buses * proporcion_recorrido)) # + tiempo_parada

        return fecha_llegada_Real


def calcular_Distancias_entre_Buses(diccionario, segmentos):
    # diccionario_datos = {}
    lista_velocidades = []

    for codigo_bus in diccionario:
        lista_buses = diccionario[codigo_bus]
        lista_datos = []
        len_segmentos = len(segmentos)

        bus_actual = lista_buses[0]
        bus_anterior = None

        if (len(lista_buses) > 2):
            for indice_bus in range(1, len(lista_buses) - 1):
                bus_anterior = bus_actual
                bus_actual = lista_buses[indice_bus]

                """ Calcular tiempo """
                tiempo = AUX.calcular_Tiempo_Segundos(
                    bus_anterior["last_update"], bus_actual["last_update"])
                if tiempo == 0:
                    break

                """ Calcular distancia """
                indice_segmento_inicial = AUX.extraer_Indice_Segmento_cercano_Bus(
                    bus_anterior, segmentos)
                indice_segmento_final = AUX.extraer_Indice_Segmento_cercano_Bus(
                    bus_actual, segmentos)
                distancia = 0

                if (indice_segmento_inicial == indice_segmento_final + 1):
                    indice_aux = indice_segmento_final
                    indice_segmento_final = indice_segmento_inicial
                    indice_segmento_inicial = indice_aux

                for indice_segmento in range(indice_segmento_inicial, len_segmentos + indice_segmento_inicial):
                    if indice_segmento % len_segmentos == indice_segmento_final:
                        break
                    distancia += segmentos[indice_segmento %
                                           len_segmentos]["distancia"]
                    pass
                pass

                distancia = round(distancia, 2)

                """ Calcular velocidad """
                velocidad = round(distancia / tiempo, 2)
                lista_datos.append(velocidad)
                lista_velocidades.append(velocidad)

                indice_bus += 1
            pass
    pass

    return lista_velocidades

































""" ------------------------------------- """
""" Aquí compruebo que utilizar mi método daba el mismo resultado (el otro daba un minuto por debajo) y tardaba MENOS tiempo en ejecutarse """
def llamar_Fecha_llegadaOLD(codigo_linea, codigo_bus, parada_objetivo, paradas_y_segmentos):
    fecha_prediccion = AUX.transformar_String_Prediccion_a_DateTime(parada_objetivo["fecha_llegada"])
    fecha_pred_baja, fecha_pred_alta = AUX.construir_Intervalo_Minutos(fecha_prediccion, intervalo_minutos=5)
    buses_aproximados = BD.get_Buses_cercanos_Hora(codigo_linea, codigo_bus, fecha_pred_baja, fecha_pred_alta)

    if len(buses_aproximados) == 0:
        return None

    t1 = datetime.now()
    fecha_llegada = get_Fecha_llegada(parada_objetivo, buses_aproximados, paradas_y_segmentos[0], paradas_y_segmentos[1])
    t2 = datetime.now()
    tA = t2 - t1
      
    t1 = datetime.now()  
    fecha_llegada_interpolada = get_Fecha_llegada_interpolada(parada_objetivo, buses_aproximados, paradas_y_segmentos[0], paradas_y_segmentos[1])
    t2 = datetime.now()
    tB = t2 - t1
    
    print(fecha_llegada_interpolada) 
    print("---")
    print(fecha_llegada)
    print("++++")
    print(str(tA) + " -- " + str(tB))
    print()
    
    if fecha_llegada == None and False:
        print("- Fecha llegada NONE")
        print()
        print(codigo_linea)
        print()
        print(codigo_bus)
        print()
        print(parada_objetivo)
        print()
        print()
    
    return fecha_llegada