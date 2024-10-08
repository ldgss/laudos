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
    const denominacionInput = document.getElementById("denominacion");
    const cantidadInput = document.getElementById("cantidad");
    
    
    console.log("...")
    switch (denominacionInput.value) {
        case 'Extrac':
        case 'Pas500':
        case 'Pelado':
        case 'Pulpa':
        case 'Pure':
        case 'Tri500':
        case 'Tri8':
            cantidadInput.value = 115;
            break; 
        case 'Tri910':
        case 'Tri950':
        case 'Tritur':
            cantidadInput.value = 0; 
            break; 
        default:
            cantidadInput.value = ''; 
            break;
    }
}


window.onload = actualizarFechaYHora;