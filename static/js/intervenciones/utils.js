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

if(document.getElementById('imagenes_galeria')){
    document.getElementById('imagenes_galeria').addEventListener('change', function() {
        if (this.files.length > 5) {
            alert("Solo puedes subir hasta 5 imágenes.");
            this.value = ""; // limpia la selección
        }
    });
}

function formatDuracionEs(intervalo) {
    let totalSegundos;

    if (typeof intervalo === "string") {
        const match = intervalo.match(/(\d+)\s+days?,\s*(\d+):(\d+):(\d+)/);
        if (!match) return intervalo;

        const [, d, h, m, s] = match.map(Number);
        totalSegundos = (((d * 24 + h) * 60) + m) * 60 + s;
    } else {
        totalSegundos = intervalo;
    }

    const dias = Math.floor(totalSegundos / 86400);
    const horas = Math.floor((totalSegundos % 86400) / 3600);
    const minutos = Math.floor((totalSegundos % 3600) / 60);
    const segundos = totalSegundos % 60;

    const partes = [];
    if (dias > 0) partes.push(`${dias} día${dias === 1 ? "" : "s"}`);
    if (horas > 0) partes.push(`${horas} hora${horas === 1 ? "" : "s"}`);
    if (minutos > 0) partes.push(`${minutos} minuto${minutos === 1 ? "" : "s"}`);
    if (segundos > 0 && dias === 0)
        partes.push(`${segundos} segundo${segundos === 1 ? "" : "s"}`);

    return partes.join(" ");
}

document.addEventListener("DOMContentLoaded", () => {
    const celdas = document.querySelectorAll(".duracion");
    celdas.forEach(td => {
        td.textContent = formatDuracionEs(td.textContent.trim());
    });
});

document.querySelectorAll('.btn-anular').forEach(button => {
    button.addEventListener('click', function () {
        const intervencion_id = this.getAttribute('data-id');
        document.getElementById('intervencion_id').value = intervencion_id;
    });
});