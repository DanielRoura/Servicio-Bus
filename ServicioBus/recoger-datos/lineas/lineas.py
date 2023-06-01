author = "Daniel Roura Sepúlveda"

import auxiliar.auxiliar as AUX
import auxiliar.BD as BD
import auxiliar.constructores as CONSTR
import auxiliar.env as ENV

#
import geojson
from fastapi import APIRouter

lineaAPI = APIRouter()

""" ------------------------------------------------------------------------ """
@lineaAPI.get('/api/acciones/get_lineas_ret/{codigo_linea}', tags=["Lineas"])
async def get_Linea_Filtradas_Ret(codigo_linea: int):
    data = AUX.get_datos(ENV.url_lineas_y_paradas)
    lineas_y_paradas = geojson.loads(data)
    linea = next((lin for lin in lineas_y_paradas if lin.get(
        "codLinea") == codigo_linea), None)

    if linea is None:
        return None

    paradas = []

    for parada in linea["paradas"]:
        datos_parada = parada["parada"]
        parada_JSON = CONSTR.construir_Parada_JSON(datos_parada.get("codParada"), 
                                                   linea.get("codLinea"),
                                                   datos_parada.get("nombreParada"), 
                                                   parada.get("orden"), 
                                                   parada.get("sentido"),
                                                    datos_parada.get("latitud"), 
                                                    datos_parada.get("longitud"))
        paradas.append(parada_JSON)

    # Construyo la línea con las paradas
    linea_JSON = CONSTR.construir_Linea_JSON(linea.get("codLinea"), linea.get("nombreLinea"),
                                             linea.get("cabeceraIda"), linea.get(
        "cabeceraVuelta"), paradas,
        AUX.get_Fecha_actual())
    return linea_JSON

@lineaAPI.get("/api/acciones/get_linea/{codigo_linea}", tags=["Lineas", "Main"])
async def get_Linea_Filtrada_Unica(codigo_linea: int):
    lineas = BD.get_Linea_mas_reciente(codigo_linea)
    if (len(lineas) > 0):
        return lineas[0]
    return []

@lineaAPI.get("/api/acciones/get_lineas_disponibles", tags=["Lineas"])
async def get_Lineas_Disponibles():
    lineas_disponibles = BD.get_Lineas_disponibles()
    return lineas_disponibles