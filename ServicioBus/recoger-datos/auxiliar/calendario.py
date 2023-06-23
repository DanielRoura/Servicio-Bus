author = "Daniel Roura Sepúlveda"

from datetime import datetime
import pytz

# Franja Horaria de Málaga, Deta Space está en otra franja
franja_horaria_malaga = pytz.timezone("Europe/Madrid") 
# tzinfo = pytz.utc

dia = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=franja_horaria_malaga)

# Festivos en España
festivosMalaga = [
    dia.replace(month=1, day=2), # Año Nuevo
    dia.replace(month=1, day=6), # Reyes
    dia.replace(month=2, day=28), # Día de Andalucía
    dia.replace(month=4, day=6), # Jueves Santo
    dia.replace(month=4, day=7), # Viernes Santo
    dia.replace(month=5, day=1), # Fiesta del Trabajo
    dia.replace(month=8, day=15), # Asunción de la Virgen
    dia.replace(month=9, day=8), # Virgen de la Victoria
    dia.replace(month=10, day=12), # Fiesta Nacional de España
    dia.replace(month=11, day=1), # Todos los Santos
    dia.replace(month=12, day=6), # Día de la Constitución
    dia.replace(month=12, day=8), # Inmaculada Concepción
    dia.replace(month=12, day=25), # Navidad
]

def es_festivo(fecha):
    for festivo in festivosMalaga:
        if fecha.day == festivo.day and fecha.month == festivo.month and fecha.year == festivo.year:
            return True
    return False

def get_Festivos():
    return festivosMalaga

def get_Fecha_Semana_Santa():
    return datetime(dia.year, 4, 1, tzinfo=franja_horaria_malaga), datetime(dia.year, 4, 10, tzinfo=franja_horaria_malaga)