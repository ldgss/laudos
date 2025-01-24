function validarMotivo() {
    //Busca en el campo de texto con el id= motivo
    const denominacionInput = document.getElementById('motivo');
    //Busca el datalist con el ID lista motivo el cual contiene las opciones validas para el campo de texto.
    const lista_motivos = document.getElementById('lista_motivos');
    //Devuelve una coleccionde todas las opciones, convierte esta coleccion en un arreglo y toma cada opcione y extrae el atributo.
    const opciones = Array.from(lista_motivos.options).map(option => option.value);
    //
    if (!opciones.includes(denominacionInput.value)) {
        denominacionInput.value = '';
    }
}
function actualizarValoresOcultos() {
    const input = document.getElementById("motivo");
    const options = document.getElementById("lista_motivos").options;

    for (let option of options) {
        if (option.value === input.value) {
            document.getElementById("id_motivo").value = option.getAttribute("data-id-motivo");
            
            break; 
        }
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

// function liberar_modal(e){
//     const numerounico = document.getElementById('numero_unico_modal').value;
//     if (!numerounico.trim()) {
//         alert('Por favor, ingrese un numero unico');
//         return;
//     }
//     alert("aprestaste el modal"+e)
    
// }

document.addEventListener("DOMContentLoaded", function () {
    const botonesLiberar = document.querySelectorAll(".boton_liberar_modal");

    botonesLiberar.forEach(boton => {
        boton.addEventListener("click", function () {
            const fila = this.closest("tr"); // Encuentra la fila del botón

            // Captura los datos de la fila
            const numeroUnico = fila.querySelector("td:nth-child(1)").textContent.trim();
            const denominacion = fila.querySelector("td:nth-child(2)").textContent.trim();
            const motivo = fila.querySelector("td:nth-child(3)").textContent.trim();
            const fechaBloqueo = fila.querySelector("td:nth-child(4)").textContent.trim();

            // Muestra los datos en los campos del modal
            document.getElementById("numero_unico_modal").value = numeroUnico;
            document.getElementById("denominacion_modal").value = denominacion;
            document.getElementById("motivo_modal").value = motivo;
            document.getElementById("fecha_bloqueo_modal").value = fechaBloqueo;

            // Generar la fecha actual y mostrarla en el modal
            const ahora = new Date();
            const fechaActual = ahora.toISOString().slice(0, 10); // Formato: YYYY-MM-DD
            const horaActual = ahora.toTimeString().slice(0, 5); // Formato: HH:mm:ss
            document.getElementById("fecha_actual_modal").value = fechaActual + " " + horaActual;

            // Limpiar el campo de observaciones (por si quedó algo de una apertura anterior)
            document.getElementById("observaciones_modal").value = "";
        });
    });

    // Enviar datos al backend al confirmar
    document.querySelector(".btn-primary").addEventListener("click", function () {
        const numeroUnico = document.getElementById("numero_unico_modal").value.trim();
        const denominacion = document.getElementById("denominacion_modal").value.trim();
        const motivo = document.getElementById("motivo_modal").value.trim();
        const fechaBloqueo = document.getElementById("fecha_bloqueo_modal").value.trim();
        const fechaActual = document.getElementById("fecha_actual_modal").value.trim();
        const usuario = document.getElementById("user_id_modal").value.trim();
        const observaciones = document.getElementById("observaciones_modal").value.trim();

        // Validar los campos antes de enviar
        if (!numeroUnico || !denominacion || !motivo || !fechaBloqueo || !fechaActual) {
            alert("Todos los campos son obligatorios.");
            return;
        }

        // Enviar los datos al backend
        fetch('/bloqueos_produccion/agregar/liberacion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                numero_unico: numeroUnico,
                denominacion: denominacion,
                motivo: motivo,
                fecha_bloqueo: fechaBloqueo,
                fecha_actual: fechaActual,
                id_usuario: usuario,
                observaciones: observaciones
            }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    $('staticBackdrop').modal('hide')
                    alert("Datos guardados exitosamente");
                } else {
                    alert("Error:" + data.error);
                    const modal = bootstrap.Modal.getInstance(document.getElementById("staticBackdrop"));
                    modal.hide();
                }
            })
            .catch(error => {
                console.error("Error al enviar los datos:", error);
                alert("Hubo un problema al guardar los datos.");
            });
    });
});

// function capturarDatosModal() {
//     // Capturar el valor del campo del modal
//     const numeroUnico = document.getElementById("numero_unico_modal").value.trim();

//     if (!numeroUnico) {
//         alert("Por favor, complete el Número Único.");
//         return;
//     }

//     // Enviar datos al servidor
//     enviarDatosAlServidor({ numero_unico: numeroUnico });
// }
try {
    window.addEventListener('load', actualizarFechaYHora);
} catch (error) {
    // console.log(error)
}