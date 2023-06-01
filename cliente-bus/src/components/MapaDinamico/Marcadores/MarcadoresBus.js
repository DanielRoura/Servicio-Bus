import React, { useState, useEffect, useCallback, useRef } from 'react'
import { Marker, LayerGroup, LayersControl, Tooltip } from 'react-leaflet';
import { bus1Icon, bus1IconPred, bus2Icon, bus2IconPred } from '../Iconos/MapaIconos';
import { TiempoAbs, TiempoMinutosSegundos } from '../../common/FuncionesTiempo/FuncionesTiempo';

const MarcadoresBus = ({ buses, busSeleccionado, funcSetBusSeleccionado, busPrediccion }) => {
    const [marcadores, setMarcadores] = useState(null);
    const layerRef = useRef(null);

    const handleBusSeleccionado = useCallback((event) => {
        const marker = event.target;
        console.log("[MapaDinamico]: ", ["Bus Seleccionado: ", marker.options.options.codigo_bus, TiempoMinutosSegundos()])
        funcSetBusSeleccionado(marker.options.options.codigo_bus);
    }, [funcSetBusSeleccionado]);

    useEffect(() => {
        setMarcadores(null)

        if (layerRef.current != null) {
            //layerRef.current.clearLayers();
        }

        var nuevosMarcadores = null;
        if (busSeleccionado === null) {
            var nuevosBuses = (buses.map((bus, idx) => {
                return (
                    <Marker
                        key={`bus-${bus.codigo_bus + TiempoAbs()}`}
                        position={[bus.latitud, bus.longitud]}
                        zIndexOffset={990}
                        icon={bus.sentido === 1 ? bus1Icon() : bus2Icon()}
                        eventHandlers={{
                            click: handleBusSeleccionado,
                        }}
                        options={{
                            key: `bus-${idx}`,
                            bus: { bus },
                            codigo_bus: bus.codigo_bus,
                        }}
                    >
                    </Marker>
                )
            }))

            nuevosMarcadores = [
                <LayerGroup ref={layerRef}>,
                    {nuevosBuses},
                </LayerGroup>
            ]

        } else {
            nuevosMarcadores = [
                <>
                    <Marker
                        key={`bus-${busSeleccionado.codigo_bus}`}
                        position={[busSeleccionado.latitud, busSeleccionado.longitud]}
                        zIndexOffset={995}
                        icon={busSeleccionado.sentido === 1 ? bus1Icon() : bus2Icon()}
                        eventHandlers={{
                            click: null, // No puedes seleccionar lo ya seleccionado
                        }}
                        options={{
                            key: `bus-${busSeleccionado.codigo_bus}`,
                            bus: { busSeleccionado },
                            codigo_bus: busSeleccionado.codigo_bus,
                        }}
                    />
                    {busPrediccion != null && (
                        <>
                            <Marker
                                key={`busPrediccion-${busPrediccion.codigo_bus}`}
                                position={[busPrediccion.latitud, busPrediccion.longitud]}
                                zIndexOffset={999}
                                icon={busPrediccion.sentido === 1 ? bus1IconPred() : bus2IconPred()}
                            >
                                <Tooltip>
                                    {"Posición aproximada en tiempo real del autobús " + busPrediccion.codigo_bus}
                                </Tooltip>
                            </Marker>
                        </>
                    )}
                </>
            ];
        }

        // console.log("[MapaDinamico]: ", ["Actualización de marcadores ", TiempoMinutosSegundos()])
        setMarcadores(nuevosMarcadores);

    }, [buses, busSeleccionado, busPrediccion, handleBusSeleccionado])


    return (
        <LayersControl.Overlay checked name="Mostrar Autobuses">
            <LayerGroup ref={layerRef}>
                {marcadores}
            </LayerGroup>
        </LayersControl.Overlay>
    )
}

export default MarcadoresBus