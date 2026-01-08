
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

