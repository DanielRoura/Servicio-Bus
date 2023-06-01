import { Box, Card, CardActions, CardContent, Typography } from '@mui/material'
import React from 'react'
import { IconoBasura } from '../common/Iconos/Iconos'
import { parseSegundosATiempos, parseTiempo } from '../common/FuncionesTiempo/FuncionesTiempo'
import Boton from '../common/Boton/Boton'
import { Styler } from '../Styler/Styler'

const TarjetaParada = ({ linea, paradaAnalizada, paradaSeleccionada, setParadaSeleccionada }) => {

    return (
        <Card
            className="tarjeta"
            sx={Styler.tarjeta}>
            <CardContent>
                <Typography variant="h5" color="text.secondary">
                    {paradaSeleccionada != null ? paradaSeleccionada.nombre_parada : "Parada no seleccionada"}
                </Typography>

                <Typography variant="body2" color="text.secondary">
                    Código: {paradaSeleccionada != null ? paradaSeleccionada.codigo_parada : null}
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
                        Dirección: {(paradaSeleccionada != null && linea != null ) ? 
                            paradaSeleccionada.sentido === 2 ? linea.cabecera_Ida : linea.cabecera_vuelta
                            : ""}
                    </p>
                    <p>
                        Fecha de llegada: {paradaAnalizada != null ? parseTiempo(paradaAnalizada.fecha_llegada) : ""}
                    </p>
                    <p>
                        Tiempo para llegar: {paradaAnalizada != null ? (paradaAnalizada.tiempo_acumulado != null ? (parseSegundosATiempos(paradaAnalizada.tiempo_acumulado)) : "ya ha llegado") : ""}
                    </p>
                </Box>

            </CardContent>

            <CardActions>
                <Box
                    component="span"
                    sx={{
                        padding: 1,
                        margin: 1,
                    }}
                >

                    <Boton
                        variant="contained"
                        color="primary"
                        size="large"
                        disabled={paradaSeleccionada == null}
                        onClick={() => setParadaSeleccionada(null)}
                    >
                        Quitar parada: {paradaSeleccionada != null ? paradaSeleccionada.codigo_parada : "Ninguna"}
                        <IconoBasura
                            disabled={paradaSeleccionada == null}
                        />
                    </Boton>
                </Box>
            </CardActions>
        </Card>
    )
}

export default TarjetaParada