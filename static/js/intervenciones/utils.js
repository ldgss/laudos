function validarLineaAfectada() {
    const linea_afectada = document.querySelectorAll('[id^="linea_afectada"]');

    linea_afectada.forEach(input => {
        // obtengo el id del datalist asociado
        const listId = input.getAttribute('list');
        const datalist = document.getElementById(listId);

        if (datalist) {
            // obtengo todas las opciones del datalist
            const opciones = Array.from(datalist.options).map(opt => opt.value.trim());
            const valor = input.value.trim();

            // si el valor no está en las opciones, se borra
            if (!opciones.includes(valor)) {
                input.value = '';
            }
        }
    });
}

function validarTipoDeFallo() {
    const linea_afectada = document.querySelectorAll('[id^="tipo_de_fallo"]');

    linea_afectada.forEach(input => {
        // obtengo el id del datalist asociado
        const listId = input.getAttribute('list');
        const datalist = document.getElementById(listId);

        if (datalist) {
            // obtengo todas las opciones del datalist
            const opciones = Array.from(datalist.options).map(opt => opt.value.trim());
            const valor = input.value.trim();

            // si el valor no está en las opciones, se borra
            if (!opciones.includes(valor)) {
                input.value = '';
            }
        }
    });
}

function actualizarValoresLineaAfectada() {
    const linea_afectada = document.getElementById('linea_afectada');
    const listId = linea_afectada.getAttribute('list');
    const datalist = document.getElementById(listId);
    if (!datalist) return;
    // Busca la opción que coincide con el valor del input
    const option = Array.from(datalist.options).find(opt => opt.value.trim() === linea_afectada.value.trim());
    const lineas_mantenimiento_id = document.getElementById('lineas_mantenimiento_id')
    if(option){
        lineas_mantenimiento_id.value = option.getAttribute('data-lineas-mantenimiento-id')
    }else{
        lineas_mantenimiento_id.value = ''
    }
}

function actualizarValoresTipoDeFallo() {
    const tipo_de_fallo = document.getElementById('tipo_de_fallo');
    const listId2 = tipo_de_fallo.getAttribute('list');
    const datalist2 = document.getElementById(listId2);
    if (!datalist2) return;
    // Busca la opción que coincide con el valor del input
    const option2 = Array.from(datalist2.options).find(opt => opt.value.trim() === tipo_de_fallo.value.trim());
    const tipo_de_fallo_id = document.getElementById('tipo_de_fallo_id')
    if(option2){
        tipo_de_fallo_id.value = option2.getAttribute('data-tipo-de-fallo-id')
    }else{
        tipo_de_fallo_id.value = ''
    }
}

document.getElementById('imagenes').addEventListener('change', function() {
    if (this.files.length > 2) {
        alert("Solo puedes subir hasta 2 imágenes.");
        this.value = ""; // limpia la selección
    }
});