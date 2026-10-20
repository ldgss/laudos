let video = document.getElementById('webcam');
let canvas = document.getElementById('canvas-dibujo');
let ctx = canvas.getContext('2d');
let puntos = [];
let nativeWidth = 640;   // Resolución base recomendada
let nativeHeight = 480;

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
    // Dibujar el fotograma actual de la cámara
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Dibujar el polígono si hay puntos
    if (puntos.length > 0) {
        ctx.beginPath();
        ctx.moveTo(puntos[0].x, puntos[0].y);
        for (let i = 1; i < puntos.length; i++) {
            ctx.lineTo(puntos[i].x, puntos[i].y);
        }
        ctx.strokeStyle = '#00ff00'; // Verde brillante para destacar
        ctx.lineWidth = 4;
        ctx.stroke();

        // Dibujar círculos en los vértices
        puntos.forEach(p => {
            ctx.fillStyle = '#ff0000';
            ctx.beginPath();
            ctx.arc(p.x, p.y, 6, 0, Math.PI * 2);
            ctx.fill();
        });
    }
    requestAnimationFrame(dibujarLoop);
}

// Capturar clics en el canvas y escalar las coordenadas al tamaño real del video
canvas.addEventListener('click', (e) => {
    let rect = canvas.getBoundingClientRect();
    let scaleX = canvas.width / rect.width;
    let scaleY = canvas.height / rect.height;
    
    let x = Math.round((e.clientX - rect.left) * scaleX);
    let y = Math.round((e.clientY - rect.top) * scaleY);
    
    puntos.push({x, y});
    actualizarInputCoordenadas();
});

function reiniciarPuntos() {
    puntos = [];
    actualizarInputCoordenadas();
}

function actualizarInputCoordenadas() {
    // Genera el formato de lista de tuplas exacto: [(x1,y1),(x2,y2)...]
    let tuplesStr = "[" + puntos.map(p => `(${p.x},${p.y})`).join(",") + "]";
    document.getElementById('coordenadas').value = tuplesStr;
}

// Capturar el evento de submit del formulario para guardar la foto actual
document.getElementById('form_agregar').addEventListener('submit', function(e) {
    // Dibujar el fotograma actual limpio en un canvas temporal o en el mismo
    let tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth || 640;
    tempCanvas.height = video.videoHeight || 480;
    let tempCtx = tempCanvas.getContext('2d');
    
    // Copiar la imagen del video (sin las líneas verdes del dibujo de usuario)
    tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
    
    // Guardar como Base64 en el input oculto
    document.getElementById('image_data').value = tempCanvas.toDataURL('image/jpeg', 0.9);
});

// Iniciar automáticamente al cargar
window.addEventListener('load', iniciarCamara);