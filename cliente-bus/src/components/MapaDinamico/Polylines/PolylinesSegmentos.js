import React from 'react'
import { LayerGroup, LayersControl, Polyline } from 'react-leaflet'
import { TiempoAbs } from '../../common/FuncionesTiempo/FuncionesTiempo'

const PolylinesSegmentos = ({ segmentos, busSeleccionado}) => {
    return (
        <LayersControl.Overlay checked name="Mostrar Recorrido">
            <LayerGroup>
                {segmentos != null ? segmentos.map((segmento, idx) => {
                    return (
                        <Polyline
                            key={`segmento-${segmento.orden + segmento.sentido * 1000 + TiempoAbs()}`} // {idx + segmento.orden * segmento.sentido * -1000 + TiempoAbs()}
                            positions={[[segmento.latitud_1, segmento.longitud_1],
                            [segmento.latitud_2, segmento.longitud_2]]}
                            color={busSeleccionado && (busSeleccionado.codigo_proxima_parada === segmento.codigo_proxima_parada)
                                && segmento.orden >= busSeleccionado.orden_segmento ? 'black' : 'black'}
                            zIndexOffset={0}
                            options={{
                                key: `segmento-${segmento.orden + segmento.sentido * 1000 + TiempoAbs()}`,
                            }}
                        >
                            
                        </Polyline>
                    )
                }) : null}
            </LayerGroup>
        </LayersControl.Overlay>
    )
}

export default PolylinesSegmentos
