import React, { useEffect, useState, useCallback } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { TiempoAbs, nuevoTiempo, parseTiempo, parseSegundosATiempos, TiempoMinutosSegundos } from '../common/FuncionesTiempo/FuncionesTiempo';
import { IconosInterrogacion, IconosTresPuntos, IconoBusEstado, IconoCorrecto, IconoIncorrecto } from '../common/Iconos/Iconos';
import { Tooltip } from '@mui/material';
import { Styler } from '../Styler/Styler';
import Titulo from '../common/Titulo/Titulo';

// eslint-disable-next-line no-unused-vars
const visibilidadColumnasDebug =
{
    id: false,
    estado: true,
    codigoParada: true,
    tiempoProximaParada: true,
    tiempoAcumulado: true,
    tiempoAcumuladoSegundos: false,
    fechaLlegadaAproximada: true,
    fechaLlegadaReal: true,
    fechaLlegadaArreglada: true,
    tiempoMedioParada: true,
    tiempoMedioParadaSegundos: true,
    tendencia: true,
    diferenciaPrediccion: true,
    error: true,
    velocidad_media: true,
    velocidad_desviacion_tipica: true,
    distanciaProximaParada: true,
    proporcionEnParada: true,
    tooltip: false,
}

// eslint-disable-next-line no-unused-vars
const visibilidadColumnasUsuario =
{
    id: false,
    estado: true,
    codigoParada: true,
    tiempoProximaParada: false,
    tiempoAcumulado: true,
    tiempoAcumuladoSegundos: false,
    fechaLlegadaAproximada: true,
    fechaLlegadaReal: true,
    fechaLlegadaArreglada: false,
    tiempoMedioParada: false,
    tiempoMedioParadaSegundos: false,
    tendencia: false,
    diferenciaPrediccion: false,
    error: false,
    velocidad_media: false,
    velocidad_desviacion_tipica: false,
    distanciaProximaParada: false,
    proporcionEnParada: false,
    tooltip: false,
}

const Tiempos = ({ busSeleccionado, linea_analizada, funcSetParadaSeleccionada }) => {
    const [filaSeleccionada, setFilaSeleccionada] = useState(null);
    const [filas, setFilas] = useState([]);
    const [columnas, setColumnas] = useState([]);
    const [visibilidadColumnas] = useState(visibilidadColumnasUsuario);

    const handleParadaSeleccionada = (fila) => {
        setFilaSeleccionada(fila.id);
        console.log("[Tiempos]: ", "Parada Seleccionada: ", fila.row.codigoParada, TiempoMinutosSegundos());
        funcSetParadaSeleccionada(fila.row.codigoParada);
    };


    const calcularEstado = useCallback((ahora, fecha_llegada_T, fecha_llegada_real_T, codigo_parada, error, estaPasadaLaParada) => {
        if (busSeleccionado.codigo_proxima_parada === codigo_parada) {
            return <IconoBusEstado llegada={estaPasadaLaParada} />;
        }

        if (fecha_llegada_real_T == null) {
            if (ahora >= fecha_llegada_T) {
                return <IconosInterrogacion />;
            } else {
                return <IconosTresPuntos />;
            }
        } else {
            // Como ya se ha llegado --> Mirar si la predicción está bien

            // Si la predicción está a menos de 30 segundos de la real está bien
            if (Math.abs(fecha_llegada_T - fecha_llegada_real_T) < 30000) {
                return <IconoCorrecto />;
            } else {
                return <IconoIncorrecto error={error} />;
            }

            // return " null "
        }
    }, [busSeleccionado.codigo_proxima_parada]);

    function parseTendencia(tendencia) {
        var tendenciaAux
        switch (tendencia) {
            case 1:
                tendenciaAux = "Frenando"
                break;
            case -1:
                tendenciaAux = "Adelantando"
                break;
            case 2:
                tendenciaAux = "Cambiando conductor"
                break;
            default:
                tendenciaAux = "Constante"
                break;
        }

        return tendenciaAux
    }

    const establecerFila = useCallback((parada, ahora, idx) => {
        var fecha_llegada_T = nuevoTiempo(parada.fecha_llegada)
        var fecha_llegada_real_T = parada.fecha_llegada_real != null ? nuevoTiempo(parada.fecha_llegada_real) : null
        var estaPasadaLaParada = fecha_llegada_real_T != null || ahora >= fecha_llegada_T

        var estado = calcularEstado(ahora, fecha_llegada_T, fecha_llegada_real_T, parada.codigo_parada, parada.error, estaPasadaLaParada);
        var tiempoProximaParada = estaPasadaLaParada ? null : parada.tiempo_proxima_parada;
        var distanciaProximaParada = Math.round(parada.distancia_proxima_parada) + "m";
        var tiempoAcumulado = parseSegundosATiempos(parada.tiempo_acumulado);
        var tiempoAcumuladoSegundos = parada.tiempo_acumulado;
        var fechaLlegadaAproximada = parseTiempo(parada.fecha_llegada);
        var fechaLlegadaReal = fecha_llegada_real_T != null ? parseTiempo(parada.fecha_llegada_real) : null;
        var tiempoMedioParada = parada.str_tiempo_medio_parada;
        var tiempoMedioParadaSegundos = parada.tiempo_medio_parada;
        var proporcionEnParada = parada.proporcion_en_parada;
        var tendencia = estaPasadaLaParada ? null : parseTendencia(parada.tendencia);
        var diferenciaPrediccion = estaPasadaLaParada ? null : parada.diferencia_prediccion;
        var error = parada.error == null ? "" : parada.error + "s";
        var velocidad_media = parada.velocidad_media_aritmetica;
        var velocidad_desviacion_tipica = parada.velocidad_desviacion_tipica;

        /* - - - - - */

        var fila = {
            id: idx,
            estado: estado,
            codigoParada: parada.codigo_parada,
            nombreParada: parada.nombre_parada,
            tiempoProximaParada: tiempoProximaParada,
            tiempoAcumulado: tiempoAcumulado,
            tiempoAcumuladoSegundos: tiempoAcumuladoSegundos,
            fechaLlegadaAproximada: fechaLlegadaAproximada,
            fechaLlegadaReal: fechaLlegadaReal,
            tiempoMedioParada: tiempoMedioParada,
            tiempoMedioParadaSegundos: tiempoMedioParadaSegundos,
            tendencia: tendencia,
            diferenciaPrediccion: diferenciaPrediccion,
            error: error,
            tooltip: "tooltip",
            velocidad_media: velocidad_media,
            velocidad_desviacion_tipica: velocidad_desviacion_tipica,
            distanciaProximaParada: distanciaProximaParada,
            proporcionEnParada: proporcionEnParada,

            fechaLlegadaArreglada: parada.fecha_llegada_arreglada != null ? parseTiempo(parada.fecha_llegada_arreglada) : null,
        }
        return fila
    }, [calcularEstado]);


    useEffect(() => {
        if (busSeleccionado != null) {
            var ahora = TiempoAbs();
            console.log("[Tiempos]: ", ["setFilas", ahora, linea_analizada.paradas[0].fecha_llegada, nuevoTiempo(linea_analizada["paradas"][0]), ahora >= nuevoTiempo(linea_analizada["paradas"][0])])
            setFilas(
                linea_analizada["paradas"].map((parada, idx) => (
                    establecerFila(parada, ahora, idx)
                ))
            );

            setColumnas(
                [
                    {
                        field: "id", headerName: "Id", width: 20, sortable: false
                    },
                    {
                        field: "tooltip", headerName: "Tooltip", width: 60, sortable: false,
                        renderCell: (params) => (
                            <div>
                                <Tooltip title={params.value}>
                                    <div>
                                        {params.value}
                                    </div>
                                </Tooltip>
                            </div>
                        ),
                    },
                    {
                        field: "estado", headerName: "Estado", width: (visibilidadColumnas === visibilidadColumnasUsuario ? 90 : 60), sortable: false,
                        renderCell: (params) => (
                            <div>
                                {params.value}
                            </div>
                        )
                    },
                    {
                        field: "codigoParada", headerName: "Código", width: (visibilidadColumnas === visibilidadColumnasUsuario ? 100 : 70), sortable: false
                    },
                    {
                        field: "nombreParada", headerName: "Nombre", width: (visibilidadColumnas === visibilidadColumnasUsuario ? 420 : 260), sortable: false
                    },
                    {
                        field: "tiempoProximaParada", headerName: "Intervalo", width: 80
                    },
                    {
                        field: "distanciaProximaParada", headerName: "Distancia próx. par.", width: 140
                    },
                    {
                        field: "tiempoAcumulado", headerName: "Tiempo restante", width: (visibilidadColumnas === visibilidadColumnasUsuario ? 190 : 120)
                    },
                    {
                        field: "tiempoAcumuladoSegundos", headerName: "Tiempo acumulado (segundos)", width: 200
                    },
                    {
                        field: "fechaLlegadaAproximada", headerName: "Predicción de llegada", width: (visibilidadColumnas === visibilidadColumnasUsuario ? 190 : 160)
                    },
                    {
                        field: "fechaLlegadaArreglada", headerName: "FPredicción con tendencia", width: 160
                    },
                    {
                        field: "fechaLlegadaReal", headerName: "Fecha de llegada", width: (visibilidadColumnas === visibilidadColumnasUsuario ? 190 : 140)
                    },
                    {
                        field: "diferenciaPrediccion", headerName: "Diff. predicciones", width: 140
                    },
                    {
                        field: "tendencia", headerName: "Tendencia", width: 120
                    },
                    {
                        field: "tiempoMedioParada", headerName: "Tiempo medio parada", width: 200
                    },
                    {
                        field: "error", headerName: "Error de predicción", width: 200
                    },
                    {
                        field: "tiempoMedioParadaSegundos", headerName: "Tiempo medio parada (segundos)", width: 200
                    },
                    {
                        field: "proporcionEnParada", headerName: "Proporcion en parada", width: 140
                    },
                    {
                        field: "velocidad_media", headerName: "Velocidad media", width: 120
                    },
                    {
                        field: "velocidad_desviacion_tipica", headerName: "Velocidad desv. típ.", width: 140
                    }
                ]
            )

            
        }

        console.log("[Tiempos]: ", ["useEffect con línea analizada: ", linea_analizada])
    }, [busSeleccionado, visibilidadColumnas, linea_analizada, establecerFila]);

    return (
        <div style={{ width: '100%', flex: '1 1 auto', overflow: 'auto' }}>
            <Titulo
                sx={{ padding: "25px" }}
                texto={"Tabla de tiempos"}
            />

            <DataGrid
                sx={Styler.tiempos}
                rows={filas}
                columns={columnas}
                columnVisibilityModel={visibilidadColumnas}
                hideFooter={true}
                hideFooterPagination
                disableSelectionOnClick
                selecionModel={filaSeleccionada != null ? [filaSeleccionada] : []}
                density="dense"
                onRowClick={(fila) => {
                    handleParadaSeleccionada(fila);
                }}
            />

        </div>
    )
};

export default Tiempos;