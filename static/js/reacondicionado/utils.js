document.getElementById("btn_agregar").addEventListener("click", function() {
    const nuevoDiv = document.createElement("div");
    nuevoDiv.classList.add("row", "m-4", "justify-content-center");

    nuevoDiv.innerHTML = `
        <div class="row m-4 justify-content-center">
            <hr class="col-7">
        </div>
        <label for="parte" class="col-sm-2 col-form-label">Numero de parte</label>
        <div class="col-sm-5 d-flex align-items-center">
            <input required type="text" class="form-control me-1 w-75"
                name="numeros_unicos"
                title="(Ej: 2024-T1-000001, 2024-T2-000001)" 
                pattern="^\\d{4}-(T1|T2)-\\d{6}$">

            <button type="button" class="btn btn-outline-secondary btn-sm p-2 me-1" onclick="buscarParte(this)">
                Buscar
            </button>

            <button type="button" class="btn btn-outline-danger btn-sm p-2" onclick="eliminarParte(this)">
                Cancelar
            </button>

        </div>
        <div class="cantidades_placeholder"></div>
    `;

    // Insertar el nuevo div en el contenedor
    document.getElementById("contenedor_partes").appendChild(nuevoDiv);

});

function buscarParte(button) {
    const inputNumeroUnico = button.previousElementSibling;
    const rowContainer = button.closest(".row");  // Encuentra el contenedor de esta fila
    if (inputNumeroUnico.validity.patternMismatch) {
        console.log("Formato incorrecto en numero_unico");
    } else if (inputNumeroUnico.value !== "") {
        console.log("searching")
        fetch("/reacondicionado/buscart1t2t/" + inputNumeroUnico.value)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la solicitud: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data)

                const cantidades_placeholder = rowContainer.querySelector(".cantidades_placeholder");
                cantidades_placeholder.innerHTML = ""; // Limpia antes de insertar

                const nuevoDiv = document.createElement("div");
                if(data["reacondicionado"].length > 1){

                    for (let i = 0; i < data["reacondicionado"].length; i++) {
                        console.log(`detalle id: ${data["reacondicionado"][i]["id"]}`)
                        console.log(`detalle cantidad: ${data["reacondicionado"][i]["cantidad"]}`)
                        nuevoDiv.innerHTML += `
                        <!-- Nueva fila para Cantidad disponible y Cantidad a tomar -->
                        <div class="row m-4 justify-content-center">
                            <label for="cantidad" class="col-sm-2 col-form-label">Detalle</label>
                            <div class="col-sm-5 d-flex align-items-center">
                                ${data["reacondicionado"][i]["lote"]}
                            </div>
                        </div>
                        <div class="row m-4 justify-content-center">
                            <label for="cantidad" class="col-sm-2 col-form-label">Cantidades</label>
                            <div class="col-sm-5 d-flex align-items-center cantidades">
                                <input hidden name="id_a_tomar" type="text" value="${data["reacondicionado"][i]["id"]}">
                                <input hidden name="mercaderia_original" type="text" value="${data["reacondicionado"][i]["mercaderia_original"]}">
                                <input type="number" class="form-control me-1" placeholder="Cantidad disponible" name="cantidad_disponible" min="0" readonly value="${data["reacondicionado"][i]["cantidad"]}">
                                <input type="number" class="form-control" placeholder="Cantidad a tomar" name="cantidad_tomar" min="0" required>
                            </div>
                        </div>
                        `
                    }
                }else{
                    nuevoDiv.innerHTML += `
                        <!-- Nueva fila para Cantidad disponible y Cantidad a tomar -->
                        <div class="row m-4 justify-content-center">
                            <label for="cantidad" class="col-sm-2 col-form-label">Detalle</label>
                            <div class="col-sm-5 d-flex align-items-center">
                                ${data["lote"]}
                            </div>
                        </div>
                        <div class="row m-4 justify-content-center">
                            <label for="cantidad" class="col-sm-2 col-form-label">Cantidades</label>
                            <div class="col-sm-5 d-flex align-items-center cantidades">
                                <input hidden name="id_a_tomar" type="text" value="${data["id"]}">
                                <input hidden name="mercaderia_original" type="text" value="${data["id"]}">
                                <input type="number" class="form-control me-1" placeholder="Cantidad disponible" name="cantidad_disponible" min="0" readonly value="${data["cantidad"]}">
                                <input type="number" class="form-control" placeholder="Cantidad a tomar" name="cantidad_tomar" min="0" required>
                            </div>
                        </div>
                        `
                }
                cantidades_placeholder.appendChild(nuevoDiv);

                // data["reacondicionado"].forEach((item, index) => {
                //     if (rowContainer) {
                //         const cantidadDisponibleInputs = rowContainer.querySelectorAll('input[name="cantidad_disponible"]');
                //         const idATomarInputs = rowContainer.querySelectorAll('input[name="id_a_tomar"]');
                        
                //         cantidadDisponibleInputs.forEach((cantidadInput, i) => {
                //             console.log("filling fields")
                //             if (data[i]) {
                //                 cantidadInput.value = data[i].cantidad;
                //             }
                //         });

                //         idATomarInputs.forEach((idInput, i) => {
                //             if (data[i]) {
                //                 idInput.value = data[i].id;
                //             }
                //         });

                //         const cantidadTomarInput = rowContainer.querySelector('input[name="cantidad_tomar"]');
                //         if (cantidadTomarInput) {
                //             cantidadTomarInput.focus();
                //         }
                //     }
                // });

            })
            .catch(error => {
                console.error("Hubo un error:", error);
            });
    }
}


function eliminarParte(button) {
    const row = button.closest(".row");
    row.remove();
}

function validarFormulario() {
    console.log("validando")
    const pares = document.querySelectorAll('.cantidades'); // Selecciona cada contenedor de pares
    if(pares.length !== 0){
        let valido = true;
        pares.forEach((par) => {
            const cantidadDisponible = par.querySelector('input[name="cantidad_disponible"]');
            const cantidadTomar = par.querySelector('input[name="cantidad_tomar"]');

            // Validación de cantidad_disponible no vacío y mayor a 0
            if (!cantidadDisponible.value) {
                alert("'Cantidad disponible'no puede estar vacia.");
                valido = false;
                return;
            }

            // Validación de cantidad_tomar no mayor que cantidad_disponible
            if (parseFloat(cantidadTomar.value) > parseFloat(cantidadDisponible.value)) {
                alert("La 'Cantidad a tomar' no puede ser mayor que la 'Cantidad disponible'.");
                valido = false;
                return;
            }
        });

        return valido;  // Si alguna validación falla, `valido` será `false`, y el formulario no se enviará
    }else{
        alert("Especifique una composicion")
        return false;
    }
}

