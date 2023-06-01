import { Box, Card, CardActions, CardContent, Typography } from '@mui/material'
import React from 'react'
import { IconoBasura } from '../common/Iconos/Iconos'
// import { parseTiempo } from '../common/FuncionesTiempo/FuncionesTiempo'
import Boton from '../common/Boton/Boton'
import { Styler } from '../Styler/Styler'
import { parseTiempoAjustado } from '../common/FuncionesTiempo/FuncionesTiempo'

const TarjetaBus = ({ paradas, busSeleccionado, codigoBusSeleccionado, funcSetBusSeleccionado, direccion }) => {
    // const codigo_parada = linea_analizada.paradas.find((parada) => parada.codigo_parada === fila.row.codigoParada);;

    return (
        <Card
            className="tarjeta"
            sx={Styler.tarjeta}>
            <CardContent>
                <Typography variant="h5" color="text.secondary">
                    {busSeleccionado != null ? "Código: " + busSeleccionado.codigo_bus : "Autobús no seleccionado"}
                </Typography>

                <Typography variant="body2" color="text.secondary">
                    Última actualización: {busSeleccionado != null ? parseTiempoAjustado(busSeleccionado.fecha_actualizacion) : ""}
                </Typography>

                <Box
                    component="span"
                    sx={{
                        overflow: 'auto',
                        display: 'block',
                        padding: 1,
                        margin: 1,
                        borderRadius: 2,
                        height: "100%"
                    }}
                >
                    <p>
                        Próxima parada: {busSeleccionado != null ? paradas.find((parada) => parada.codigo_parada === busSeleccionado.codigo_proxima_parada).nombre_parada : ""}
                    </p>

                    <p>
                        Direccion: {direccion != null ? direccion : ""}
                    </p>

                    <p>
                        Distancia hasta la próxima parada: {busSeleccionado != null ? (busSeleccionado.distancia_proxima_parada).toFixed(0) + "m" : ""}
                    </p>

                </Box>

            </CardContent>

            <CardActions>
                <Box
                    component="span"
                    sx={{
                        p: 1,
                        m: 1,
                    }}
                >

                    <Boton
                        variant="contained"
                        size="large"
                        disabled={busSeleccionado == null}
                        onClick={() => funcSetBusSeleccionado(null)}
                    >
                        Bus seleccionado: {busSeleccionado != null ? codigoBusSeleccionado : "ninguno"}
                        <IconoBasura
                            disabled={busSeleccionado == null}
                        />
                    </Boton>
                </Box>
            </CardActions>
        </Card>
    )
}

export default TarjetaBus