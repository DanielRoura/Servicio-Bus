import React from 'react'
import { Box, Grid, Typography } from '@mui/material';
import CopyrightIcon from '@mui/icons-material/Copyright';
import { Styler } from '../Styler/Styler';
// import Grid from '@mui/material/Grid'; y columnas

const api_url = process.env.REACT_APP_API_URL;

const PiePagina = () => {
  return (
    <Box>
      <Grid
        className='pie-pagina row'
        sx={Styler.piePagina}
      >

        <Grid item className='col'>
          <Typography
            variant="h7"
            color='primary'
            bgcolor='background.paper'
          >
            <CopyrightIcon
              sx={{ p: 1 }}
            />
            Daniel Roura Sepúlveda
          </Typography>
        </Grid>

        <Grid item className='col'>
          <Typography
            variant="h7"
            color='primary'
            bgcolor='background.paper'
          >
            <a href={api_url + "/api"}>
              Acceso a la API
            </a>
          </Typography>
        </Grid>

      </Grid>
    </Box>
  )
}

export default PiePagina
