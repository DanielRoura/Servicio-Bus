author = "Daniel Roura Sepúlveda"

import auxiliar.env as ENV
#
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

extraAPI = APIRouter()

@extraAPI.get("/api")
async def index():
    with open("./static/index.html") as file:
        return HTMLResponse(file.read())


@extraAPI.get("/api/datos/estado", tags=["Extra"])
async def get_Estado_datos():
    if ENV.estado_datos:
        return [{"estado": "Se están guardando los datos"}]
    else:
        return [{"estado": "No se están guardando los datos"}]


@extraAPI.get("/api/recoleccion/estado", tags=["Extra"])
async def estado():
    if ENV.recoleccion_activa:
        return [{"estado": "Recolección activa"}]
    else:
        return [{"estado": "Recolección inactiva"}]
