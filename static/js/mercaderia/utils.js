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
    const clase = document.getElementById("cod_cls").value;
    const cantidadInput = document.getElementById("cantidad");
    switch (clase) {
        case 'Extrac':
            break;
        case 'Pas500':
            cantidadInput.value = 1080;
            break;
        case 'Pelado':
            cantidadInput.value = 294;
            break;
        case 'Pulpa':
            console.log("Defina si la pulpa es Lata 8 o Botella 500");
            break;
        case 'Pure':
            cantidadInput.value = 1980;
            break;
        case 'Tri500':
            cantidadInput.value = 1080;
            break;
        case 'Tri8':
            cantidadInput.value = 115;
            break; 
        case 'Tri910':
            cantidadInput.value = 840;
            break;
        case 'Tri950':
            cantidadInput.value = 840;
            break;
        case 'Tritur':
            break; 
        default:
            console.log("La cantidad no esta definida")
            break;
    }
}

function actualizarValoresOcultos() {
    const input = document.getElementById("denominacion");
    const options = document.getElementById("denominacion_opciones").options;

    for (let option of options) {
        if (option.value === input.value) {
            document.getElementById("cod_cls").value = option.getAttribute("data-cod-cls");
            document.getElementById("cod_mae").value = option.getAttribute("data-cod-mae");
            break; 
        }
    }
}

function lote_a_automatico(){
    const lote_a = document.getElementById("lote_a");
    const fechaActual = new Date()
    const year = fechaActual.getFullYear();
    const hoy = year.toString()[3]
    lote_a.value = hoy;
}

function julianoAutomatico(){
    const lote_c = document.getElementById("lote_c");
    const fechaActual = new Date()
    const year = fechaActual.getFullYear();
    const fechaInicial = new Date(year, 0, 1);
    const hoy = Math.floor((fechaActual - fechaInicial) / (1000 * 60 * 60 * 24)) + 1;
    lote_c.value = hoy;
}

function imprimir(){
    const text = document.getElementById('barcode_text').value;
    JsBarcode("#barcode", text, {
        format: "CODE128",
        width: 4, 
        height: 200,
        displayValue: true
    });
}

function imprimir_new_tab(){
        document.getElementById('print-barcode').addEventListener('click', function() {
            
            const barcodeSvg = document.getElementById('barcode').outerHTML;
            const descripcion = document.getElementById('descripcion').outerHTML;
            
            
            const newWindow = window.open('', '_blank');
            newWindow.document.write(`
                <html>
                <head>
                

                <title>Código de Barras</title>
                </head>
                <body>
                
                <div style="text-align:center;">
                ${barcodeSvg}
                </div>

                <div class="table-container">
                    ${descripcion}
                </div>

                <style>
                    
                    .table-container {
                        justify-content: center; 
                        align-items: center;    
                        
                    }

                   
                    #descripcion {
                        border-collapse: collapse; 
                        width: 50%; 
                        margin: 0 auto; 
                        border: 2px solid black;
                    }

                    
                    #descripcion th, #descripcion td {
                        border: 1px solid black;
                        padding: 8px; 
                        text-align: left;
                    }

                    
                    #descripcion tbody tr:nth-child(odd) {
                        background-color: #f2f2f2; 
                    }

                    
                    #descripcion thead {
                        background-color: #4CAF50;
                        color: white;
                    }
                </style>


                
                
                <script>
                //     window.onload = function() {
                //         window.print();
                //     }
                // <\/script>
                    </body>
            </html>
        `);

        newWindow.document.close();
    });
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

function calcular_vencimiento(fecha_elaboracion, meses) {
    const [year, month, day] = fecha_elaboracion.split(' ')[0].split('-').map(Number);
    const [hours, minutes] = fecha_elaboracion.split(' ')[1].split(':').map(Number);
    const date = new Date(year, month - 1, day, hours, minutes);
    date.setMonth(date.getMonth() + meses);
    
    const nuevoYear = date.getFullYear();
    const nuevoMes = String(date.getMonth() + 1).padStart(2, '0');
    const nuevoDia = String(date.getDate()).padStart(2, '0');
    const nuevoHoras = String(date.getHours()).padStart(2, '0');
    const nuevoMinutos = String(date.getMinutes()).padStart(2, '0');
    
    return `${nuevoYear}-${nuevoMes}-${nuevoDia} ${nuevoHoras}:${nuevoMinutos}`;
}

function actualizar_vencimiento_en_listado(){
    document.querySelectorAll('#listado_con_vto tbody tr').forEach(row => {
        const fecha_elaboracion = row.querySelector('.fecha_elaboracion').innerText;
        const meses = parseInt(row.querySelector('.meses').innerText);
        const vencimiento = calcular_vencimiento(fecha_elaboracion, meses);
        
        row.querySelector('.vencimiento').innerText = vencimiento;
    });
}

// function actualizar_vencimiento_unico(){
//     const fecha_elaboracion = document.querySelector('.fecha_elaboracion').innerText;
//     const meses = parseInt(document.querySelector('.meses').innerText);
//     const vencimiento = calcular_vencimiento(fecha_elaboracion, meses);
        
//     document.querySelector('.vencimiento').innerText = vencimiento;
    
// }

function actualizar_vencimiento_unico(){
    const elementosFechaElaboracion = document.querySelectorAll('.fecha_elaboracion');
    const elementosMeses = document.querySelectorAll('.meses');
    const elementosVencimiento = document.querySelectorAll('.vencimiento');
    
    // Asegurarse de que haya el mismo número de elementos de fecha, meses y vencimiento
    const cantidadElementos = elementosFechaElaboracion.length;

    for (let i = 0; i < cantidadElementos; i++) {
        const fecha_elaboracion = elementosFechaElaboracion[i].innerText;
        const meses = parseInt(elementosMeses[i].innerText);
        const vencimiento = calcular_vencimiento(fecha_elaboracion, meses);
        
        // Actualizar el vencimiento en cada elemento correspondiente
        elementosVencimiento[i].innerText = vencimiento;
    }
}


try {
    window.addEventListener('load', actualizarFechaYHora);
    window.addEventListener('load', julianoAutomatico);
    window.addEventListener('load', lote_a_automatico);
    window.addEventListener('load', imprimir);
    window.addEventListener('load', imprimir_new_tab);
    window.addEventListener('load', actualizar_vencimiento_en_listado);
    window.addEventListener('load', actualizar_vencimiento_unico);
} catch (error) {
    // console.log(error)
}