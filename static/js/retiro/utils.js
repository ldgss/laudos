function actualizarCuit() {
    const transporteInput = document.getElementById('transporte');
    const cuitInput = document.getElementById('cuit');
    const opciones = document.getElementById('transporte_opciones').options;
    
    // Buscar el valor seleccionado en el datalist
    for (let i = 0; i < opciones.length; i++) {
        if (opciones[i].value === transporteInput.value) {
            cuitInput.value = opciones[i].getAttribute('data-cuit');
            return;
        }
    }
    
    // Si no encuentra coincidencia, limpia el campo CUIT
    cuitInput.value = '';
}

function validarTransporte() {
    const TransporteInputs = document.querySelectorAll('[id^="transporte"]');
    const TransporteOpciones = document.getElementById('transporte_opciones');
    
    // Validar que el elemento de opciones exista
    if (!TransporteOpciones) return;

    // Obtener las opciones como un array
    const opciones = Array.from(TransporteOpciones.options).map(option => option.value);

    TransporteInputs.forEach(input => {
        if (!opciones.includes(input.value)) {
            input.value = '';
        }
    });
}

function updateDateTimeField() {
    const field = document.getElementById('fecha');
    const now = new Date();

    // Ajusta la fecha y hora al huso horario UTC-3
    now.setHours(now.getUTCHours() - 6);

    // Formatea la fecha y hora ajustada en formato YYYY-MM-DDTHH:mm
    const formattedDateTime = now.toISOString().slice(0, 16);

    // Actualiza el campo
    if (field) {
        field.value = formattedDateTime;
    } else {
        console.warn("El campo con ID 'fecha' no fue encontrado.");
    }
}

function boton_volver() {
    const currentUrl = window.location.pathname;
    const urlSegments = currentUrl.split('/').filter(segment => segment);

    if (urlSegments.length > 1) {
        // volver al menu principal
        window.location.href = '/' + urlSegments[0];
    } else {
        // si no hay pagina previa, volver al index
        window.location.href = "/";
    }
}

// setear el reloj la primera vez y el interval luego
updateDateTimeField()
setInterval(updateDateTimeField, 1000);
