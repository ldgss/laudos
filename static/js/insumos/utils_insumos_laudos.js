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

        const btnBuscar = document.getElementById("btnBuscar");
        btnBuscar.classList.add("boton-destello");
        setTimeout(() => {
            btnBuscar.classList.remove("boton-destello");
        }, 5000);
    } else {
        console.log("Código no válido:", detectedCode);
    }
});

});

document.getElementById("buscar_insumo").addEventListener("submit", function (e) {
    e.preventDefault(); // evita el submit tradicional

    const form = e.target;
    const formData = new FormData(form);

    fetch("/insumos/buscar_insumo_laudo", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }
        return response.json(); // o .text() según lo que devuelva tu backend
    })
    .then(data => {
        if(!data["error"]){
            console.log("Respuesta:", data);
            cta_alm = document.getElementById("cta_alm")
            cta_alm.value = data["producto"]
            cod_lot = document.getElementById("cod_lot")
            cod_lot.value = data["lote"]
            den_fac = document.getElementById("den_fac")
            den_fac.value = data["numero_unico"]
            can = document.getElementById("can")
            can.value = data["cantidad"]
        }else{
            alert("El pallet ya fue consumido como insumo")
        }
    })
    .catch(error => {
        alert("Numero de parte no encontrado")
        console.log(error)
    });
});

