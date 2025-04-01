document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form_agregar");
    const pesoInput = document.getElementById("peso");

    // actualizar reloj por primera vez y setear el interval
    updateDateTimeField();
    setInterval(updateDateTimeField, 1000);

    if(document.getElementById("peso_en_tiempo_real")){
        pesar_en_tiempo_real()
        setInterval(pesar_en_tiempo_real, 5000)
    }


    // evitar enviar formulario con enter
    form.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
        }
    });

    // validar el peso antes de enviar
    form.addEventListener("submit", function (event) {
        const peso = parseInt(pesoInput.value, 10) || 0;
        if (peso < 1000) {
            alert("El peso debe ser al menos 1000.");
            event.preventDefault();
        }
    });
});

function pesar() {
    const boton = document.querySelector(".btn-warning");
    const inputPeso = document.getElementById("peso");
    const spinner = document.getElementById("spinner");
    // mostrar el spinner hasta que vuelva la respuesta
    spinner.style.display = "inline-block";
    // deshabilitar el boton hasta que vuelva la respuesta
    boton.setAttribute("disabled", "true");
    boton.classList.add("disabled"); // agregar clase de bootstrap

    fetch("/bascula/tara")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al obtener el peso");
            }
            return response.text();
        })
        .then(text => {
            inputPeso.value = extraerPeso(text);
        })
        .catch(error => {
            console.error("Error:", error);
            alert("No se pudo obtener el peso");
        })
        .finally(() => {
            // ocultar el spinner cuando la respuesta vuelva
            spinner.style.display = "none";
            // habilitar el boton cuando la respuesta este lista
            boton.removeAttribute("disabled");
            boton.classList.remove("disabled");
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

function extraerPeso(texto) {
    if(texto.length === 9){
        return 0
    }else{
        // Eliminar caracteres de control (\u0002 o \x02) y espacios innecesarios
        texto = texto.replace(/[\u0002\x02]/g, '').trim();
        // Buscar el número más a la derecha
        const match = texto.match(/(\d+)\D*$/);
        return match ? parseInt(match[1], 10) : 0;
    }
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

function print(){
    let datos = {
        fecha: document.querySelector("#descripcion_bascula td:nth-child(2)").innerText,
        dia: document.querySelector("#descripcion_bascula tr:nth-child(2) td").innerText,
        hora: document.querySelector("#descripcion_bascula tr:nth-child(3) td").innerText,
        modo: document.querySelector("#descripcion_bascula tr:nth-child(4) td").innerText,
        chofer: document.querySelector("#descripcion_bascula tr:nth-child(5) td").innerText,
        dominio: document.querySelector("#descripcion_bascula tr:nth-child(6) td").innerText,
        ipm: document.querySelector("#descripcion_bascula tr:nth-child(7) td").innerText,
        peso: document.querySelector("#descripcion_bascula .peso td").innerText.replace(" KG", ""),
    };

    fetch('/bascula/imprimir/sticker', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}

function pesar_en_tiempo_real() {
    const peso_en_tiempo_real = document.getElementById("peso_en_tiempo_real");

    fetch("/bascula/tara")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al obtener el peso");
            }
            return response.text();
        })
        .then(text => {
            peso_en_tiempo_real.innerText = extraerPeso(text);
        })
        .catch(error => {
            console.error("Error:", error);
            alert("No se pudo obtener el peso");
        })
}



