document.getElementById('form_insumo').addEventListener('submit', async function (e) {
    e.preventDefault();

    const input = document.getElementById('insumo_buscar');
    const valor = input.value.trim();

    if (!valor) {
        return;
    }

    try {
        const response = await fetch('/insumos/buscar_insumo_para_sticker', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ insumo_buscar: valor })
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();
        popularModalInsumos(data);

    } catch (error) {
        console.error('Error al buscar insumo:', error);
    }
});

function popularModalInsumos(insumos) {
    const tbody = document.getElementById('insumosTableBody');
    // Limpiar resultados previos
    tbody.innerHTML = '';

    if (!insumos || insumos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted">
                    No se encontraron insumos
                </td>
            </tr>
        `;
    } else {
        insumos.forEach(insumo => {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${insumo.arb_insumo_codigo}</td>
                <td>${insumo.arb_insumo_denominacion}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-primary btn-seleccionar-insumo"
                        data-codigo="${insumo.arb_insumo_codigo}"
                        data-denominacion="${insumo.arb_insumo_denominacion}">
                        Seleccionar
                    </button>
                </td>
            `;

            tbody.appendChild(tr);
        });
    }

    // Mostrar el modal (requiere bootstrap.bundle.js cargado)
    const modal = new bootstrap.Modal(document.getElementById('insumosModal'));
    modal.show();
}

document.getElementById('insumosTableBody').addEventListener('click', function (e) {
    const btn = e.target.closest('.btn-seleccionar-insumo');
    if (!btn) return;

    const codigo = btn.dataset.codigo;
    const denominacion = btn.dataset.denominacion;

    console.log('Insumo seleccionado:', codigo, denominacion);

    const arb_insumo_codigo = document.getElementById('arb_insumo_codigo');
    const arb_insumo_denominacion = document.getElementById('arb_insumo_denominacion');
    arb_insumo_codigo.value = codigo;
    arb_insumo_denominacion.value = denominacion;
    lote_previo(codigo, denominacion);

    const modalEl = document.getElementById('insumosModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();
});

document.getElementById('form_proveedor').addEventListener('submit', async function (e) {
    e.preventDefault();

    const input = document.getElementById('proveedor_buscar');
    const valor = input.value.trim();

    if (!valor) {
        return;
    }

    try {
        const response = await fetch('/insumos/buscar_proveedor_para_sticker', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ proveedor_buscar: valor })
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log(data)
        popularModalProveedor(data);

    } catch (error) {
        console.error('Error al buscar proveedor:', error);
    }
});

function popularModalProveedor(proveedores) {
    const tbody = document.getElementById('proveedorTableBody');
    // Limpiar resultados previos
    tbody.innerHTML = '';

    if (!proveedores || proveedores.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted">
                    No se encontraron proveedores con ese nombre.
                </td>
            </tr>
        `;
    } else {
        proveedores.forEach(proveedor => {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${proveedor.arb_proveedor_codigo}</td>
                <td>${proveedor.arb_proveedor_denominacion}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-primary btn-seleccionar-proveedor"
                        data-codigo="${proveedor.arb_proveedor_codigo}"
                        data-clase="${proveedor.arb_proveedor_clase}"
                        data-denominacion="${proveedor.arb_proveedor_denominacion}">
                        Seleccionar
                    </button>
                </td>
            `;

            tbody.appendChild(tr);
        });
    }

    // Mostrar el modal (requiere bootstrap.bundle.js cargado)
    const modal = new bootstrap.Modal(document.getElementById('proveedorModal'));
    modal.show();
}

document.getElementById('proveedorTableBody').addEventListener('click', function (e) {
    const btn = e.target.closest('.btn-seleccionar-proveedor');
    if (!btn) return;

    const codigo = btn.dataset.codigo;
    const clase = btn.dataset.clase;
    const denominacion = btn.dataset.denominacion;

    console.log('Proveedor seleccionado:', codigo, denominacion, clase);

    const arb_proveedor_codigo = document.getElementById('arb_proveedor_codigo');
    const arb_proveedor_clase = document.getElementById('arb_proveedor_clase');
    const arb_proveedor_denominacion = document.getElementById('arb_proveedor_denominacion');
    arb_proveedor_codigo.value = codigo;
    arb_proveedor_clase.value = clase;
    arb_proveedor_denominacion.value = denominacion;

    const modalEl = document.getElementById('proveedorModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();
});

const insumo_sticker_form = document.getElementById("insumo_sticker_form")

insumo_sticker_form.addEventListener('submit', function(e) {

  const arb_insumo_codigo = document.getElementById('arb_insumo_codigo');
  const arb_insumo_denominacion = document.getElementById('arb_insumo_denominacion');
  const arb_proveedor_codigo = document.getElementById('arb_proveedor_codigo');
  const arb_proveedor_clase = document.getElementById('arb_proveedor_clase');
  const arb_proveedor_denominacion = document.getElementById('arb_insumo_denominacion');
  
  if (  !arb_insumo_codigo.value.trim() || 
        !arb_insumo_denominacion.value.trim() || 
        !arb_proveedor_codigo.value.trim() ||
        !arb_proveedor_clase.value.trim() ||
        !arb_proveedor_denominacion.value.trim()) {
    e.preventDefault();
    alert("Busque y seleccione el articulo y el proveedor por favor.");
  }

});

async function lote_previo(codigo, denominacion){
    const lote = document.getElementById("lote");
    
    try {
        const response = await fetch('/insumos/lote_previo_sticker', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                codigo: codigo,
                denominacion: denominacion 
            })
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log(data)
        if(!data){
            lote.value = ""
            lote.placeholder = "Sin lote previo. Consultar a calidad."
        }else{
            lote.value = ""
            lote.placeholder = `Lote previo: ${data}`
        }
        

    } catch (error) {
        console.error('Error al buscar lote previo:', error);
    }

}