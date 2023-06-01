import React from 'react'
import parada from "../../static/images/parada.png"
import { Styler } from '../Styler/Styler'
import { useNavigate } from 'react-router-dom';
import { Grid, MenuItem } from '@mui/material';

const apartados = [
    { id: 1, label: 'Mapa de paradas', route: '/mapa' },
    // { id: 2, label: 'Información', route: '/info' },
];

const MenuSuperior = () => {
    const navigate = useNavigate();

    return (
        <div className="menu-superior" sx={Styler.menu_superior}>
            <div className='contenedor-logo'>
                <div className="fondo-logo">
                    <div className="logo">
                        <img src={parada} alt="Logo de la página" />
                    </div>
                </div>

            </div>

            <Grid
                container
                direction="row"
                justifyContent="flex-start"
                alignItems="center"
                spacing={0}
            >

                {apartados.map((item, index) => (
                    <Grid item>
                        <MenuItem
                            key={'menuItem'+item.id}
                            onClick={() => navigate(item.route)}
                        >
                            {item.label}
                            <div
                                primary={item.label}
                            />
                        </MenuItem>
                    </Grid>
                ))}

                <div className="spacer" />
                
                <div className="login">
                    {/* Aquí iría el botón de inicio de sesión con Google */}
                </div>
            </Grid>
        </div >
    )
}

export default MenuSuperior
