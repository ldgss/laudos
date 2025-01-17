
function a(){
    document.getElementById('productor_razon_social').addEventListener('input', function () {
        const input = this.value;
        const datalist = document.getElementById('productor_razon_social_lista');
        const options = datalist.options;

        let found = false;

        for (let i = 0; i < options.length; i++) {
            if (options[i].value === input) {
                // Actualizar el valor de productor_codigo
                document.getElementById('productor_codigo').value = options[i].dataset.codMae;
                found = true;
                break;
            }
        }

        // Si no se encuentra, limpiar el valor de productor_codigo
        if (!found) {
            document.getElementById('productor_codigo').value = '';
        }
    });
}

function b(){
    document.getElementById('fletero_nombre').addEventListener('input', function () {
        const input = this.value;
        const datalist = document.getElementById('fletero_nombre_lista');
        const options = datalist.options;

        let found = false;

        for (let i = 0; i < options.length; i++) {
            if (options[i].value === input) {
                // Actualizar el valor de fletero_codigo
                document.getElementById('fletero_codigo').value = options[i].dataset.codMae;
                found = true;
                break;
            }
        }

        // Si no se encuentra, limpiar el valor de fletero_codigo
        if (!found) {
            document.getElementById('fletero_codigo').value = '';
        }
    });
}

function c(){
    document.getElementById('variedad_nombre').addEventListener('input', function () {
        const input = this.value;
        const datalist = document.getElementById('variedad_nombre_lista');
        const options = datalist.options;

        let found = false;

        for (let i = 0; i < options.length; i++) {
            if (options[i].value === input) {
                // Actualizar el valor de variedad_codigo
                document.getElementById('variedad_codigo').value = options[i].dataset.codMae;
                found = true;
                break;
            }
        }

        // Si no se encuentra, limpiar el valor de variedad_codigo
        if (!found) {
            document.getElementById('variedad_codigo').value = '';
        }
    });
}

function d(){
    document.getElementById('variedad_nombre_acoplado').addEventListener('input', function () {
        const input = this.value;
        const datalist = document.getElementById('variedad_nombre_acoplado_lista');
        const options = datalist.options;

        let found = false;

        for (let i = 0; i < options.length; i++) {
            if (options[i].value === input) {
                // Actualizar el valor de variedad_codigo
                document.getElementById('variedad_codigo_acoplado').value = options[i].dataset.codMae;
                found = true;
                break;
            }
        }

        // Si no se encuentra, limpiar el valor de variedad_codigo
        if (!found) {
            document.getElementById('variedad_codigo_acoplado').value = '';
        }
    });
}

function validar_productor_razon_social() {
    const denominacionInputs = document.querySelectorAll('[id^="productor_razon_social"]');
    const denominacionOpciones = document.getElementById('productor_razon_social_lista');
    if (!denominacionOpciones) return;
    const opciones = Array.from(denominacionOpciones.options).map(option => option.value);
    denominacionInputs.forEach(input => {
        if (!opciones.includes(input.value)) {
            input.value = '';
        }
    });
}

function validar_productor_zona() {
    const denominacionInputs = document.querySelectorAll('[id^="productor_zona"]');
    const denominacionOpciones = document.getElementById('productor_zona_lista');
    if (!denominacionOpciones) return;
    const opciones = Array.from(denominacionOpciones.options).map(option => option.value);
    denominacionInputs.forEach(input => {
        if (!opciones.includes(input.value)) {
            input.value = '';
        }
    });
}

function validar_productor_tipo_cosecha() {
    const denominacionInputs = document.querySelectorAll('[id^="productor_tipo_cosecha"]');
    const denominacionOpciones = document.getElementById('producto_tipo_cosecha_lista');
    if (!denominacionOpciones) return;
    const opciones = Array.from(denominacionOpciones.options).map(option => option.value);
    denominacionInputs.forEach(input => {
        if (!opciones.includes(input.value)) {
            input.value = '';
        }
    });
}

function validar_fletero_nombre() {
    const denominacionInputs = document.querySelectorAll('[id^="fletero_nombre"]');
    const denominacionOpciones = document.getElementById('fletero_nombre_lista');
    if (!denominacionOpciones) return;
    const opciones = Array.from(denominacionOpciones.options).map(option => option.value);
    denominacionInputs.forEach(input => {
        if (!opciones.includes(input.value)) {
            input.value = '';
        }
    });
}

function validar_variedad_nombre() {
    const denominacionInputs = document.querySelectorAll('[id^="variedad_nombre"]');
    const denominacionOpciones = document.getElementById('variedad_nombre_lista');
    if (!denominacionOpciones) return;
    const opciones = Array.from(denominacionOpciones.options).map(option => option.value);
    denominacionInputs.forEach(input => {
        if (!opciones.includes(input.value)) {
            input.value = '';
        }
    });
}

function validar_variedad_nombre_acoplado() {
    const denominacionInputs = document.querySelectorAll('[id^="variedad_nombre_acoplado"]');
    const denominacionOpciones = document.getElementById('variedad_nombre_acoplado_lista');
    if (!denominacionOpciones) return;
    const opciones = Array.from(denominacionOpciones.options).map(option => option.value);
    denominacionInputs.forEach(input => {
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

function ipm(){
    console.log("instalando")
    document.getElementById('print-ipm').addEventListener('click', function() {
    console.log("ejecutando")
        
        let contenido;
        let id_para_estilo;

        if (document.getElementById('descripcion')){
            contenido = document.getElementById('descripcion').outerHTML;
            id_para_estilo = "descripcion"
        }else{
            contenido = document.getElementById('descripcion_reacondicionado').outerHTML;
            id_para_estilo = "descripcion_reacondicionado"
        }

        const newWindow = window.open('', '_blank');
        newWindow.document.write(`
            <html>
            <head>
            

            <title>Código de Barras</title>
            </head>
            <body>
            
            <div style="text-align:center;">
            IPM PORTERIA
            </div>

            <div class="table-container">
                ${contenido}
            </div>

            <style>
                
                .table-container {
                    justify-content: center; 
                    align-items: center;    
                }

                
                #${id_para_estilo} {
                    border-collapse: collapse; 
                    width: 50%; 
                    margin: 0 auto; 
                    border: 2px solid black;
                }

                
                #${id_para_estilo} th, #${id_para_estilo} td {
                    border: 1px solid black;
                    padding: 8px; 
                    text-align: left;
                }

                
                #${id_para_estilo} tbody tr:nth-child(odd) {
                    background-color: #ffffff; 
                }

                
                #${id_para_estilo} thead {
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


try {
    window.addEventListener('load', updateDateTimeField);
    window.addEventListener('load', a);
    window.addEventListener('load', b);
    window.addEventListener('load', c);
    window.addEventListener('load', d);
    window.addEventListener('load', ipm);
    const formulario = document.getElementById("materia");
    formulario.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
        }
    });
    setInterval(updateDateTimeField, 1000);
} catch (error) {
    console.log(error)
}


