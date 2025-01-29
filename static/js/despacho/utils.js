document.querySelectorAll('.btn-anular').forEach(button => {
    button.addEventListener('click', function () {
        const despacho_id = this.getAttribute('data-id');
        document.getElementById('despacho_id').value = despacho_id;
    });
});

function actualizarFleteroCodigo(){
    const fletero_codigo = document.querySelectorAll('[id^="fletero_codigo"]');
    const fletero_nombre = document.querySelectorAll('[id^="fletero_nombre"]');
    const fletero_nombre_lista = document.getElementById("fletero_nombre_lista");
    if (!fletero_nombre_lista) return;
    const options = fletero_nombre_lista.options;


    fletero_nombre.forEach(input => {
        for (let option of options) {
            if (option.value === input.value) {
                fletero_codigo.forEach(maeInput => {
                    maeInput.value = option.getAttribute("data-cod-mae");
                });
                break;
            }
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

const beepSound = new Audio("/static/sounds/scan_success.mp3");

document.addEventListener("DOMContentLoaded", function () {
    // Inicializar QuaggaJS en el div con id "interactive"
    Quagga.init({
        inputStream: {
            type: "LiveStream",
            constraints: {
                facingMode: "environment" // Usa la cámara trasera si está disponible
            },
            target: document.querySelector("#interactive")
        },
        decoder: {
            readers: ["code_128_reader"] // Soporta códigos de barras tipo Code 128
        }
    }, function (err) {
        if (err) {
            console.error("Error al iniciar Quagga: ", err);
            return;
        }
        Quagga.start();
    });

    // Manejar la detección exitosa de código de barras respetando el patrón
    const pattern = /^\d{4}-(T1|T2|H1|E1|I1)-\d{6}$/;
    let contador = 0; // Contador para generar IDs únicos

    function existeEscaneo(codigo) {
        return Array.from(document.querySelectorAll("#lista_numero_unico input"))
            .some(input => input.value === codigo);
    }

    Quagga.onDetected(function (result) {
        let codigoBarras = result.codeResult.code;
        if (pattern.test(codigoBarras) && !existeEscaneo(codigoBarras)) {
            document.getElementById("escaneo").value = codigoBarras;
            beepSound.play()
        }
    });

    function agregarEscaneo(numeroUnicoValor) {
        contador++;
        let inputId = `numero_unico_${contador}`;
        let rowId = `row_${contador}`;
        
        let divRow = document.createElement("div");
        divRow.className = "row m-4 justify-content-center";
        divRow.id = rowId;

        let divCol = document.createElement("div");
        divCol.className = "col-sm-5";

        let input = document.createElement("input");
        input.type = "text";
        input.className = "form-control";
        input.name = inputId;
        input.id = inputId;
        input.value = numeroUnicoValor;
        input.readOnly = true;

        let divBtnCol = document.createElement("div");
        divBtnCol.className = "col-sm-2";

        let btnEliminar = document.createElement("button");
        btnEliminar.className = "btn btn-danger";
        btnEliminar.innerText = "Eliminar";
        btnEliminar.onclick = function () {
            let elemento = document.getElementById(rowId);
            if (elemento) {
                elemento.remove();
            }
        };

        divCol.appendChild(input);
        divBtnCol.appendChild(btnEliminar);
        divRow.appendChild(divCol);
        divRow.appendChild(divBtnCol);

        document.getElementById("lista_numero_unico").appendChild(divRow);
    }

    document.getElementById("agregar").addEventListener("click", function () {
        let numeroUnicoValor = document.getElementById("escaneo").value;
        if (!pattern.test(numeroUnicoValor)) {
            alert("El Número Único no cumple con el formato requerido: (Ej: 2024-T1-000001)");
            return;
        }
        if (existeEscaneo(numeroUnicoValor)) {
            alert("El escaneo ya ha sido agregado.");
            return;
        }
        document.getElementById("escaneo").value = ""
        agregarEscaneo(numeroUnicoValor);
    });

     // Evitar envío del formulario con Enter y verificar que haya al menos un escaneo
     const formulario = document.getElementById("formulario");
     formulario.addEventListener("keydown", function (event) {
         if (event.key === "Enter") {
             event.preventDefault();
         }
     });
 
     formulario.addEventListener("submit", function (event) {
         let inputs = document.querySelectorAll("#lista_numero_unico input");
         if (inputs.length === 0) {
             alert("Debe agregar al menos un escaneo antes de enviar el formulario.");
             event.preventDefault();
         }
     });
});


