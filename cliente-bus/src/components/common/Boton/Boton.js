import React from 'react'
import Button from '@mui/material/Button';

const Boton = ({ children, disabled, size, color, variant, onClick }) => {
    return (
        <Button 
            className="boton"
            color= {color === null ? "primary" : color}
            disabled={disabled}
            size={size}
            variant={variant} // variant = contained, filled, outlined
            onClick={onClick}
        >
            {children}
        </Button>
    )
}

export default Boton
