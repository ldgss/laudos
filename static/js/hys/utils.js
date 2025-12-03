
function validarGravedad() {
    const gravedad = document.getElementById('gravedad');
    const gravedad_opciones = document.getElementById('gravedad_opciones');
    const opciones = Array.from(gravedad_opciones.options).map(option => option.value);

    if (!opciones.includes(gravedad.value)) {
        gravedad.value = '';
    }
}

function validarTipoDeAtencion() {
    const tipo_de_atencion = document.getElementById('tipo_de_atencion');
    const tipo_de_atencion_opciones = document.getElementById('tipo_de_atencion_opciones');
    const opciones = Array.from(tipo_de_atencion_opciones.options).map(option => option.value);

    if (!opciones.includes(tipo_de_atencion.value)) {
        tipo_de_atencion.value = '';
    }
}

function validarAgenteOrigen() {
    const agente_origen = document.getElementById('agente_origen');
    const agente_origen_opciones = document.getElementById('agente_origen_opciones');
    const opciones = Array.from(agente_origen_opciones.options).map(option => option.value);

    if (!opciones.includes(agente_origen.value)) {
        agente_origen.value = '';
    }
}

document.querySelectorAll('.btn-anular').forEach(button => {
    button.addEventListener('click', function () {
        const id_hys = this.getAttribute('data-id');
        document.getElementById('id_hys').value = id_hys;
    });
});

