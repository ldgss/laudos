const form = document.getElementById('anulacion_form');
const modal = new bootstrap.Modal(document.getElementById('anulacion_modal'));
const detalle = document.getElementById('detalle_modal');
const numero_unico = document.getElementById('numero_unico');
const confirmar = document.getElementById('boton_confirmar_modal');
const pallet = document.getElementById("pallet_modal")

form.addEventListener('submit', function (e) {
    e.preventDefault(); 
    pallet.innerHTML = numero_unico.value

    if (/^\d{4}-T2-\d{6}$/.test(numero_unico.value)) {
        get_detalles();
    }

    modal.show();   
});

function get_detalles(){
    fetch('/anulacion/detalle_t2', {
        method: 'POST',
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({ numero_unico: numero_unico.value })
    })
    .then(function (response) {
        if (!response.ok) {
        throw new Error('Error al obtener el detalle');
        }
        return response.json(); // Cambia a .json() si tu backend devuelve JSON
    })
    .then(function (data) {
        if (!Array.isArray(data) || data.length === 0) {
            console.log(data)
            detalle.innerHTML = `<div class="text-danger">No se encontraron datos para mostrar.</div>`;
            return;
        }

        const numeroUnico = data[0].numero_unico;
        const nuevaDen = data[0].nueva_den;
        const tipoReacondicionado = data[0].tipo_reacondicionado;

        // Encabezado
        let html = `
            <div class="text-danger mb-2">
                <strong>Se eliminará:</strong><br>
                ${numeroUnico}<br>
                ${nuevaDen}<br>
                ${tipoReacondicionado}
            </div>
            <div class="text-danger">
                <strong>Se devolverán las siguientes unidades:</strong><br>
        `;

        // Inputs ocultos iniciales
        html += `
            <input type="hidden" name="nueva_den" value="${nuevaDen}">
            <input type="hidden" name="tipo_reacondicionado" value="${tipoReacondicionado}">
        `;

        data.forEach((item, index) => {
            const destino = item.e_nu_a_dev || item.m_nu_a_dev || item.r_nu_a_dev;
            const origen = item.m_original || item.e_original || '';
            const originInfo = origen ? ` (origen: ${origen})` : '';

            html += `${item.cantidad} a ${destino}${originInfo}<br>`;

            // Inputs ocultos por cada item
            html += `
                <input type="hidden" name="items[${index}][cantidad]" value="${item.cantidad}">
                <input type="hidden" name="items[${index}][destino]" value="${destino}">
                <input type="hidden" name="items[${index}][origen]" value="${item.rd2_id_a_dev}">
            `;
        });

        html += `</div>`;

        // Asignar al innerHTML
        detalle.innerHTML = html;

    })
    .catch(function (error) {
        detalle.innerHTML = `<div class="text-danger">No se pudo cargar el detalle del pallet.</div>`;
    });
}

confirmar.addEventListener('click', function () {
    modal.hide();       
    form.submit();          
});