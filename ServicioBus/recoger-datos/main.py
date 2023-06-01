author = "Daniel Roura Sepúlveda"

import auxiliar.BD as BD
import auxiliar.env as ENV
import buses.buses as BUSES
import lineas.lineas as LINEAS
import lineas.formas as FORMAS
import datos.datos as DATOS
import lineas.funcionesLinForm as FUNCLINFORM
import auxiliar.extras as EXTRAS
#
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(BUSES.busAPI)
app.include_router(LINEAS.lineaAPI)
app.include_router(FORMAS.formaAPI)
app.include_router(DATOS.datosAPI)
app.include_router(EXTRAS.extraAPI)
app.include_router(BD.bdAPI)

""" SECCIONES """
@app.post('/api/acciones/set_linea_y_forma/{codigo_linea}', tags=["Lineas", "Formas"])
async def set_Linea_y_Forma(codigo_linea: int):
    linea_filtrada = await LINEAS.get_Linea_Filtradas_Ret(codigo_linea)
    forma_filtrada = await FORMAS.get_Formas_Filtradas_Ret(codigo_linea)

    # En esta función le voy a añadir a cada parada su segmento más cercano, pero solo poniendo el orden
    # y a cada segmento su parada más cercana, con el orden

    try:
        linea_actualizada, forma_actualizada = FUNCLINFORM.unir_Linea_y_Forma(linea_filtrada, forma_filtrada)

        BD.set_Linea(linea_actualizada)
        BD.set_Forma(forma_actualizada)
        return {"message": "Set_Secciones: lineas y formas actualizadas con éxito"}
    except:
        return {"message": "Set_Secciones: ERROR"}

""" ACCIONES AUTOMÁTICAS """
@app.post('/__space/v0/actions', tags=["Lineas", "Formas", "Buses", "Datos", "Deta Space"])
async def deta_accion(data: dict):
    event = data["event"]
    if event["id"] == "get_datos":
        print("Deta Action: " + event["id"])
        return await BUSES.set_Buses_Filtrados(11)
    elif event["id"] == "set_tiempos_ahora":
        print("Deta Action: " + event["id"])
        if ENV.recoleccion_activa:
            return await DATOS.set_Datos_ahora(11)
        else:
            return {"message": "No se pueden analizar tiempos: recoleccion_activa es falso"}
    elif event["id"] == "set_linea_analizada_hora":
        print("Deta Action: " + event["id"])
        return await DATOS.set_Linea_Analizada(11)
    else:
        return {"message": "error en Accion Deta"}

"""
{
  "event": {
    "id": "get_datos",
    "trigger": "schedule"
  }
}
"""