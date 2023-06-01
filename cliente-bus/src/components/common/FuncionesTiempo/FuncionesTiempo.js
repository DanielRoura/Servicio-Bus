export function Tiempo() {
    return new Date()
}

export function nuevoTiempo(str_Tiempo) {
    return new Date(str_Tiempo);
}

export function TiempoAbs() {
    return new Date().getTime()
};

export function nuevoTiempoAbs(fecha) {
    return fecha.getTime()
};

export function TiempoMinutosSegundos() {
    var ahora = new Date()
    return (ahora.getHours() < 10 ? "0" + ahora.getHours() : ahora.getHours()) + ":" +
        (ahora.getMinutes() < 10 ? "0" + ahora.getMinutes() : ahora.getMinutes()) + ":" +
        (ahora.getSeconds() < 10 ? "0" + ahora.getSeconds() : ahora.getSeconds())
};

export function parseTiempo(str_Tiempo) {
    var tiempo = new Date(str_Tiempo)
    var horas = tiempo.getHours()
    if (horas < 10) {
        horas = "0" + horas
    }

    var minutos = tiempo.getMinutes()
    if (minutos < 10) {
        minutos = "0" + minutos
    }

    var segundos = tiempo.getSeconds()
    if (segundos < 10) {
        segundos = "0" + segundos
    }

    return horas + ":" + minutos + ":" + segundos;
}

export function parseTiempoAjustado(str_Tiempo) {
    var tiempo = new Date(str_Tiempo)
    var horas = tiempo.getHours() - 2
    if (horas < 10) {
        horas = "0" + horas
    }

    var minutos = tiempo.getMinutes()
    if (minutos < 10) {
        minutos = "0" + minutos
    }

    var segundos = tiempo.getSeconds()
    if (segundos < 10) {
        segundos = "0" + segundos
    }

    return horas + ":" + minutos + ":" + segundos;
}

export function parseSegundosATiempos(segundos) {
    if (segundos === null) {
        return ""
    }

    var horas = Math.floor(segundos / 3600);
    if (horas < 10) {
        horas = "0" + horas;
    }

    var minutos = Math.floor((segundos % 3600) / 60);
    if (minutos < 10) {
        minutos = "0" + minutos;
    }

    var segundosRestantes = segundos % 60;
    if (segundosRestantes < 10) {
        segundosRestantes = "0" + segundosRestantes;
    }

    if (horas === 0 && minutos === 0 && segundosRestantes === 0) {
        return "";
    }

    return horas + ":" + minutos + ":" + segundosRestantes;
}


export function diferenciaFechasEnSegundos(millis1, millis2) {
    const diffMillis = Math.abs(millis2 - millis1);
    return Math.floor(diffMillis / 1000);
}

export function diferenciaEntreFechasSegundos(fecha_final, fecha_inicial) {
    var tiempo_incial = fecha_inicial.getMinutes() * 60 + fecha_inicial.getSeconds()
    var tiempo_final = fecha_final.getMinutes() * 60 + fecha_final.getSeconds()
    var diff = tiempo_final - tiempo_incial
    if (diff < 0) {
        diff += 3600;
    }

    // console.log("[FuncionesTiempo]: ", ["diferenciaEntreFechasSegundos", diff, tiempo_incial, fecha_inicial.getMinutes() +":" + fecha_inicial.getSeconds(), tiempo_final, fecha_final.getMinutes() +":" + fecha_final.getSeconds()])
    return diff;
}