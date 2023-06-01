import './App.css';
import Main from "./pages/Main/Main";
import MapaPage from './pages/Mapa/MapaPage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MenuSuperior from './components/MenuSuperior/MenuSuperior';
import PiePagina from './components/PiePagina/PiePagina';
import { ThemeProvider } from '@emotion/react';
import { createTheme } from '@mui/material';
import InfoPage from './pages/Informacion/InfoPage';

const optionesTema = {
  palette: {
    mode: 'light',
    primary: {
      main: '#A75353',
    },
    secondary: {
      main: '#B1D5DD',
    },
    terciary: {
      main: '#C4DBDF',
    },
    background: {
      default: '#DFDDDB',
      paper: '#DFDDDB',
    },
    info: {
      main: '#BDDFB3',
    },
    divider: '#BDDFB3',
  },
  typography: {
    fontSize: 16,
    fontFamily: [
      'Roboto',
      'sans-serif',
    ]
  },
  shape: {
    borderRadius: 5,
  }, 

};

export const tema = createTheme(optionesTema);


function App() {
  return (
    <ThemeProvider theme={tema}>

      <div className='cuerpo'>
        <BrowserRouter>
          <MenuSuperior />
          <Routes>
            <Route path="" element={<Main />} />
            <Route path="/mapa" element={<MapaPage />} />
            <Route path="/info" element={<InfoPage />} />
          </Routes>
        </BrowserRouter>
      </div>

      <PiePagina />

    </ThemeProvider>
  );
}

export default App;
