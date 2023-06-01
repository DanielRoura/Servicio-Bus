import React from 'react'; //  { useState, useCallback, useEffect } 
import { MapContainer, TileLayer, LayersControl } from 'react-leaflet';
import L from 'leaflet';
import { Box } from '@mui/material';
import { Styler } from '../Styler/Styler';
import MarcadoresBus from './Marcadores/MarcadoresBus';
import MarcadoresParadas from './Marcadores/MarcadoresParadas';
import PolylinesSegmentos from './Polylines/PolylinesSegmentos';
import MarcadorUsuario from './Marcadores/MarcadorUsuario';

/* https://react-leaflet.js.org/docs/start-introduction/ */
/* https://leafletjs.com/reference.html */
/* https://react-leaflet.js.org/docs/api-map/ */

const FarLands = L.latLngBounds(
  L.latLng(36.78, -4.55),
  L.latLng(36.65, -4.25)
);

const MapaDinamico = ({ buses, linea, segmentos, busSeleccionado, busPrediccion, funcSetBusSeleccionado, funcSetParadaSeleccionada }) => {
  const coordenadasIniciales = [36.72184282369917, -4.418403224132213];

  /* Return */
  // Bus Seleccionado: {busSeleccionado != null ? busSeleccionado.codigo_bus : "Ninguno"}
  return (
    <div>
      <Box sx={Styler.mapa}>
        <MapContainer
          className="leaflet-container"
          style={{ width: "100%", height: "60vh" }}
          center={coordenadasIniciales}
          zoom={13}
          removeOutsideVisibleBounds={false}
          scrollWheelZoom={true}
          maxBounds={FarLands}
          maxBoundsViscosity={1.0}
          maxZoom={18}
          minZoom={12} // minZoom={6}

          noMoveStart={false}
        >

          <TileLayer
            attribution='&copy; 
            <a 
              href="https://www.openstreetmap.org/copyright"
            >
              OpenStreetMap
            </a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <LayersControl position="topright">
            <MarcadorUsuario />

            <MarcadoresBus
              buses={buses}
              busSeleccionado={busSeleccionado}
              funcSetBusSeleccionado={funcSetBusSeleccionado}
              busPrediccion={busPrediccion}
            />

            <MarcadoresParadas
              linea={linea}
              funcSetParadaSeleccionada={funcSetParadaSeleccionada}
            />

            <PolylinesSegmentos
              segmentos={segmentos}
              busSeleccionado={busSeleccionado}
            />

          </LayersControl>

        </MapContainer>
      </Box >
    </div>
  )
}

export default MapaDinamico