import auxiliar.auxiliar as AUX

def unir_Linea_y_Forma(linea, forma):
    # Debería añadir el orden del otro aquí a ambos
    paradas_seg = unir_Paradas_y_Segmentos(linea["paradas"], forma["segmentos"])
    paradas_seg_dist = calcular_Distancia_Paradas(paradas_seg, forma["segmentos"])
    forma["segmentos"] = actualizar_Paradas_Formas(forma["segmentos"])

    linea["paradas"] = paradas_seg_dist
    return linea, forma

def unir_Paradas_y_Segmentos(paradas, segmentos):
    # ya debería estar ordenadas
    paradas_ordenadas = sorted(paradas, key=lambda p: p['orden']) 

    # lista para almacenar las paradas
    paradas_seg = []
    indice_seg_cercano = None
    len_seg = len(segmentos)
    
    for i in range(len(paradas_ordenadas)):
        parada_actual = paradas_ordenadas[i]
        distancia_minima = float("inf")

        lat_p = float(parada_actual['latitud'])
        lon_p = float(parada_actual['longitud'])
        
        j = 0

        # Busco el segmento más cercano a la parada
        while j < len_seg:
            segmento = segmentos[j]
            j += 1

            lat_s_2 = float(segmento['latitud_2'])
            lon_s_2 = float(segmento['longitud_2'])
            
            if (segmento["sentido"] == parada_actual["sentido"]):
                distancia_parada_segmento = AUX.calcular_Distancia_Euclidea((lat_p, lon_p), (lat_s_2, lon_s_2))
                
                if distancia_parada_segmento <= distancia_minima and segmento not in paradas_seg:
                    distancia_minima = distancia_parada_segmento
                    indice_seg_cercano = j % len_seg
                pass
            pass
        pass
        

        if distancia_minima == float("inf"):
            print("ERROR: no hay segmento cercano con j=" + str(j))
        else:
            parada_actual["orden_segmento"] = segmentos[indice_seg_cercano]["orden"]
            segmentos[indice_seg_cercano]["orden_parada"] = parada_actual["orden"]
            segmentos[indice_seg_cercano]["codigo_parada"] = parada_actual["codigo_parada"]
        pass
    pass

    return paradas

def calcular_Distancia_Paradas(paradas_seg, segmentos):
    paradas_dist = []
    len_paradas = len(paradas_seg)
    parada_actual = paradas_seg[0]

    # Calculo la distancia entre paradas utilizando los segmentos
    for i in range(1, len_paradas + 1):
        parada_anterior = parada_actual
        parada_actual = paradas_seg[i % len_paradas]

        distancia_proxima_parada = AUX.calcular_Distancia_entre_Segmentos(parada_anterior["orden_segmento"], parada_actual["orden_segmento"], parada_actual["sentido"], segmentos)
        
        parada_anterior["codigo_proxima_parada"] = parada_actual["codigo_parada"]
        parada_anterior["distancia_proxima_parada"] = distancia_proxima_parada
        paradas_dist.append(parada_anterior)
        pass
    pass

    return paradas_dist


""" EXTRA """
def actualizar_Paradas_Formas(segmentos):
    orden_parada = None
    codigo_parada = None

    for seg in segmentos:
        if "orden_parada" in seg:
            orden_parada = seg["orden_parada"]
            codigo_parada = seg["codigo_parada"]
            break
        pass
    pass

    for i in range(len(segmentos) - 1, -1, -1):
        seg_actual = segmentos[i]
        if "orden_parada" in seg_actual:
            orden_parada = seg_actual["orden_parada"]  
            codigo_parada = seg_actual["codigo_parada"]
        else:
            seg_actual["orden_proxima_parada"] = orden_parada
            seg_actual["codigo_proxima_parada"] = codigo_parada
        pass
    pass

    return segmentos
