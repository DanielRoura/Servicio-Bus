import L from 'leaflet';

export function marcadorIcon() {
    return L.icon({
        iconUrl: require("../../../static/images/marcador.png"),
        iconSize: [50, 50],
    });
};

export function bus1Icon() {
    return L.icon({
        iconUrl: require("../../../static/images/bus1mini.png"),
        iconSize: [50, 50],
    });
};

export function bus2Icon() {
    return L.icon({
        iconUrl: require("../../../static/images/bus2mini.png"),
        iconSize: [50, 50],
    });
};

export function bus1IconPred() {
    return L.icon({
        iconUrl: require("../../../static/images/bus1miniFantasma.png"),
        iconSize: [50, 50],
    });
};

export function bus2IconPred() {
    return L.icon({
        iconUrl: require("../../../static/images/bus2miniFantasma.png"),
        iconSize: [50, 50],
    });
};


export function bus1IconSel() {
    return L.icon({
        iconUrl: require("../../../static/images/bus1miniSel.png"),
        iconSize: [50, 50],
    });
};

export function bus2IconSel() {
    return L.icon({
        iconUrl: require("../../../static/images/bus2miniSel.png"),
        iconSize: [50, 50],
    });
};

export function paradaIcon() {
    return L.icon({
        iconUrl: require("../../../static/images/parada.png"),
        iconSize: [25, 25],
    });
};