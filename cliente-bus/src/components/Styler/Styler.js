/* https://zenoo.github.io/mui-theme-creator/#Menu */

const color1 = "#B1D5DD"; // light blue
const color2 = "#C4DBDF"; // columbia blue
const color3 = "#BDDFB3"; // celadon
const color4 = "#A75353"; // redwood 
const color5 = "#DFDDDB"; // platinum

export const Styler = {
    colores: {
        color1: color1,
        color2: color2,
        color3: color3,
        color4: color4,
        color5: color5,
    },
    piePagina: {
        height: '100%',
        width: '100%',
    },
    tiempos: {
        height: '100%',
        border: 4,
        borderRadius: 3,
        borderColor: 'primary.main',
        '& .MuiDataGrid-row:hover': {
            color: 'primary.main',
            backgroundColor: 'info.main',
        },
        padding: "1px",
        margin: "15px",
        display: "show",
        boxShadow: '0 10px 15px 0 rgba(0, 0, 0, 0.26)',
    },
    tarjeta: {
        height: '100%',
        border: 4,
        borderRadius: 3,
        borderColor: 'primary.main',
        padding: "1px",
        margin: "15px",
        display: "show",
        boxShadow: '0 10px 15px 0 rgba(0, 0, 0, 0.26)',
    },
    boton: {
        color: color1,
    },
    menu_superior: {
        height: '100%',
    },
    tabla: {
        width: "100%"
    },
    pads: {
        marginLeft: '3px',
        marginRight: '3px',
        marginBottom: '12px',
        padding: "5px"
    },
    titulo: {
        padding: "1px",
    },
    mapa: {
        m: "20px",
        border: 4,
        borderRadius: 2,
        boxShadow: '0 10px 15px 0 rgba(0, 0, 0, 0.26)',
        borderColor: 'primary.main',
        marginLeft: '3px',
        marginRight: '6px',
        marginBottom: '6px'
    },
    loading: {
        padding: '100px',
        align: "center"
    },
    page: {
        padding: '20px',
        marginLeft: '30px',
        marginRight: '30px',
        marginBottom: '50px',
    },
    icons: {
        color: 'rgba(255, 255, 255, 0.7)!important',
        marginLeft: '20px',
    }
};