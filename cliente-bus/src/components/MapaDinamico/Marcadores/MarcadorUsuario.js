import React, { useEffect, useState } from 'react'
import { Marker, Tooltip } from 'react-leaflet';
import { marcadorIcon } from '../Iconos/MapaIconos';

const MarcadorUsuario = () => {
    const [misCoordenadas, setMisCoordenadas] = useState([]);

    useEffect(() => {
        navigator.geolocation.getCurrentPosition(
            position => {
                setMisCoordenadas([position.coords.latitude, position.coords.longitude]);
                console.log("[MarcadorUsuario:", misCoordenadas)

            },
            error => console.log(error),
            { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
    }, [misCoordenadas]);

    if (misCoordenadas != null && misCoordenadas.length > 0) {
        return (
            <Marker
                key={`misCoordenadas`}
                position={misCoordenadas}
                icon={marcadorIcon()}
            >
                <Tooltip>
                    {"Su posición aproximada en tiempo real"}
                </Tooltip>
            </Marker>

        )
    }

}

export default MarcadorUsuario