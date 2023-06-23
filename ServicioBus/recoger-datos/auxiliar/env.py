author = "Daniel Roura Sepúlveda"

from dotenv import load_dotenv
import os 

# Carga las variables de entorno desde el archivo .env
load_dotenv()

uri_bd = os.getenv('PY_URI')

# Deta se reinicia solo y se detiene la recolección en False
recoleccion_activa = os.getenv('PY_RECOLECCION_ACTIVA') == "True"
estado_datos = os.getenv('PY_GUARDAR_DATOS') == "True"

# Origen de datos
origen = os.getenv('PY_ORIGEN')

# Enlace a datos abiertos y línea que vamos a filtrar
url_buses = "https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTLineasUbicaciones/lineasyubicaciones.csv"
url_lineas_y_paradas = "https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTLineasYParadas/lineasyparadas.geojson"
url_formas = "https://datosabiertos.malaga.eu/recursos/transporte/EMT/lineasYHorarios/shapes.csv"

# Reescribir en set_Datos
PY_REESCRIBIR_DATOS = os.getenv('PY_REESCRIBIR_DATOS') == "True"