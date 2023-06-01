import React from 'react'
import CircularProgress from '@mui/material/CircularProgress';

const SimboloCarga = () => {
    return (
        <div className='simbolo-cargando'>
            <CircularProgress 
            color='primary'
            size={60} />
        </div>
    )
}

export default SimboloCarga