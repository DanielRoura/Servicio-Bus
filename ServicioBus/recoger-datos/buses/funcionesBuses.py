import auxiliar.constructores as CONSTR
import auxiliar.auxiliar as AUX


""" Construye los buses a partir del string sacado de la url de datos abiertos """
def contruir_Buses_desde_String(codigo_linea_str, buses_str):
    nuevos_buses = []
    
    for bus_str in buses_str:
        bus_lista = bus_str.replace('"', '').strip().split(",")
        if codigo_linea_str in bus_str:
            bus_JSON = CONSTR.construir_Bus_JSON(int(bus_lista[0]), float(bus_lista[1]), int(bus_lista[2]),
                                                            float(bus_lista[4]), float(bus_lista[3]), int(bus_lista[5]), 
                                                            AUX.transformar_String_a_Datetime_generico(bus_lista[6]))           
            nuevos_buses.append(bus_JSON)
            
    return nuevos_buses


""" Divide los buses en Posicionados y no Posicionados """
def posicionar_Buses_Mezclados(buses_mezclados, segmentos, linea):
    buses_Pos, buses_sin_Pos = [], []
    
    for bus in buses_mezclados:
        if "codigo_proxima_parada" in bus:
            buses_Pos.append(bus)
        else:
            buses_sin_Pos.append(bus)
            
    return buses_Pos + posicionar_Buses(buses_sin_Pos, segmentos, linea)


""" Calcula la posición del bus, sus siguiente parada, su camino y la distancia"""
def posicionar_Buses(buses, segmentos, linea):
    # Podría unirle el segmento al guardarlo para reducir cálculos
    buses = unir_Buses_con_Segmentos(buses, segmentos) # Aquí se pone el bus sobre el segmento

    # Distancia hasta la siguiente parada
    buses = calcular_Distancia_Bus_Siguiente_Parada(buses, segmentos, linea["paradas"])
    return buses

def unir_Buses_con_Segmentos(buses, segmentos):
    # lista para almacenar las paradas
    buses_con_segmentos = []
    
    for bus in buses:
        if "segmento" not in bus:
            lat_p = float(bus['latitud'])
            lon_p = float(bus['longitud'])
            
            segmento_mas_cercano, distancia = AUX.buscar_Segmento_Cercano(bus["sentido"], segmentos, (lat_p, lon_p))

            if segmento_mas_cercano is None:
                # Error más grave!!
                print("ERROR: no hay segmento cercano con bus=" + str(bus["codigo_bus"]))
            else:
                bus["orden_segmento"] = segmento_mas_cercano["orden"]
                # bus["segmento"] = segmento_mas_cercano

                # Aproximación de la posición
                bus["error"] = distancia
                bus["latitud"] = segmento_mas_cercano["latitud_1"]
                bus["longitud"] = segmento_mas_cercano["longitud_1"]
                buses_con_segmentos.append(bus)
            pass
        else:
            buses_con_segmentos.append(bus)
        pass
    pass

    return buses_con_segmentos

def calcular_Distancia_Bus_Siguiente_Parada(buses, segmentos, paradas):
    # Calculo la distancia entre cada bus y la siguiente parada
    for bus in buses:
        segmento_bus = AUX.get_Segmento_con_Orden(bus["orden_segmento"], bus["sentido"], segmentos)
        
        if "orden_parada" in segmento_bus:
            proxima_parada = AUX.get_Parada_con_Orden(segmento_bus["orden_parada"], segmento_bus["sentido"], paradas)
            bus["distancia_proxima_parada"] = 0
            bus["codigo_proxima_parada"] = proxima_parada["codigo_parada"]
            bus["ordenes_segmentos"] = [] #[bus["orden_segmento"]]

        elif "orden_proxima_parada" in segmento_bus:
            proxima_parada = AUX.get_Parada_con_Orden_sin_Sentido(segmento_bus["orden_proxima_parada"], paradas)
            camino_segmentos = AUX.get_Camino_entre_Segmentos(bus["orden_segmento"], proxima_parada["orden_segmento"], bus["sentido"], segmentos)
            distancia_proxima_parada, ordenes_segmentos = AUX.get_Atributos_Camino(camino_segmentos)
            
            bus["distancia_proxima_parada"] = distancia_proxima_parada
            bus["codigo_proxima_parada"] = proxima_parada["codigo_parada"]
            bus["ordenes_segmentos"] = ordenes_segmentos

        else:
            print("ERROR: no hay parada cercana con bus=" + str(bus["codigo_bus"]))
            continue
        pass
    pass

    return buses