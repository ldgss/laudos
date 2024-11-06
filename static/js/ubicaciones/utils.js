document.addEventListener('DOMContentLoaded', function () {



Quagga.init({
    inputStream: {
        name: "Live",
        type: "LiveStream",
        target: document.querySelector('#interactive'), // Selección del elemento para la transmisión
        constraints: {
            facingMode: "user" // Usa la cámara trasera
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
Quagga.onDetected(function (data) {
    document.getElementById('numero_unico').value = "Scan Result: " + data.codeResult.code;
    console.log(data.codeResult.code);
});

});