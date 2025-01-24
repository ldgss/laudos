if ( document.getElementById('buscar_insumo') ){
    document.getElementById('buscar_insumo').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevenir el envío del formulario estándar
    
        // Obtener los valores de los inputs
        const codigoInsumo = document.getElementById('cta_alm_buscar').value;
        const loteInsumo = document.getElementById('cod_lot_buscar').value;
    
        // Validar los campos
        if (!codigoInsumo || !loteInsumo) {
            alert('Por favor, complete todos los campos.');
            return;
        }
    
        // Enviar la solicitud al servidor
        fetch('/insumos/buscar_insumo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cta_alm: codigoInsumo, cod_lot: loteInsumo })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor.');
            }
            return response.json(); // Asumimos que el servidor responde con JSON
        })
        .then(data => {
            // Verificar que los datos sean válidos
            if (!data || data.length === 0) {
                alert('No se encontraron resultados.');
                return;
            }
    
            // Limpiar la tabla del modal
            const tableBody = document.getElementById('resultTableBody');
            tableBody.innerHTML = '';
    
            // Llenar la tabla con los datos recibidos
            data.forEach((item, index) => {
                const row = document.createElement('tr');
                // queda afuera item.can
                row.innerHTML = `
                    <td>${item.cta_alm}</td>
                    <td>${item.cod_lot}</td>
                    <td>${item.den_fac}</td>
                    
                    <td>
                        <button class="btn btn-primary btn-sm" onclick="selectInsumo(${index})">Seleccionar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
    
            // Guardar los datos temporalmente para selección
            window.modalData = data;
    
            // Mostrar el modal
            const modal = new bootstrap.Modal(document.getElementById('resultModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al realizar la búsqueda.');
        });
    });
}

// Función para manejar la selección de un insumo
function selectInsumo(index) {
    const selectedItem = window.modalData[index];

    // Rellenar los inputs del formulario
    document.getElementById('cta_alm').value = selectedItem.cta_alm;
    document.getElementById('cod_lot').value = selectedItem.cod_lot;
    document.getElementById('den_fac').value = selectedItem.den_fac;
    // document.getElementById('can').value = selectedItem.can;

    // Cerrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('resultModal'));
    modal.hide();
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-anular').forEach(button => {
        button.addEventListener('click', function () {
            const insumo_envase_id = this.getAttribute('data-id');
            document.getElementById('insumo_envase_id').value = insumo_envase_id;
        });
    });
});