// Audio para el sonido de éxito
const beepSound = new Audio("/static/sounds/scan_success.mp3"); // Cambia el URL si tienes otro sonido
// Obtener el patrón del input
const inputElement = document.getElementById('numero_unico');
const inputPattern = inputElement.getAttribute('pattern');
const barcodeRegex = new RegExp(inputPattern); 


document.addEventListener('DOMContentLoaded', function () {

const modal = new bootstrap.Modal(document.getElementById('interactionModal'));
modal.show();

Quagga.init({
    inputStream: {
        name: "Live",
        type: "LiveStream",
        target: document.querySelector('#interactive'), // Selección del elemento para la transmisión
        constraints: {
            facingMode: "environment" // Usa la cámara trasera
        }
    },
    decoder: {
        readers: [
            "code_128_reader",        // Code 128
            "ean_reader",             // EAN-13 y EAN-8
            "ean_8_reader",           // EAN-8 (específico)
            "upc_reader",             // UPC-A y UPC-E
            "upc_e_reader",           // UPC-E (específico)
            "code_39_reader",         // Code 39
            "code_93_reader",         // Code 93
            "codabar_reader"
        ]
    }
}, function (err) {
    if (err) {
        console.log(err);
        return;
    }
    console.log("QuaggaJS inicializado correctamente");
    Quagga.start();
});


// Detecta el código de barras
// Quagga.onDetected(function (data) {
//     document.getElementById('numero_unico').value = data.codeResult.code;
//     console.log(data.codeResult.code);
// });

Quagga.onDetected(function (data) {
    const detectedCode = data.codeResult.code;

    // Verifica si el código coincide con el patrón del input
    if (barcodeRegex.test(detectedCode)) {
        // Asigna el valor al input
        inputElement.value = detectedCode;
        console.log("Código válido detectado:", detectedCode);

        // Detener el escaneo
        Quagga.stop();

        // Reproducir sonido
        beepSound.play();
    } else {
        console.log("Código no válido:", detectedCode);
    }
});

});

function validarUbicacion(){
    const denominacionInput = document.getElementById('ubicacion');
    const denominacion_opciones = document.getElementById('ubicacion_nombre');
    const opciones = Array.from(denominacion_opciones.options).map(option => option.value);

    if (!opciones.includes(denominacionInput.value)) {
        denominacionInput.value = '';
    }
}

function actualizarValoresOcultos() {
    const input = document.getElementById("ubicacion");
    const options = document.getElementById("ubicacion_nombre").options;

    for (let option of options) {
        if (option.value === input.value) {
            document.getElementById("id_ubicacion").value = option.getAttribute("data-cod-id");
            break; 
        }
    }
}