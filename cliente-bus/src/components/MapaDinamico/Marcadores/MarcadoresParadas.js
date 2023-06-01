import React from 'react'
import { Marker, LayerGroup, LayersControl } from 'react-leaflet';
import { paradaIcon } from '../Iconos/MapaIconos';

const MarcadoresParadas = ({ linea, funcSetParadaSeleccionada }) => {
  const handleParadaSeleccionada = (event) => {
    const marker = event.target;
    // console.log("[MapaDinamico]: ", ["Parada Seleccionada: ", marker.options.options.codigo_parada, TiempoMinutosSegundos()])
    funcSetParadaSeleccionada(marker.options.options.codigo_parada);
  };

  return (
    <LayersControl.Overlay checked name="Mostrar Paradas">
      <LayerGroup>
        {linea != null ? linea.paradas.map((parada, idx) =>
          <Marker
            key={`parada-${parada.codigo_parada}`}
            position={[parada.latitud, parada.longitud]}
            icon={paradaIcon()}
            zIndexOffset={500}
            eventHandlers={{
              click: handleParadaSeleccionada,
            }}
            options={{
              key: `parada-${parada.codigo_parada}`,
              codigo_parada: parada.codigo_parada,
            }}
          >
            
          </Marker>
        ) : null}
      </LayerGroup>
    </LayersControl.Overlay>
  )
}

export default MarcadoresParadas
