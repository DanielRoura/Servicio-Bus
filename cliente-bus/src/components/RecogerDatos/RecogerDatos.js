import axios from 'axios';
import { Tiempo } from '../common/FuncionesTiempo/FuncionesTiempo';

// Variables de entorno
const api_url = process.env.REACT_APP_API_URL;


export const getLineasDisponibles = async (setCodigosLinea) => {
    const response = await axios.get(api_url + "/api/acciones/get_lineas_disponibles");
    setCodigosLinea([])
    setCodigosLinea(response.data)
    console.log("[RecogerDatos]: ", ["setCodigosLinea", response.data])
};

export const getForma = async (linea_seleccionada, setForma, setSegmentos) => {
    const response = await axios.get(api_url + "/api/acciones/get_forma/" + linea_seleccionada);
    setForma(null);
    setForma(response.data);
    setSegmentos(response.data.segmentos);
    console.log("[RecogerDatos]: ", ["getForma", response.data]);
};

export const getLinea = async (linea_seleccionada, setLinea) => {
    const response = await axios.get(api_url + "/api/acciones/get_linea/" + linea_seleccionada);
    setLinea(null)
    setLinea(response.data)
    console.log("[RecogerDatos]: ", ["getLinea", response.data])
};

export const getBuses = async (linea_seleccionada, setBuses, setCargando) => {
    const response = await axios.get(api_url + "/api/acciones/get_buses/" + linea_seleccionada);
    setBuses([])
    setBuses(response.data)
    console.log("[RecogerDatos]: ", ["getBuses", response.data])

    setCargando(false)
};

export const getUltimoLog = async (setFechaActualizacion) => {
    const response = await axios.get(api_url + "/api/acciones/get_ultimo_log");

    var ultimoLog = response.data

    if (ultimoLog != null) {
        var fecha = Tiempo(ultimoLog.$date).getSeconds() + 3;

        setFechaActualizacion(fecha)
        console.log("[RecogerDatos]: ", ["getUltimoLog", fecha])
    } else {
        console.log("[RecogerDatos]: ", ["getUltimoLog", null])
    }
};

export async function getMapaTiemposOld(linea_seleccionada, busSeleccionado, mapaTiempos, setMapaTiempos) {
    return new Promise((resolve, reject) => {
        if (linea_seleccionada === -1) {
            console.log("[RecogerDatos]: ", "Cambio de busSeleccionado")

            mapaTiempos.linea_analizada = null
            mapaTiempos.lista_lineas_analizadas = []
            mapaTiempos.informacion = []
            mapaTiempos.fecha_inicio = Tiempo()
        } else {
            const response = axios.post(api_url + "/api/datos/get_mapa_tiempos",
                {
                    "fecha_inicio": mapaTiempos.fecha_inicio,
                    "codigo_linea": linea_seleccionada,
                    "bus_seleccionado": busSeleccionado,
                    "linea_analizada": mapaTiempos.linea_analizada,
                    "lista_lineas_analizadas": mapaTiempos.lista_lineas_analizadas,
                }
            );

            mapaTiempos.lista_lineas_analizadas.push(mapaTiempos.linea_analizada)

            // listaMapaTiempos.push(response.data)
            setMapaTiempos(null)
            setMapaTiempos(response.data)

            console.log("[RecogerDatos]: ", ["getMapaTiempos", response.data])
        }
    })
};

export async function getMapaTiempos(linea_seleccionada, busSeleccionado, mapaTiempos, setMapaTiempos) {
    if (linea_seleccionada === -1) {
        console.log("[RecogerDatos]: ", "Cambio de busSeleccionado")

        mapaTiempos.linea_analizada = null
        mapaTiempos.lista_lineas_analizadas = []
        mapaTiempos.informacion = []
        mapaTiempos.fecha_inicio = Tiempo()
    } else {
        try {
            const response = await axios.post(api_url + "/api/datos/get_mapa_tiempos", {
                "fecha_inicio": mapaTiempos.fecha_inicio,
                "codigo_linea": linea_seleccionada,
                "bus_seleccionado": busSeleccionado,
                "linea_analizada": mapaTiempos.linea_analizada,
                "lista_lineas_analizadas": mapaTiempos.lista_lineas_analizadas,
            });

            mapaTiempos.lista_lineas_analizadas.push(mapaTiempos.linea_analizada);

            setMapaTiempos(response.data);

            console.log("[RecogerDatos]: ", ["getMapaTiempos", response.data]);
        } catch (error) {
            console.error(error);
        }
    }
}
