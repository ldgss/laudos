
document.getElementById("buscar").addEventListener("click", async function (e) {
    e.preventDefault();

    const valor = document.getElementById("denominacion").value.trim();

    if (!valor) {
        alert("Debe ingresar una denominación.");
        return;
    }

    const opciones = document.querySelectorAll("#denominacion_opciones option");

    let opcionEncontrada = null;
    opciones.forEach(op => {
        if (op.value.trim() === valor) {
            opcionEncontrada = op;
        }
    });

    if (!opcionEncontrada) {
        alert("No se encontró la denominación seleccionada.");
        return;
    }

    const codigo = opcionEncontrada.dataset.codigo;
    const clase = opcionEncontrada.dataset.clase;

    let existente = null;

    try {
        const response = await fetch(`/etiquetasystickers/buscar`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                codigo: codigo,
                denominacion: valor
            })
        });

        if (response.ok) {
            const data = await response.json();
            console.log(`data: ${data}`)
            if (data[0]) {
                existente = data[0];
                console.log(`existente: ${existente}`)
            }
        }
    } catch (error) {
        console.error("Error consultando API:", error);
    }


    // esto se completa siempre
    document.getElementById("codigo_modal").value = codigo;
    document.getElementById("clase_modal").value = clase;
    document.getElementById("denominacion_modal").value = valor;
    document.getElementById("denominacion_modal_visible").value = valor;

    const contenedorImagenes = document.getElementById("imagenes_existentes");
    contenedorImagenes.innerHTML = "";

    // si ya tenia foto, mostrarla
    if (existente) {
        const id = document.getElementById("id_modal")
        id.value = existente.id
        let imagenes = [];

        if (existente.imagen) {

            if (typeof existente.imagen === "string") {
                try {
                    imagenes = JSON.parse(existente.imagen);
                } catch (e) {
                    console.warn("Imagen venía como string pero no se pudo parsear:", e);
                    imagenes = [];
                }
            }

            else if (Array.isArray(existente.imagen)) {
                imagenes = existente.imagen;
            }

            else {
                imagenes = [existente.imagen];
            }

            imagenes.forEach(img => {
                const ruta = img.replace(/\\/g, "/");
                const div = document.createElement("div");
                div.className = "mt-3";
                div.innerHTML = `
                    <img src="${ruta}" class="img-thumbnail" alt="imagen existente"
                        style="max-width: 200px; cursor: pointer;"
                        onclick="abrirImagen('${ruta}')">
                `;

                contenedorImagenes.appendChild(div);
            });

        } else {
            contenedorImagenes.innerHTML = "<p class='text-muted'>No hay imágenes registradas.</p>";
        }
    }
    const modal = new bootstrap.Modal(document.getElementById("modal_etiquetasystickers"));
    modal.show();
});

function abrirImagen(src) {
    document.getElementById("imagenAmpliada").src = src;
    const modal = new bootstrap.Modal(document.getElementById("modalImagen"));
    modal.show();
}

function abrirImagenJinja(src){
    src = src.replace(
        '/static/img/etiquetasystickers',
        '/static/img/etiquetasystickers/'
    );
    document.getElementById("imagenAmpliada").src = src;
    const modal = new bootstrap.Modal(document.getElementById("modalImagen"));
    modal.show();
}
