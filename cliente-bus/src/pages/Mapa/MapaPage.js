import React, { useEffect, useState, useRef, useCallback } from 'react';
import Titulo from '../../components/common/Titulo/Titulo';
import MapaDinamico from '../../components/MapaDinamico/MapaDinamico';
import SelectorLinea from '../../components/SelectorLinea/SelectorLinea';
import Tiempos from '../../components/Tiempos/Tiempos.js';
import SimboloCarga from '../../components/common/SimboloCarga/SimboloCarga';
import { getLineasDisponibles, getForma, getLinea, getBuses, getMapaTiempos, getUltimoLog } from '../../components/RecogerDatos/RecogerDatos';
import { Tiempo, TiempoMinutosSegundos, diferenciaEntreFechasSegundos, nuevoTiempo } from '../../components/common/FuncionesTiempo/FuncionesTiempo';
import { Box, Grid } from '@mui/material';
import TarjetaParada from '../../components/Tarjetas/TarjetaParada';
import TarjetaBus from '../../components/Tarjetas/TarjetaBus';

const lineaPorDefecto = 11;
const valorPredeterminadoMapaTiempos = {
    "linea_analizada": null,
    "lista_lineas_analizadas": [],
    "fecha_inicio": Tiempo(),
    "informacion": []
}

const MapaPage = () => {
    const [codigosLinea, setCodigosLinea] = useState([lineaPorDefecto])
    const [lineaSeleccionada, setLineaSeleccionada] = useState(lineaPorDefecto)
    const [cargando, setCargando] = useState(true)

    function seleccionarLinea(nueva_linea) {
        if (nueva_linea !== lineaSeleccionada) {
            setLineaSeleccionada(nueva_linea);
            setBuses([]);

            setParadaSeleccionada(null);
            setParadaAnalizada(null);

            setCargando(true);
            setMapaTiempos(valorPredeterminadoMapaTiempos);

            funcSetBusSeleccionado(null);
        }
    }

    const [codigoBusSeleccionado, setCodigoBusSeleccionado] = useState(null)
    const [busSeleccionado, setBusSeleccionado] = useState(null)
    const [busPrediccion, setBusPrediccion] = useState(null)
    const [mapaTiempos, setMapaTiempos] = useState(valorPredeterminadoMapaTiempos)

    const [paradaSeleccionada, setParadaSeleccionada] = useState(null)
    const [paradaAnalizada, setParadaAnalizada] = useState(null)

    const [linea, setLinea] = useState(null)
    const [forma, setForma] = useState(null)
    const [segmentos, setSegmentos] = useState([])
    const [buses, setBuses] = useState([])
    const [fechaActualizacion, setFechaActualizacion] = useState(null)

    /* - - - - - - - - - - - - - - - - - - - - Seleccionar Parada - - - - - - - - - - - - - - - - - - - - */
    const funcSetParadaSeleccionada = useCallback(async (nuevoCodigoParada) => {
        var nuevaParada = null;
        console.log("[MapaPage]: ", ["funcSetParadaSeleccionada", nuevoCodigoParada], TiempoMinutosSegundos())

        if (nuevoCodigoParada != null) {
            linea.paradas.forEach((parada) => {
                if (parada.codigo_parada === nuevoCodigoParada) {
                    nuevaParada = parada;
                }
            });
        }

        if (paradaSeleccionada != null && paradaSeleccionada.codigo_parada === nuevoCodigoParada) {
            console.log("[MapaPage]: ", " ParadaSeleccionada sin cambio", TiempoMinutosSegundos())
        } else {
            console.log("[MapaPage]: ", " ParadaSeleccionada de: "
                + (paradaSeleccionada != null ? paradaSeleccionada.codigo_parada : "ninguna")
                + " a:" + nuevoCodigoParada, TiempoMinutosSegundos())
            setParadaSeleccionada(nuevaParada);
        }
        console.log("[MapaPage]: ", " aaaaaa", mapaTiempos, TiempoMinutosSegundos())

        if (mapaTiempos.linea_analizada != null) {
            setParadaAnalizada(mapaTiempos.linea_analizada.paradas.find(p => p.codigo_parada === nuevoCodigoParada));
        } else {
            setParadaAnalizada(null); //
        }
    }, [linea, paradaSeleccionada, mapaTiempos, setParadaSeleccionada]);

    
    /* - - - - - - - - - - - - - - - - - - - - Seleccionar Bus - - - - - - - - - - - - - - - - - - - - */
    const funcSetBusSeleccionado = useCallback(async (nuevoCodigoBus) => {
        var nuevoBus = null;
        console.log("[MapaPage]: ", ["funcSetBusSeleccionado", nuevoCodigoBus], TiempoMinutosSegundos())

        if (nuevoCodigoBus != null) {
            buses.forEach((bus) => {
                if (bus.codigo_bus === nuevoCodigoBus) {
                    nuevoBus = bus;
                }
            });
        }

        if (nuevoBus != null) {
            if (nuevoCodigoBus === codigoBusSeleccionado) {
                // console.log("[MapaPage]: ", " BusSeleccionado actualizado", TiempoMinutosSegundos())
                getMapaTiempos(lineaSeleccionada, nuevoBus, mapaTiempos, setMapaTiempos);
            } else {
                console.log("[MapaPage]: ", " BusSeleccionado de: " + codigoBusSeleccionado + " a:" + nuevoCodigoBus, TiempoMinutosSegundos())
                setCodigoBusSeleccionado(nuevoCodigoBus);
                setMapaTiempos(null)
                await getMapaTiempos(-1, null, mapaTiempos, setMapaTiempos);
                setMapaTiempos(valorPredeterminadoMapaTiempos)
                await getMapaTiempos(lineaSeleccionada, nuevoBus, mapaTiempos, setMapaTiempos);
                setBusPrediccion(null);
            }
        } else {
            setCodigoBusSeleccionado(null)
            await getMapaTiempos(-1, null, mapaTiempos, setMapaTiempos);
            setBusPrediccion(null);
        }

        setBusSeleccionado(nuevoBus);
        if (paradaSeleccionada != null) {
            funcSetParadaSeleccionada(paradaSeleccionada.codigo_parada);
        }

    }, [codigoBusSeleccionado, buses, lineaSeleccionada, mapaTiempos, paradaSeleccionada, setBusSeleccionado, setCodigoBusSeleccionado, setMapaTiempos, funcSetParadaSeleccionada]);


    // ID del intervalo 
    /* https://www.w3schools.com/react/react_useref.asp */
    let intervalId = useRef(0); // Debería guardar el valor entre renders usando .current

    useEffect(() => {
        // Almacenar el ID del intervalo
        intervalId.current = setInterval(() => {

            var ahoraSegundos = Tiempo().getSeconds();

            if (ahoraSegundos === fechaActualizacion) {
                console.log("[MapaPage]: ", " Renovar buses y cambiar el seleccionado ", TiempoMinutosSegundos());
                getBuses(lineaSeleccionada, setBuses, setCargando);
                funcSetBusSeleccionado(codigoBusSeleccionado);
            }

        }, 1000);

        return () => clearInterval(intervalId.current);
    }, [fechaActualizacion, setFechaActualizacion, busSeleccionado, lineaSeleccionada, codigoBusSeleccionado, funcSetBusSeleccionado]);


    /* - - - - - - - - - - - - - - - - - - - - Get Datos - - - - - - - - - - - - - - - - - - - - */
    useEffect(() => {
        if (cargando) {
            getLineasDisponibles(setCodigosLinea);
            getLinea(lineaSeleccionada, setLinea);
            getForma(lineaSeleccionada, setForma, setSegmentos);
            getBuses(lineaSeleccionada, setBuses, setCargando);
            getUltimoLog(setFechaActualizacion);
        }
    }, [cargando, lineaSeleccionada, setLinea, setForma, setSegmentos, setBuses, setCargando, setFechaActualizacion]);


    /* - - - - - - - - - - - - - - - - - - - - Bus Prediccion - - - - - - - - - - - - - - - - - - - - */
    const funcSetBusPrediccion = useCallback((nuevoBusPrediccion) => {
        if (nuevoBusPrediccion != null && mapaTiempos != null && mapaTiempos.linea_analizada != null) {
            // console.log("[MapaPage]: ", "funcSetBusPrediccion ", TiempoMinutosSegundos())
            var ahora = Tiempo();
            var diffTiempo = diferenciaEntreFechasSegundos(ahora, nuevoTiempo(nuevoBusPrediccion.fecha_actualizacion));
            var segmento = null;
            var inicio = null;
            var tiempo_segmento = null;
            var parada = null;

            for (var i = 0; i < segmentos.length * 3; i++) {
                segmento = segmentos[i % segmentos.length];

                if (segmento.orden === nuevoBusPrediccion.orden_segmento && segmento.sentido === nuevoBusPrediccion.sentido) {
                    inicio = true;
                }

                if (inicio) {
                    let codigo_parada = null;
                    if (segmento.codigo_proxima_parada === null) {
                        codigo_parada = segmento.codigo_parada;
                    } else {
                        codigo_parada = segmento.codigo_proxima_parada;
                    }

                    parada = mapaTiempos.linea_analizada.paradas.find(p => p.codigo_parada === codigo_parada);
                    // console.log(parada)

                    if (parada != null) {
                        tiempo_segmento = segmento.distancia / (parada.velocidad_media_aritmetica);
                        if (tiempo_segmento > diffTiempo) {
                            // console.log(i, diffTiempo, tiempo_segmento)

                            nuevoBusPrediccion.orden_segmento = segmento.orden;
                            nuevoBusPrediccion.sentido = segmento.sentido;
                            break;
                        } else {
                            diffTiempo -= tiempo_segmento;
                        }
                    }
                }
            }

            if (parada == null) {
                setBusPrediccion(null);
                console.log("[MapaPage]: ", "Error en la predicción del bus: PARADA NULA", TiempoMinutosSegundos());
                return;
            }
            // Coordanada del segmento por donde va el bus
            let vector_coordenadas = [
                segmento.latitud_2 - segmento.latitud_1,
                segmento.longitud_2 - segmento.longitud_1
            ];

            // Vector normalizado
            vector_coordenadas = [
                vector_coordenadas[0] / segmento.distancia,
                vector_coordenadas[1] / segmento.distancia
            ]

            let distancia_recorrida = parada.velocidad_media_aritmetica * diffTiempo;
            nuevoBusPrediccion.latitud = segmento.latitud_1 + vector_coordenadas[0] * distancia_recorrida;
            nuevoBusPrediccion.longitud = segmento.longitud_1 + vector_coordenadas[1] * distancia_recorrida;

            // console.log("segmento", segmento.orden)
            // console.log("nuevoBusPrediccion", nuevoBusPrediccion.orden_segmento)

            setBusPrediccion(nuevoBusPrediccion)
        } else {
            setBusPrediccion(null);
        }
    }, [mapaTiempos, setBusPrediccion, segmentos]);


    let intervalId_Prediccion = useRef(0); // Debería guardar el valor entre renders usando .current

    useEffect(() => {
        intervalId_Prediccion.current = setInterval(() => {
            // console.log("[MapaPage]: ", "busPrediccion ", TiempoMinutosSegundos())
            funcSetBusPrediccion({ ...busSeleccionado });
        }, 5000 / 2);

        return () => clearInterval(intervalId_Prediccion.current);
    }, [funcSetBusPrediccion, busSeleccionado]);

    return (
        <div
            className="container-xxl"
        >
            <Grid
                container
                direction="row"
                justifyContent="flex-start"
                alignItems="flex-end"
            >
                <Grid item xs={10} sm={10} md={11} l={11}>
                    <Titulo
                        texto="Mapa de paradas de la Ciudad de Málaga"
                    />
                </Grid>

                <Grid item xs={2} sm={2} md={1} l={1}>
                    <SelectorLinea
                        codigosLinea={codigosLinea}
                        seleccionarLinea={seleccionarLinea}
                        lineaSeleccionada={lineaSeleccionada}
                    />
                </Grid>

            </Grid>


            {linea != null && forma != null ?
                <>
                    <Grid
                        container
                        direction="row"
                        justifyContent="center"
                        alignItems="left"
                        spacing={3}
                        sx={{
                            padding: { xs: 2 },
                            paddingRight: { xs: 0, sm: 2 },
                            paddingLeft: { xs: 0, sm: 2 }
                        }}
                    >

                        <Grid item xs={12} sx={11}>
                            <MapaDinamico
                                buses={buses}
                                linea={linea}
                                segmentos={segmentos}
                                busSeleccionado={busSeleccionado}
                                busPrediccion={busPrediccion}
                                funcSetBusSeleccionado={funcSetBusSeleccionado}
                                funcSetParadaSeleccionada={funcSetParadaSeleccionada}
                            />
                        </Grid>

                    </Grid>

                    <Box
                        sx={{
                            margin: {
                                xs: '0px',
                                sm: '0px',
                                md: '50px',
                            },
                        }}
                    >

                        <Titulo
                            texto="Cuadro de mandos"
                        />

                        <Grid
                            container
                            direction="row"
                            justifyContent="center"
                            // justifyContent="flex-start"
                            // alignItems="center"
                            sx={{
                                spacing: { sm: 0, md: 3, l: 3 },
                            }}

                        >

                            <Grid item xs={12} sm={12} md={6}>
                                <Box>
                                    <TarjetaBus
                                        paradas={linea.paradas}
                                        busSeleccionado={busSeleccionado}
                                        codigoBusSeleccionado={codigoBusSeleccionado}
                                        funcSetBusSeleccionado={funcSetBusSeleccionado}
                                        direccion={busSeleccionado != null ? (busSeleccionado.sentido === 1 ? linea.cabecera_vuelta : linea.cabecera_Ida) : null}
                                    />
                                </Box>
                            </Grid>

                            <Grid item xs={12} sm={12} md={6} >
                                <Box>
                                    <TarjetaParada
                                        linea={linea}
                                        paradaSeleccionada={paradaSeleccionada}
                                        paradaAnalizada={paradaAnalizada}
                                        setParadaSeleccionada={setParadaSeleccionada}
                                    />
                                </Box>
                            </Grid>

                        </Grid>

                        {busSeleccionado != null ?
                            <div>
                                {mapaTiempos === null || mapaTiempos.linea_analizada === null ?
                                    <>
                                        <SimboloCarga />
                                    </>
                                    :
                                    <Tiempos
                                        busSeleccionado={busSeleccionado}
                                        linea_analizada={mapaTiempos.linea_analizada}
                                        funcSetParadaSeleccionada={funcSetParadaSeleccionada}
                                    />
                                }
                            </div>
                            :
                            null
                        }
                    </Box>
                </>
                :
                <SimboloCarga />
            }




        </div>
    )
}

export default MapaPage