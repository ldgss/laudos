function formInsumo(){
    if(document.getElementById('form_insumo')){
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
    }
}

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

function insumosTableBody(){
    if(document.getElementById('insumosTableBody')){
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
            lotePrevio(codigo, denominacion);

            const modalEl = document.getElementById('insumosModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
        });
    }
}

function formProveedor(){
    if(document.getElementById('form_proveedor')){
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
    }
}

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

function proveedorTableBody(){
    if(document.getElementById('proveedorTableBody')){
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
    }
}

function insumoStickerForm(){
    if(document.getElementById("insumo_sticker_form")){
        document.getElementById("insumo_sticker_form").addEventListener('submit', function(e) {

            // chequear insumo y proveedor
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
                window.scrollTo({ top: 0, behavior: "smooth" });
            
            }

            // chequear cantidades
            const cantidad_total = parseFloat(document.getElementById("cantidad_total").value);
            let composicion;
            let pallets_1 = document.getElementById("pallets_1");
            let unidades_1 = document.getElementById("unidades_1");
            composicion = pallets_1.value * unidades_1.value;

            // chequear que composicion 2 este completa
            let pallets_2 = document.getElementById("pallets_2");
            let unidades_2 = document.getElementById("unidades_2");

            if(pallets_2 && unidades_2 && pallets_2.value && unidades_2.value){
                composicion += pallets_2.value * unidades_2.value;
            } else if(!!pallets_2?.value !== !!unidades_2?.value){
                e.preventDefault();
                alert("La segunda línea de la composición no está completa");
                pallets_2.focus()
            }

            // chequear que composicion 3 este completa
            let pallets_3 = document.getElementById("pallets_3");
            let unidades_3 = document.getElementById("unidades_3");

            if(pallets_3 && unidades_3 && pallets_3.value && unidades_3.value){
                composicion += pallets_3.value * unidades_3.value;
            } else if(!!pallets_3?.value !== !!unidades_3?.value){
                e.preventDefault();
                alert("La tercera línea de la composición no está completa");
                pallets_3.focus()
            }
            
            if(cantidad_total !== composicion){
                e.preventDefault();
                alert(`El total: ${cantidad_total} no coincide con la composicion: ${composicion}`);
                document.getElementById("cantidad_total").focus();
            }
        });
    }
}

async function lotePrevio(codigo, denominacion){
    const lote = document.getElementById("lote");
    if(lote){

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

}

function printBarcodeSticker() {

    const printButton = document.getElementById('print-barcode-sticker');

    if (!printButton) {
        return;
    }

    printButton.addEventListener('click', function () {

        const stickers = document.querySelectorAll('.descripcion_sticker');

        if (stickers.length === 0) {
            return;
        }

        const newWindow = window.open('', '_blank');

        if (!newWindow) {
            alert('El navegador bloqueó la ventana de impresión.');
            return;
        }

        let contenido = '';

        stickers.forEach((sticker) => {
            contenido += `
                <div class="sticker">
                    ${sticker.outerHTML}
                </div>
            `;
        });

        newWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>Códigos de Barras</title>

                <style>

                    @page {
                        margin: 10mm;
                    }

                    body {
                        margin: 0;
                        padding: 0;
                        font-family: Arial, sans-serif;
                    }

                    .sticker {
                        width: 100%;
                        margin: 0 auto 20px auto;
                        page-break-inside: avoid;
                    }

                    .descripcion_sticker {
                        border-collapse: collapse;
                        width: 50%;
                        margin: 0 auto;
                        border: 2px solid black;
                    }

                    .descripcion_sticker th,
                    .descripcion_sticker td {
                        border: 1px solid black;
                        padding: 18px;
                        text-align: left;
                        font-size:20px;
                    }
                    
                    .descripcion_sticker tbody tr:nth-child(odd) {
                        background-color: #ffffff;
                    }

                    .descripcion_sticker thead {
                        background-color: #4CAF50;
                        color: white;
                    }

                    .deno {
                        width: 50%;
                        margin: 0 auto;
                        text-align: center;
                        font-weight: bold;
                        font-style: italic;
                        border: 2px solid black;
                        border-top: none;
                        box-sizing: border-box;
                        padding: 15px;
                    }

                    .atencion {
                        font-style: normal;
                    }

                    @media print {

                        .sticker {
                            page-break-inside: avoid;
                        }

                    }

                </style>
            </head>

            <body>

                ${contenido}

            </body>
            </html>
        `);

        newWindow.document.close();

        newWindow.onload = function () {
            newWindow.focus();
            newWindow.print();
        };

    });
}

function generarBarCode(){
    // Selecciona todos los inputs con la clase 'barcode_text'
    const inputs = document.querySelectorAll('.barcode_text');

    inputs.forEach((input, index) => {
        const text = input.value;

        // Busca el SVG/canvas correspondiente por posición o por data-attribute
        const barcodeElement = document.querySelectorAll('.barcode')[index];

        JsBarcode(barcodeElement, text, {
            format: "CODE128",
            width: 4,
            height: 200,
            displayValue: true
        });
    });
}

formInsumo();
insumosTableBody();
formProveedor();
proveedorTableBody();
insumoStickerForm();
printBarcodeSticker();
generarBarCode()