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