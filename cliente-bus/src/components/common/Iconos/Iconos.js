import React from 'react'
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import DirectionsBusTwoToneIcon from '@mui/icons-material/DirectionsBusTwoTone';
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';
import ErrorIcon from '@mui/icons-material/Error';
import { Tooltip } from '@mui/material';
import Zoom from '@mui/material/Zoom';
import DeleteIcon from '@mui/icons-material/Delete';

/* https://mui.com/material-ui/react-tooltip/ */

export const IconoBasura = ({disabled}) => {
    return (
        <div>
            <Tooltip
                describeChild
                leaveDelay={500}
                TransitionComponent={Zoom}
                title="Quitar selección"
            >
                <DeleteIcon
                    sx={{m: '3px'}}
                    color= {disabled ? "primary" : "info"}
                />
            </Tooltip>
        </div>

    )
}

export const IconosInterrogacion = () => {
    return (
        <div>
            <Tooltip
                describeChild
                leaveDelay={500}
                TransitionComponent={Zoom}
                title="El bús debería haber llegado (sin confirmación)"
            >
                <QuestionMarkIcon
                    color="primary"
                />
            </Tooltip>
        </div>

    )
}

export const IconoBusEstado = ({ llegada }) => {
    return (
        <div>
            <Tooltip
                describeChild
                leaveDelay={500}
                TransitionComponent={Zoom}
                title={llegada ? "El autobus ha llegado a su destino" : "El autobus está llegando a su destino"}
            >
                <DirectionsBusTwoToneIcon
                    color="primary"
                />
            </Tooltip>
        </div>
    )
}

export const IconoCorrecto = () => {
    return (
        <Tooltip
            describeChild
            leaveDelay={500}
            TransitionComponent={Zoom}
            title="El bús ha llegado en un tiempo cercano a la fecha prevista"
        >
            <CheckIcon
                color="primary"
            />
        </Tooltip>
    )
}

export const IconoIncorrecto = ({ error }) => {
    return (
        <Tooltip
            describeChild
            leaveDelay={500}
            TransitionComponent={Zoom}
            title={error > 0 ? "El bus ha llegado demasiado tarde a la parada" : "El bus ha llegado con demasada antelación a la parada"}
        >
            <ClearIcon
                color="primary"
            />
        </Tooltip >
    )
}

export const IconoError = () => {
    return (
        <ErrorIcon
            color="primary"
        />
    )
}

export const IconosTresPuntos = () => {
    return (
        <div>
            <Tooltip
                describeChild
                leaveDelay={500}
                TransitionComponent={Zoom}
                title="Aún no ha llegado el bus"
            >
                <MoreHorizIcon
                    color="primary"
                />
            </Tooltip>
        </div>
    )
}