let total_escaneado = document.getElementById("total_escaneado");
let total_escaneado_value = 0;
const codigos_escaneados = new Set();

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
        // return Array.from(document.querySelectorAll("#lista_numero_unico input"))
        //     .some(input => input.value === codigo);
        return codigos_escaneados.has(codigo)
    }

    Quagga.onDetected(function (result) {
        let codigoBarras = result.codeResult.code;
        if (pattern.test(codigoBarras) && !existeEscaneo(codigoBarras)) {
            document.getElementById("escaneo").value = codigoBarras;
            beepSound.play()
        }
    });

    function agregarEscaneo(numeroUnicoValor, despachado, detalles) {
        let agotado = chequear_agotado(detalles)
        // total mostrado al lado del boton agregar
        total_escaneado_value++;
        total_escaneado.innerText = total_escaneado_value

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
        input.style.border = `1px solid ${despachado || agotado ? "red" : "green"}`;
        input.style.boxShadow = `${despachado || agotado ? "red" : "green"} 0px 0px 5px`;

        let divBtnCol = document.createElement("div");
        divBtnCol.className = "col-sm-2";

        let btnEliminar = document.createElement("button");
        btnEliminar.className = "btn btn-danger";
        btnEliminar.innerText = "Eliminar";
        btnEliminar.onclick = function () {
            let elemento = document.getElementById(rowId);
            if (elemento) {
                elemento.remove();
                codigos_escaneados.delete(numeroUnicoValor)
            }
            total_escaneado_value--;
            total_escaneado.innerText = total_escaneado_value
        };

        // Contenedor para la información de despacho
        let despachoInfoContainer = document.createElement("div");
        despachoInfoContainer.className = "mt-2";
        let despachoEstado = document.createElement("p");
        if(despachado){
            despachoEstado.innerHTML = `<p>Estado: Despachado el dia ${detalles[0]["despachado"]}</p>`
        }else if(agotado){
            despachoEstado.innerHTML = `<p>Estado: Agotado</p>`
        }else{
            despachoEstado.innerHTML = `<p>Estado: Disponible</p>`
        }
        despachoInfoContainer.appendChild(despachoEstado);

        detalles.forEach((detalle) => {
            let despachoInfo = document.createElement("p");
            let den = detalle["m3_den"] || detalle["m_den"] || detalle["e3_den"] || detalle["e_den"] || detalle["h_den"] || detalle["m2_den"] || detalle["e2_den"] || "-";
            let lote = detalle["m3_lote"] || detalle["m_lote"] || detalle["e3_lote"] || detalle["e_lote"] || detalle["h_lote"] || detalle["m2_lote"] || detalle["e2_lote"] || "-";
            despachoInfo.innerHTML = `<p>${den}</p> <p>${lote}</p>`;
            despachoInfoContainer.appendChild(despachoInfo);
        });



        divCol.appendChild(input);
        divCol.appendChild(despachoInfoContainer);
        divBtnCol.appendChild(btnEliminar);
        divRow.appendChild(divCol);
        divRow.appendChild(divBtnCol);

        document.getElementById("lista_numero_unico").appendChild(divRow);
    }

    function chequear_agotado(detalles){
        return !detalles.some((detalle) =>
            detalle["m_cantidad"] ||
            detalle["m3_cantidad"] ||
            detalle["m2_cantidad"] ||
            detalle["h_cantidad"] ||
            detalle["e_cantidad"] ||
            detalle["e3_cantidad"] ||
            detalle["e2_cantidad"]
        );
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

        // si no esta agregado, lo hacemos aca
        codigos_escaneados.add(numeroUnicoValor)

        document.getElementById("escaneo").value = ""
        // agregamos solo despues de conocer el estado del pallet, despachado o no
        // agregarEscaneo(numeroUnicoValor);

        // chequear el estado del pallet
        // si existe, si esta despachado, nombre del producto y lote
        fetch("/despacho/detalle", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ numeroUnico: numeroUnicoValor })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la petición: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            try{
                if (!data || !Array.isArray(data)) {
                    throw new Error("Error al obtener el pallet o no existe. C1");
                }

                // agregamos el pallet pero avisando si esta despachado o no
                // si no hay detalle, el pallet no se ha despachado y se contornea verde
                // si hay detalle, el pallet se ha despachado y se contornea rojo
                const despachado = data.length > 0 && data.some(item => item.hasOwnProperty('despachado') && item['despachado']);
                agregarEscaneo(numeroUnicoValor, despachado, data);
            } catch (error) {
                alert("Error al obtener el pallet o no existe. C2:", error);
            }
        })
        .catch(error => console.error("Error al obtener el pallet o no existe. C3:", error));
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
         let despachados = document.querySelectorAll("#lista_numero_unico p");

         if (inputs.length === 0) {
             alert("Debe agregar al menos un escaneo antes de enviar el formulario.");
             event.preventDefault();
         }

         for (let p of despachados) {
            if (p.textContent.toLowerCase().includes("despachado")) {
                alert("Algunos elementos ya fueron despachados, revise e intente de nuevo");
                event.preventDefault();
                return;
            }
        }
     });
});


