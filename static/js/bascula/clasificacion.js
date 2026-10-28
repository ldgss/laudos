let video = document.getElementById('webcam');
let canvas = document.getElementById('canvas-dibujo');
let ctx = canvas.getContext('2d');
let puntos = [];
let muestrasAcumuladas = [];
let imagenEstatica = null; 
let streamActual = null;
let animacionId = null;
let areaImagen = null;
let temporizadorDahua = null;
let dahuaActivo = false;

async function iniciarCamara() {
    detenerStreamActual();

    imagenEstatica = null;
    puntos = [];

    video.style.display = 'none';

    try {
        let stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 }
            }
        });

        streamActual = stream;
        video.srcObject = stream;

        await video.play();

        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;

        console.log("Webcam iniciada:", canvas.width, canvas.height);

        dibujarLoop();

    } catch (err) {
        console.error("No se pudo acceder a la cámara:", err);
        alert("No se pudo iniciar la webcam.");
    }
}

async function iniciarCamaraDahua() {
    detenerStreamActual();

    dahuaActivo = true;
    imagenEstatica = null;
    puntos = [];

    video.style.display = 'none';

    canvas.width = 640;
    canvas.height = 480;

    await actualizarCapturaDahua();
}

async function actualizarCapturaDahua() {
    if (!dahuaActivo) return;

    try {
        const response = await fetch(
            '/bascula/captura_dahua',
            { cache: 'no-store' }
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        const img = new Image();

        img.onload = () => {
            URL.revokeObjectURL(imageUrl);

            if (!dahuaActivo) return;

            imagenEstatica = img;
            redibujarEscenario();

            temporizadorDahua = setTimeout(
                actualizarCapturaDahua,
                1000
            );
        };

        img.onerror = () => {
            URL.revokeObjectURL(imageUrl);
            console.error('No se pudo decodificar la imagen Dahua.');
            temporizadorDahua = setTimeout(
                actualizarCapturaDahua,
                2000
            );
        };

        img.src = imageUrl;

    } catch (error) {
        console.error('Error obteniendo captura Dahua:', error);

        temporizadorDahua = setTimeout(
            actualizarCapturaDahua,
            2000
        );
    }
}

function detenerStreamActual() {
    dahuaActivo = false;

    if (temporizadorDahua) {
        clearTimeout(temporizadorDahua);
        temporizadorDahua = null;
    }
    
    if (animacionId) {
        cancelAnimationFrame(animacionId);
        video.onloadedmetadata = null;
        animacionId = null;
    }
    if (streamActual) {
        streamActual.getTracks().forEach(track => track.stop());
        streamActual = null;
    }
    video.pause();
    video.srcObject = null;
    video.src = "";
}

function cambiarFuenteImagen() {
    let fuente = document.getElementById('fuente-imagen').value;
    let inputArchivo = document.getElementById('input-archivo');

    puntos = [];

    if (fuente === 'webcam') {
        inputArchivo.style.display = 'none';
        iniciarCamara();
    } else if (fuente === 'dahua') {
        inputArchivo.style.display = 'none';
        iniciarCamaraDahua();
    } else if (fuente === 'archivo') {
        imagenEstatica = null;
        detenerStreamActual();
        video.style.display = 'none';
        inputArchivo.style.display = 'block';
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
}

function cargarImagenArchivo(event) {
    let archivo = event.target.files[0];
    if (!archivo) return;

    let reader = new FileReader();

    reader.onload = function(e) {
        let img = new Image();

        img.onload = function() {
            imagenEstatica = img;
            puntos = [];

            canvas.width = 640;
            canvas.height = 480;

            redibujarEscenario();
        };

        img.src = e.target.result;
    };

    reader.readAsDataURL(archivo);
}

// Función centralizada para redibujar el canvas (imagen + puntos/líneas)
function redibujarEscenario() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (imagenEstatica) {
        areaImagen = calcularAreaImagen(
            imagenEstatica.width,
            imagenEstatica.height
        );

        ctx.drawImage(
            imagenEstatica,
            areaImagen.x,
            areaImagen.y,
            areaImagen.ancho,
            areaImagen.alto
        );

    } else if (video.readyState >= 2) {
        areaImagen = {
            x: 0,
            y: 0,
            ancho: canvas.width,
            alto: canvas.height
        };

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    }

    if (puntos.length > 0) {
        ctx.beginPath();
        ctx.moveTo(puntos[0].x, puntos[0].y);

        for (let i = 1; i < puntos.length; i++) {
            ctx.lineTo(puntos[i].x, puntos[i].y);
        }

        if (puntos.length >= 3) {
            ctx.closePath();
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
}

function dibujarLoop() {
    if (imagenEstatica) {
        animacionId = null;
        return;
    }

    redibujarEscenario();

    animacionId = requestAnimationFrame(dibujarLoop);
}

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();

    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    if (imagenEstatica && areaImagen) {
        if (
            x < areaImagen.x ||
            x > areaImagen.x + areaImagen.ancho ||
            y < areaImagen.y ||
            y > areaImagen.y + areaImagen.alto
        ) {
            return;
        }
    }

    puntos.push({
        x: Math.round(x),
        y: Math.round(y)
    });

    redibujarEscenario();
});

function reiniciarPuntos() {
    puntos = [];
    redibujarEscenario();
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

if (imagenEstatica) {
    tempCanvas.width = imagenEstatica.naturalWidth;
    tempCanvas.height = imagenEstatica.naturalHeight;
} else {
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
}

let tempCtx = tempCanvas.getContext('2d');

if (imagenEstatica) {
    tempCtx.drawImage(imagenEstatica, 0, 0);
} else {
    tempCtx.drawImage(
        video,
        0, 0,
        tempCanvas.width,
        tempCanvas.height
    );
}

let imageData = tempCanvas.toDataURL('image/jpeg', 0.9);
    
    let puntosOriginales = puntos;

if (imagenEstatica && areaImagen) {
    puntosOriginales = puntos.map(p => ({
        x: Math.round(
            (p.x - areaImagen.x) *
            imagenEstatica.width / areaImagen.ancho
        ),
        y: Math.round(
            (p.y - areaImagen.y) *
            imagenEstatica.height / areaImagen.alto
        )
    }));
}

let coordenadasStr = "[" +
    puntosOriginales.map(p => `(${p.x},${p.y})`).join(",") +
    "]";

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
        let aceptado;
        
        if (resultadoAnalisis.error) {
            alert("La muestra no es suficiente. Intente nuevamente.");
        } else {
            aceptado = confirm(`Resultado del Análisis:
                \n\nDecision: ${resultadoAnalisis.decision}
                \nDescripción: ${resultadoAnalisis.descripcion}
                \nEtapa predominante: ${resultadoAnalisis.decision}
                \n¿Deseas aceptar esta muestra e incluirla en el lote?`);
        }

        if (aceptado) {
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

function calcularAreaImagen(anchoImagen, altoImagen) {
    const escala = Math.min(
        canvas.width / anchoImagen,
        canvas.height / altoImagen
    );

    const ancho = anchoImagen * escala;
    const alto = altoImagen * escala;

    return {
        x: (canvas.width - ancho) / 2,
        y: (canvas.height - alto) / 2,
        ancho: ancho,
        alto: alto
    };
}

document.getElementById('form_agregar').addEventListener('submit', function(e) {
    if (muestrasAcumuladas.length === 0) {
        e.preventDefault();
        alert("Debes tomar y aceptar al menos una muestra antes de guardar el lote.");
        return;
    }
});

window.addEventListener('load', iniciarCamara);