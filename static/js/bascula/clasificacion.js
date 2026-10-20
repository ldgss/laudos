let video = document.getElementById('webcam');
let canvas = document.getElementById('canvas-dibujo');
let ctx = canvas.getContext('2d');
let puntos = [];
let nativeWidth = 640; 
let nativeHeight = 480;

let muestrasAcumuladas = [];

async function iniciarCamara() {
    try {
        let stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: { ideal: nativeWidth }, height: { ideal: nativeHeight } } 
        });
        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            nativeWidth = video.videoWidth;
            nativeHeight = video.videoHeight;
            canvas.width = nativeWidth;
            canvas.height = nativeHeight;
            requestAnimationFrame(dibujarLoop);
        };
    } catch (err) {
        console.error("No se pudo acceder a la cámara: ", err);
        alert("Asegúrate de dar permisos de cámara o usar HTTPS/localhost.");
    }
}

function dibujarLoop() {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    if (puntos.length > 0) {
        ctx.beginPath();
        ctx.moveTo(puntos[0].x, puntos[0].y);
        for (let i = 1; i < puntos.length; i++) {
            ctx.lineTo(puntos[i].x, puntos[i].y);
        }
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 4;
        ctx.stroke();

        puntos.forEach(p => {
            ctx.fillStyle = '#ff0000';
            ctx.beginPath();
            ctx.arc(p.x, p.y, 6, 0, Math.PI * 2);
            ctx.fill();
        });
    }
    requestAnimationFrame(dibujarLoop);
}

canvas.addEventListener('click', (e) => {
    let rect = canvas.getBoundingClientRect();
    let scaleX = canvas.width / rect.width;
    let scaleY = canvas.height / rect.height;
    
    let x = Math.round((e.clientX - rect.left) * scaleX);
    let y = Math.round((e.clientY - rect.top) * scaleY);
    
    puntos.push({x, y});
});

function reiniciarPuntos() {
    puntos = [];
}

async function analizarMuestra() {
    if (puntos.length < 4) {
        alert("Debes marcar al menos 4 puntos para definir la zona de tomates.");
        return;
    }

    let ipmVal = document.getElementById('ipm').value;
    let pesoVal = document.getElementById('peso').value;

    if (!ipmVal) {
        alert("Por favor, completa el campo IPM antes de analizar.");
        return;
    }

    let tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth || 640;
    tempCanvas.height = video.videoHeight || 480;
    let tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
    let imageData = tempCanvas.toDataURL('image/jpeg', 0.9);

    let coordenadasStr = "[" + puntos.map(p => `(${p.x},${p.y})`).join(",") + "]";

    try {
        let response = await fetch('clasificar_muestra', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ipm: ipmVal,
                peso: pesoVal,
                image_data: imageData,
                coordenadas: coordenadasStr
            })
        });

        if (!response.ok) throw new Error("Error en el servidor al analizar.");
        
        let data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }

        let resultadoAnalisis = data.analisis || "Análisis completado exitosamente";
        console.log(resultadoAnalisis)
        let aceptado = confirm(`Resultado del Análisis:
            \n\nDecision: ${resultadoAnalisis.decision}
            \n\nDescripción: ${resultadoAnalisis.descripcion}
            \n\nEtapa predominante: ${resultadoAnalisis.decision}
            \n\n¿Deseas aceptar esta muestra e incluirla en el lote?`);

        if (aceptado) {
            // Guardamos todo en memoria, incluyendo la imagen en Base64 para enviarla al guardar el lote
            muestrasAcumuladas.push({
                image_data: imageData,
                coordenadas: coordenadasStr,
                analisis: resultadoAnalisis
            });

            reiniciarPuntos();
            actualizarInterfazMuestras();
        }

    } catch (error) {
        console.error(error);
        alert("Ocurrió un error al procesar el análisis por AJAX.");
    }
}

function actualizarInterfazMuestras() {
    let contenedor = document.getElementById('contenedor-muestras');
    contenedor.innerHTML = '';

    muestrasAcumuladas.forEach((muestra, index) => {
        let badge = document.createElement('div');
        badge.className = 'alert alert-secondary d-flex justify-content-between align-items-center py-2 px-3 mb-2';
        badge.innerHTML = `
            <span><strong>Muestra #${index + 1}</strong></span>
            <button type="button" class="btn btn-close btn-sm" aria-label="Eliminar" onclick="eliminarMuestra(${index})"></button>
        `;
        contenedor.appendChild(badge);
    });

    document.getElementById('muestras_json').value = JSON.stringify(muestrasAcumuladas);
}

function eliminarMuestra(index) {
    muestrasAcumuladas.splice(index, 1);
    actualizarInterfazMuestras();
}

document.getElementById('form_agregar').addEventListener('submit', function(e) {
    if (muestrasAcumuladas.length === 0) {
        e.preventDefault();
        alert("Debes tomar y aceptar al menos una muestra antes de guardar el lote.");
        return;
    }
});

window.addEventListener('load', iniciarCamara);