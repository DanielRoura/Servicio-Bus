import { React } from 'react';
import InputLabel from '@mui/material/InputLabel';
import Box from '@mui/material/Box';
import NativeSelect from '@mui/material/NativeSelect';


const SelectorLinea = ({ codigosLinea, seleccionarLinea, lineaSeleccionada }) => {
    if (codigosLinea == null) {
    } else {
        return (
            <Box>
                <InputLabel variant="standard" htmlFor="uncontrolled-native">
                    Línea
                </InputLabel>
                <NativeSelect
                    onChange={(nueva_linea) => seleccionarLinea(nueva_linea.target.value)}
                    value={lineaSeleccionada}
                    inputProps={{
                        name: 'age',
                        id: 'uncontrolled-native',
                    }}
                >
                    {codigosLinea != null ? codigosLinea.map((codigo_linea, idx) =>
                        <option
                            value={codigo_linea}
                            key={idx}
                        >
                            {codigo_linea}
                        </option>
                    ) : null}
                </NativeSelect>
            </Box>
        )
    }
}

export default SelectorLinea
