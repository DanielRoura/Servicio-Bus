author = "Daniel Roura Sepúlveda"

import auxiliar.BD as BD
import buses.funcionesBuses as FUNCBUSES
import lineas.lineas as LINEAS
import lineas.formas as FORMAS
import auxiliar.auxiliar as AUX
import datos.funcionesDatos as FUNCDATOS
import auxiliar.calendario as CALEND
#
from datetime import timedelta
from fastapi import APIRouter


datosAPI = APIRouter()

""" Get Datos Analizados para TODAS las paradas de una línea """
async def get_Datos_Parada_Todas(codigo_linea: int):
    NUM_SEMANAS = 8

    # hora_a = AUX.get_Fecha_actual()
    fecha_datos_inicial = AUX.get_Fecha_actual().replace(
        microsecond=0, second=0, minute=0)
    fecha_limite = fecha_datos_inicial - timedelta(weeks=NUM_SEMANAS, hours=1)

    lista_grupos_datos = BD.get_Datos_Parada_Todas(codigo_linea, fecha_datos_inicial, fecha_limite)

    # print((AUX.get_Fecha_actual() - hora_a).total_seconds())

    dict_datos = {}

    for grupo_datos_parada in lista_grupos_datos:
        codigo_parada = grupo_datos_parada["codigo_parada"]
        if codigo_parada not in dict_datos:
            dict_datos[codigo_parada] = []
        dict_datos[codigo_parada].append(grupo_datos_parada)

    dict_medias = {}

    for codigo_parada in dict_datos:
        datos = dict_datos[codigo_parada]

        lista_datos_completa = []
        cantidad_datos = 0
        cantidad_datos_parados = 0

        fechas_paradas = []

        for grupo_datos_parada in datos:
            lista_datos_completa.extend(grupo_datos_parada["lista_datos"])
            cantidad_datos += grupo_datos_parada["cantidad_datos"]
            cantidad_datos_parados += grupo_datos_parada["cantidad_datos_parados"]
            fechas_paradas.extend(grupo_datos_parada["fechas_paradas"])

        media_aritmetica, desviacion_tipica = FUNCDATOS.analizar_Datos(
            lista_datos_completa, cantidad_datos)
        tiempos_paradas = FUNCDATOS.analizar_Tiempos_Paradas(
            cantidad_datos_parados, cantidad_datos, fechas_paradas)

        dict_medias[codigo_parada] = {
            "media_aritmetica": media_aritmetica,
            "desviacion_tipica": desviacion_tipica,
            "cantidad_datos": cantidad_datos,
            "cantidad_datos_parados": cantidad_datos_parados,
            
            # Para calcular cuánto se tira parado un bus en una parada específica
            "datos_paradas": tiempos_paradas
        }

    return dict_medias


""" Cálculo y Set de datos analizados """
@datosAPI.post("/api/set_datos/{codigo_linea}/{hora_inicial}/{dia_semana}/{numero_semanas}", tags=["Datos"])
async def set_Datos_en_Masa(codigo_linea: int, hora_inicial: int, dia_semana: int, numero_semanas: int):
    if not (AUX.valorValido(hora_inicial, 6, 23) and AUX.valorValido(dia_semana, 0, 6) and AUX.valorValido(numero_semanas, 0, 8)):
        return {"message": "Fecha no válida"}
    
    fecha_actualizacion = AUX.get_Fecha_actual()
    fecha_datos = fecha_actualizacion.replace(
        microsecond=0, second=0, minute=0, hour=hora_inicial)

    forma_filtrada = (await FORMAS.get_Forma_Filtrada_Unica(codigo_linea))
    linea_filtrada = (await LINEAS.get_Linea_Filtrada_Unica(codigo_linea))

    if (forma_filtrada == None):
        return None

    # Último día que fue el mismo weekday que dia_semana
    ultimo_dia = AUX.ultimo_dia(fecha_datos, dia_semana)

    duracion_datos_minutos = 60

    semanaSanta = CALEND.get_Fecha_Semana_Santa()

    for i in range(0, numero_semanas):
        fecha_datos = ultimo_dia - timedelta(weeks=i)
        fecha_datos_max = fecha_datos + timedelta(minutes=duracion_datos_minutos)

        if (semanaSanta[0] <= fecha_datos <= semanaSanta[1]):
            print("set_Datos: Fecha no válida (Semana santa) : " + str(fecha_datos))
            continue
            
        buses_mezclados = BD.get_Buses_con_Intervalo_y_codigo_bus(fecha_datos, fecha_datos_max, codigo_linea)

        buses = FUNCBUSES.posicionar_Buses_Mezclados(buses_mezclados, forma_filtrada["segmentos"], linea_filtrada)

        if len(buses) <= 2:  # Al menos 2 buses que analizar
            print("set_Datos: Lista de buses vacía --> Error? len=" + str(len(buses)))
            continue
        
        print(fecha_datos, fecha_actualizacion)
        dict_datos = FUNCDATOS.crear_Diccionario_Pares_Buses_y_Paradas(buses, forma_filtrada["segmentos"], 
                                                                        linea_filtrada["paradas"], 
                                                                        [codigo_linea, fecha_datos, duracion_datos_minutos, fecha_actualizacion])

        if dict_datos == None or len(dict_datos.keys()) == 0:
            print("set_Datos: Lista de buses vacía --> Error?")
            continue         
        
        cursor = BD.set_Datos(dict_datos, codigo_linea, fecha_datos)

        if cursor == None:
            return {"message": "set_Datos: Error al insertar un dato: Linea: " + str(codigo_linea) + ", Fecha datos: " + str(fecha_datos)}
        else:
            print({"message": "set_Datos: Datos actualizados correctamente : " + str(codigo_linea) + ", Fecha datos: " + str(fecha_datos)})
    # for

    return {"message": "set_Datos: Datos insertados y actualizados en la BD con éxito"}


@datosAPI.post("/api/set_datos_ahora/{codigo_linea}", tags=["Datos"])
async def set_Datos_ahora(codigo_linea: int):
    fecha_datos = AUX.get_Fecha_actual()
    return await set_Datos_en_Masa(codigo_linea, fecha_datos.hour, fecha_datos.weekday(), numero_semanas=3) # 4 mejor


@datosAPI.post("/api/set_datos_hoy/{codigo_linea}", tags=["Datos"])
async def set_Datos_Hoy(codigo_linea: int):
    fecha_datos = AUX.get_Fecha_actual()
    respuestas = []
    for i in range(6, 25):
        respuestas.append(await set_Datos_en_Masa(codigo_linea, i, fecha_datos.weekday(), 2))

    return respuestas


@datosAPI.post("/api/set_datos_ultima_semana/{codigo_linea}", tags=["Datos"])
async def set_Datos_Hora_Dia_Semana(codigo_linea: int):
    respuestas = []
    for d in range(0, 7):
        for h in range(6, 25):
            respuestas.append(await set_Datos_en_Masa(codigo_linea, h, d, 5))

    return respuestas


""" ------------------------------------------------------------------------ Ampliación de festivos ------------------------------------------------------------------------ """
@datosAPI.post("/api/get_datos_festivos/{codigo_linea}", tags=["Datos"])
async def get_Datos_Parada_Todas_Festivos(codigo_linea: int):      
    # Busco los datos solo de festivos
    lista_grupos_datos = []
    
    for fecha_datos in CALEND.get_Festivos():
        lista_grupos_datos.extend(BD.get_Datos_Parada_por_Fechas(codigo_linea, fecha_datos))

    dict_datos = {}

    for grupo_datos_parada in lista_grupos_datos:
        codigo_parada = grupo_datos_parada["codigo_parada"]
        fecha_datos = AUX.transformar_String_a_Datetime_generico(grupo_datos_parada["fecha_datos"]["$date"])

        if not (fecha_datos.month == 5 and fecha_datos.day == 1):
            continue
        """if CALEND.es_festivo(fecha_datos) != festivo:
            continue"""
        
        if codigo_parada not in dict_datos:
            dict_datos[codigo_parada] = []
        dict_datos[codigo_parada].append(grupo_datos_parada)

    dict_medias = {}

    for codigo_parada in dict_datos:
        datos = dict_datos[codigo_parada]

        lista_datos_completa = []
        cantidad_datos = 0
        cantidad_datos_parados = 0

        fechas_paradas = []

        for grupo_datos_parada in datos:
            lista_datos_completa.extend(grupo_datos_parada["lista_datos"])
            cantidad_datos += grupo_datos_parada["cantidad_datos"]
            cantidad_datos_parados += grupo_datos_parada["cantidad_datos_parados"]
            fechas_paradas.extend(grupo_datos_parada["fechas_paradas"])

        media_aritmetica, desviacion_tipica = FUNCDATOS.analizar_Datos(
            lista_datos_completa, cantidad_datos)
        tiempos_paradas = FUNCDATOS.analizar_Tiempos_Paradas(
            cantidad_datos_parados, cantidad_datos, fechas_paradas)

        dict_medias[codigo_parada] = {
            "media_aritmetica": media_aritmetica,
            "desviacion_tipica": desviacion_tipica,
            "cantidad_datos": cantidad_datos,
            "cantidad_datos_parados": cantidad_datos_parados,
            
            # Para calcular cuánto se tira parado un bus en una parada específica
            "datos_paradas": tiempos_paradas
        }

    return dict_medias

""" Cálculo y Set de datos analizados con Fecha """
async def set_Datos_en_Masa_con_Fecha(codigo_linea, hora_inicial, fecha_datos, numero_semanas, forma_filtrada, linea_filtrada):
    if not (AUX.valorValido(hora_inicial, 6, 23) and AUX.valorValido(numero_semanas, 0, 8)):
        return {"message": "Fecha no válida"}

    fecha_actualizacion = AUX.get_Fecha_actual()
    fecha_datos = fecha_datos.replace(microsecond=0, second=0, minute=0, hour=hora_inicial)

    if (forma_filtrada is None or linea_filtrada is None):
        return {"message": "Forma o linea nula"}

    ultimo_dia = fecha_datos
    
    es_Festivo = CALEND.es_festivo(fecha_datos)

    duracion_datos_minutos = 60

    semanaSanta = CALEND.get_Fecha_Semana_Santa()

    for i in range(0, numero_semanas):
        fecha_datos = ultimo_dia - timedelta(weeks=i)
        fecha_datos_max = fecha_datos + timedelta(minutes=duracion_datos_minutos)
        
        if (es_Festivo != CALEND.es_festivo(fecha_datos)):
            print()
 
        # En semana santa se ignoran los datos (hago aux mire fecha si está en semana santa?)
        if (semanaSanta[0] <= fecha_datos <= semanaSanta[1]):
            print("set_Datos: Fecha no válida (Semana santa) : " + str(fecha_datos))
            continue
        
    
        buses_mezclados = BD.get_Buses_con_Intervalo_y_codigo_bus(fecha_datos, fecha_datos_max, codigo_linea)
        
        
        buses = FUNCBUSES.posicionar_Buses_Mezclados(buses_mezclados, forma_filtrada["segmentos"], linea_filtrada)

        if len(buses) <= 2:  # Al menos 2 buses que analizar
            print("set_Datos: Lista de buses vacía --> Error? len=" + str(len(buses)))
            continue
        
        dict_datos = FUNCDATOS.crear_Diccionario_Pares_Buses_y_Paradas(buses, forma_filtrada["segmentos"], 
                                                                        linea_filtrada["paradas"], 
                                                                        [codigo_linea, fecha_datos, duracion_datos_minutos, fecha_actualizacion])

        if dict_datos == None or len(dict_datos.keys()) == 0:
            print("set_Datos: Lista de buses vacía --> Error?")
            continue         
        
        cursor = BD.set_Datos(dict_datos, codigo_linea, fecha_datos)

        if cursor == None:
            return {"message": "set_Datos: Error al insertar un dato: Linea: " + str(codigo_linea) + ", Fecha datos: " + str(fecha_datos)}
        else:
            print({"message": "set_Datos: Datos actualizados correctamente : " + str(codigo_linea) + ", Fecha datos: " + str(fecha_datos)})
    # for

    return {"message": "set_Datos: Datos insertados y actualizados en la BD con éxito"}


@datosAPI.post("/api/set_datos_festivos/{codigo_linea}", tags=["Datos"])
async def set_Datos_Festivos(codigo_linea: int):   
    forma_filtrada = (await FORMAS.get_Forma_Filtrada_Unica(codigo_linea))
    linea_filtrada = (await LINEAS.get_Linea_Filtrada_Unica(codigo_linea))
    respuestas = []
    
    for fecha_datos in CALEND.get_Festivos():   
        
        for i in range(6, 25):
            respuestas.append(await set_Datos_en_Masa_con_Fecha(codigo_linea, i, fecha_datos, 1, forma_filtrada, linea_filtrada))
       
    return respuestas

""" ------------------------------------------------------------------------ Análisis de líneas ------------------------------------------------------------------------ """

""" Analiza línea y la devuelve sin guardar """
@datosAPI.post("/api/datos/get_linea_analizada_ret/{codigo_linea}", tags=["Datos"])
async def get_Linea_Analizada_Ret(codigo_linea: int):
    linea_Analizada = (await LINEAS.get_Linea_Filtrada_Unica(codigo_linea))
    # Los datos están mezclados y no analizados
    datos_analizados = await get_Datos_Parada_Todas(codigo_linea)

    for parada in linea_Analizada["paradas"]:
        datos_analizados_parada = datos_analizados[parada["codigo_parada"]]
        media_a, desv_tipica = float(datos_analizados_parada["media_aritmetica"]), float(
            datos_analizados_parada["desviacion_tipica"])
        datos_paradas = datos_analizados_parada["datos_paradas"]
        parada = FUNCDATOS.set_Velocidades_Parada(
            parada, media_a, desv_tipica, datos_paradas)
    pass

    linea_Analizada = FUNCDATOS.analizar_Tiempos_Linea(linea_Analizada)

    fecha_datos = AUX.get_Fecha_actual()
    linea_Analizada["dia_semana"] = fecha_datos.weekday()
    linea_Analizada["hora_inicial"] = fecha_datos.hour
    linea_Analizada["es_festivo"] = CALEND.es_festivo(fecha_datos) # ES FESTIVO --------------------------------------------

    return linea_Analizada


""" Pide a _Ret crear la Linea Analizada y la guarda en BD sin bus """
@datosAPI.post("/api/datos/analizar_linea/{codigo_linea}", tags=["Datos"])
async def set_Linea_Analizada(codigo_linea: int):
    linea_Analizada = await get_Linea_Analizada_Ret(codigo_linea)

    if (linea_Analizada != None):
        BD.set_Linea_Analizada(linea_Analizada)

    return linea_Analizada


""" Crear línea analizada y la guarda en BD """
@datosAPI.post("/api/datos/get_linea_analizada/{codigo_linea}", tags=["Datos"])
async def get_Linea_Analizada(codigo_linea: int):
    fecha_datos = AUX.get_Fecha_actual()
    linea_analizada = BD.get_Linea_Analizada(codigo_linea, fecha_datos.weekday(), fecha_datos.hour)

    if linea_analizada is None or AUX.es_Fecha_Antigua_Dias(AUX.transformar_String_a_Datetime_generico(linea_analizada["fecha_actualizacion"]), dias=6):
        return await set_Linea_Analizada(codigo_linea)
    else:
        return linea_analizada


""" Crear mapa de tiempos y lo guarda cuando tenga al menos 10 líneas analizadas anteriores y luego cada 5 líneas """
@datosAPI.post("/api/datos/get_mapa_tiempos", tags=["Datos"])
async def get_Mapa_Tiempos(body: dict):
    """
    mapaTiempos.linea_analizada = null
    mapaTiempos.lista_lineas_analizadas = []
    mapaTiempos.informacion = []
    mapaTiempos.fecha_inicio = Tiempo()
    """
    
    if "fecha_inicio" not in body:
        print({"message": "get_Mapa_Tiempos: Error no hay fecha_inicio"})   
        return
    
    fecha_inicio = AUX.transformar_String_a_Datetime_generico(body["fecha_inicio"])
    codigo_linea = body["codigo_linea"]
    bus = body["bus_seleccionado"]
    ultima_linea_analizada = body["linea_analizada"]
    lista_lineas_analizadas = body["lista_lineas_analizadas"]        
    
    nueva_linea_analizada = FUNCDATOS.construir_Mapa_Tiempos(bus, await get_Linea_Analizada(codigo_linea))

    # Si hay una línea analizada anterior, la fusiono con la nueva
    if ultima_linea_analizada is not None:
        segmentos = (await FORMAS.get_Forma_Filtrada_Unica(codigo_linea))["segmentos"]
        
        # nueva_linea_analizada = FUNCDATOS.aplicar_Tendencia_Anterior(nueva_linea_analizada, ultima_linea_analizada)        
        nueva_linea_analizada = FUNCDATOS.estudiar_Tendencia(nueva_linea_analizada, ultima_linea_analizada, bus["codigo_proxima_parada"])        
        nueva_linea_analizada = FUNCDATOS.fusionar_Lineas_Analizadas(bus["codigo_bus"], nueva_linea_analizada, ultima_linea_analizada, segmentos)
    

    mapa_Tiempos = {
        "fecha_inicio": fecha_inicio, 
        "codigo_linea": codigo_linea,
        "codigo_bus": bus["codigo_bus"],
        "bus_seleccionado": bus,
        "linea_analizada": nueva_linea_analizada,
        "lista_lineas_analizadas": lista_lineas_analizadas + [nueva_linea_analizada],
    }

    if len(lista_lineas_analizadas) > 10 and len(lista_lineas_analizadas) % 5 == 0: # A partir de 10 cuando haya múltipli de 5 en la lista se guarda
            cursor = BD.set_Mapa_Tiempos(fecha_inicio, codigo_linea, bus["codigo_bus"], mapa_Tiempos) 
            if cursor is not None:
                print({"message": "get_Mapa_Tiempos: Mapa de tiempos guardado en BD"})   
                

    return {   
        "fecha_inicio": fecha_inicio, 
        "codigo_linea": codigo_linea,
        "bus_seleccionado": None,    
        "linea_analizada": mapa_Tiempos["linea_analizada"],
        "lista_lineas_analizadas": mapa_Tiempos["lista_lineas_analizadas"],
    }
