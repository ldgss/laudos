function validarMarca() {
    const denominacionInput = document.getElementById('denominacion');
    const denominacion_opciones = document.getElementById('denominacion_opciones');
    const opciones = Array.from(denominacion_opciones.options).map(option => option.value);

    if (!opciones.includes(denominacionInput.value)) {
        denominacionInput.value = '';
    }
}

function actualizarFechaYHora() {
    const inputFecha = document.getElementById('fecha');
    const inputHora = document.getElementById('hora');
    const fechayhora = new Date();

    const año = fechayhora.getFullYear();
    const mes = String(fechayhora.getMonth() + 1).padStart(2, '0');
    const dia = String(fechayhora.getDate()).padStart(2, '0');
    const horas = String(fechayhora.getHours()).padStart(2, '0');
    const minutos = String(fechayhora.getMinutes()).padStart(2, '0');
    
    inputFecha.value = `${año}-${mes}-${dia}`;
    inputHora.value = `${horas}:${minutos}`;
}

function rellenarCantidad() {
    const clase = document.getElementById("cod_cls").value;
    const cantidadInput = document.getElementById("cantidad");
    console.log("mae" + document.getElementById("cod_mae").value)
    console.log("clase" + document.getElementById("cod_cls").value)
    console.log("den" + document.getElementById("denominacion").value)
    switch (clase) {
        case 'Extrac':
            break;
        case 'Pas500':
            break;
        case 'Pelado':
            cantidadInput.value = 294;
            break;
        case 'Pulpa':
            break;
        case 'Pure':
            cantidadInput.value = 1980;
            break;
        case 'Tri500':
            break;
        case 'Tri8':
            cantidadInput.value = 115;
            break; 
        case 'Tri910':
            cantidadInput.value = 840;
            break;
        case 'Tri950':
            break;
        case 'Tritur':
            break; 
        default:
            cantidadInput.value = "";
            break;
    }
}

function actualizarValoresOcultos() {
    const input = document.getElementById("denominacion");
    const options = document.getElementById("denominacion_opciones").options;

    for (let option of options) {
        if (option.value === input.value) {
            document.getElementById("cod_cls").value = option.getAttribute("data-cod-cls");
            document.getElementById("cod_mae").value = option.getAttribute("data-cod-mae");
            break; 
        }
    }
}

function julianoAutomatico(){
    const lote = document.getElementById("lote");
    const fechaActual = new Date()
    const year = fechaActual.getFullYear();
    const fechaInicial = new Date(year, 0, 1);
    const hoy = Math.floor((fechaActual - fechaInicial) / (1000 * 60 * 60 * 24)) + 1;

    lote.placeholder += "X-XXX-" + hoy + ". El dia juliano de hoy es " + hoy;
}

window.addEventListener('load', actualizarFechaYHora);
window.addEventListener('load', julianoAutomatico);