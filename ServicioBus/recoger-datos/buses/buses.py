author = "Daniel Roura Sepúlveda"

import auxiliar.BD as BD
import auxiliar.constructores as CONSTR
import auxiliar.env as ENV
import lineas.lineas as LINEAS
import lineas.formas as FORMAS
import auxiliar.auxiliar as AUX
import buses.funcionesBuses as FUNCBUSES
#
from datetime import datetime, timedelta
from fastapi import APIRouter


busAPI = APIRouter()


@busAPI.post('/api/acciones/set_buses/{codigo_linea}', tags=["Buses", "Main"])
async def set_Buses_Filtrados(codigo_linea: int):
    print("Acción de recoger autobuses")

    if ENV.recoleccion_activa:
        nuevos_buses, bus_recoleccion = await get_Buses_Filtrados_Ret(codigo_linea)

        if nuevos_buses == None:
            return {"message": "No hay nuevos buses de la línea " + str(codigo_linea)}
        else:
            BD.set_Buses(ENV.estado_datos, nuevos_buses, bus_recoleccion)
            return {"message": "Hay " + str(len(nuevos_buses)) + " nuevos buses de la línea " + str(codigo_linea)}
    else:
        return {"message": "Recolección de datos inactiva"}
    

@busAPI.get("/api/acciones/get_buses_ret/{codigo_linea}", tags=["Buses"])
async def get_Buses_Filtrados_Ret(codigo_linea: int):
    codigo_linea_str = str(codigo_linea) + ".0"
    data = AUX.get_datos(ENV.url_buses)

    if len(data) == 0:
        return None
    
    buses_str = data.strip().split("\n")
    nuevos_buses = FUNCBUSES.contruir_Buses_desde_String(codigo_linea_str, buses_str)

    if len(nuevos_buses) == 0:
        return None
    else:
        forma_filtrada = (await FORMAS.get_Forma_Filtrada_Unica(codigo_linea))
        linea_filtrada = (await LINEAS.get_Linea_Filtrada_Unica(codigo_linea))
        nuevos_buses = FUNCBUSES.posicionar_Buses(nuevos_buses, forma_filtrada["segmentos"], linea_filtrada)
        bus_recoleccion = CONSTR.construir_Bus_recoleccion_JSON(len(nuevos_buses), AUX.get_Fecha_actual(), ENV.origen)

        return nuevos_buses, bus_recoleccion


@busAPI.get("/api/acciones/get_buses/{codigo_linea}", tags=["Buses", "Main"])
async def get_Buses_Filtrados(codigo_linea: int):
    # Últimos autobuses de hace 10 minutos hasta ahora
    hora_minima = datetime.now(
        AUX.franja_horaria_malaga) - timedelta(minutes=30, seconds=00)
    hora_minima = hora_minima.replace(tzinfo=AUX.tzinfo)

    buses =  BD.get_Buses_con_Hora_minima(hora_minima, codigo_linea)

    if len(buses) == 0:
        return []

    # Los filtro, todos tienen que tener la hora más reciente
    buses_filtrados = AUX.filtrar_Buses_mas_recientes(buses)
    
    if "distancia_proxima_parada" not in buses_filtrados[0]:
        forma_filtrada = (await FORMAS.get_Forma_Filtrada_Unica(codigo_linea))
        linea_filtrada = (await LINEAS.get_Linea_Filtrada_Unica(codigo_linea))
        buses_posicionados = FUNCBUSES.posicionar_Buses(buses_filtrados, forma_filtrada["segmentos"], linea_filtrada)
    else:
        buses_posicionados = buses_filtrados

    return buses_posicionados

@busAPI.get("/api/acciones/get_ultimo_log", tags=["Buses", "Main"])
async def get_Ultimo_Log():
    log =  BD.get_Ultimo_Log_con_Datos()
    return log
