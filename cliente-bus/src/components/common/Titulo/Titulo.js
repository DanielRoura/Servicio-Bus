import React from 'react'
import { Typography } from '@mui/material';

const Titulo = ({ texto }) => {
    return (
        <div className="titulo" style={{marginTop: '30px'}}>
            <Typography
                variant="h3 overline"
                color='black'
            >
                <h1>
                    {texto}
                </h1>
            </Typography>
        </div>
    )
}

export default Titulo
