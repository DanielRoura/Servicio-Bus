author = "Daniel Roura Sepúlveda"

import auxiliar.auxiliar as AUX
import auxiliar.BD as BD
import auxiliar.constructores as CONSTR
import auxiliar.env as ENV
#
from fastapi import APIRouter

formaAPI = APIRouter()

""" ------------------------------------------------------------------------ """
@formaAPI.get('/api/acciones/get_formas_ret/{codigo_linea}', tags=["Formas"])
async def get_Formas_Filtradas_Ret(codigo_linea: int):
    codigo_linea_forma_ida = str(codigo_linea) + "IDA"
    codigo_linea_forma_vuelta = str(codigo_linea) + "VTA"
    data = AUX.get_datos(ENV.url_formas)

    formas = data.strip().split("\n")
    formas_filtradas_ida = []
    formas_filtradas_vuelta = []
    segmentos = []

    for punto in formas:
        punto = punto.replace('"', '').strip().split(",")

        if (punto[0] == codigo_linea_forma_ida):
            forma_ida_json = CONSTR.construir_Forma_Ida_Vuelta_JSON(1, punto[1], punto[2], punto[3])
            formas_filtradas_ida.append(forma_ida_json)

        elif (punto[0] == codigo_linea_forma_vuelta):
            forma_vuelta_json = CONSTR.construir_Forma_Ida_Vuelta_JSON(2, punto[1], punto[2], punto[3])
            formas_filtradas_vuelta.append(forma_vuelta_json)

    len_formas_ida = len(formas_filtradas_ida)
    len_formas_vuelta = len(formas_filtradas_vuelta)

    if len_formas_ida > 1 and len_formas_vuelta > 1:
        # Construir los segmentos de ida
        for i in range(1, len_formas_ida):
            forma_1 = formas_filtradas_ida[i-1]
            forma_2 = formas_filtradas_ida[i]

            latitud_1 = float(forma_1["latitud"])
            longitud_1 = float(forma_1["longitud"])
            latitud_2 = float(forma_2["latitud"])
            longitud_2 = float(forma_2["longitud"])

            distancia = round(AUX.calcular_Distancia_Haversine([latitud_1, longitud_1], [latitud_2, longitud_2]) , 2)

            segmento_json = CONSTR.construir_Segmento_JSON(int(forma_1["orden"]),
                                                             int(forma_1["sentido"]),
                                                             latitud_1,
                                                             longitud_1,
                                                             latitud_2,
                                                             longitud_2,
                                                             distancia)
            if (segmento_json != None):
                segmentos.append(segmento_json)

        # Construir los segmentos de vuelta
        for i in range(1, len_formas_vuelta):
            forma_1 = formas_filtradas_vuelta[i-1]
            forma_2 = formas_filtradas_vuelta[i]

            latitud_1 = float(forma_1["latitud"])
            longitud_1 = float(forma_1["longitud"])
            latitud_2 = float(forma_2["latitud"])
            longitud_2 = float(forma_2["longitud"])

            distancia = round(AUX.calcular_Distancia_Haversine([latitud_1, longitud_1], [latitud_2, longitud_2]) , 2)

            segmento_json = CONSTR.construir_Segmento_JSON(int(forma_1["orden"]),
                                                             int(forma_1["sentido"]),
                                                             latitud_1,
                                                             longitud_1,
                                                             latitud_2,
                                                             longitud_2,
                                                             distancia)
            if (segmento_json != None):
                segmentos.append(segmento_json)

        formas_linea_json = CONSTR.construir_Forma_JSON(
            codigo_linea, segmentos, AUX.get_Fecha_actual())
        
        return formas_linea_json
    else:
        return None

@formaAPI.get("/api/acciones/get_forma/{codigo_linea}", tags=["Formas", "Main"])
async def get_Forma_Filtrada_Unica(codigo_linea: int):
    formas = BD.get_Forma_mas_reciente_Filtrada(codigo_linea)
    if (len(formas) > 0):
        return formas[0]
    return []
