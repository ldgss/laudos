document.addEventListener("DOMContentLoaded", function () {
    const dataElement = document.getElementById("clasificacion-data");
    if (!dataElement) return;

    try {
        const clasificaciones = JSON.parse(dataElement.textContent);

        clasificaciones.forEach((item, index) => {
            const idx = index + 1;
            const img = document.getElementById(`img-${idx}`);
            const canvas = document.getElementById(`canvas-${idx}`);

            if (!img || !canvas) return;

            // Función para renderizar el dibujo idéntico al momento de analizar
            const renderMascara = () => {
                // Ajustar resolución interna del Canvas a la resolución real de la imagen
                canvas.width = img.naturalWidth || img.clientWidth;
                canvas.height = img.naturalHeight || img.clientHeight;

                const ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                if (item.coordenadas_mascara) {
                    try {
                        // Parsear la cadena '[(348,19),(382,441)...]' a un array de objetos [{x, y}]
                        let rawStr = item.coordenadas_mascara
                            .replace(/\[\vert{}\]/g, '') // Eliminar corchetes
                            .trim();

                        // Extraer cada par (x,y)
                        let regex = /\((\d+),\s*(\d+)\)/g;
                        let match;
                        let puntos = [];

                        while ((match = regex.exec(rawStr)) !== null) {
                            puntos.push({
                                x: parseInt(match[1], 10),
                                y: parseInt(match[2], 10)
                            });
                        }

                        // Dibujar tal cual el loop de análisis
                        if (puntos.length > 0) {
                            // 1. Trazar líneas del polígono
                            ctx.beginPath();
                            ctx.moveTo(puntos[0].x, puntos[0].y);
                            for (let i = 1; i < puntos.length; i++) {
                                ctx.lineTo(puntos[i].x, puntos[i].y);
                            }
                            // Cerrar la figura si es un área completa
                            ctx.closePath();
                            ctx.strokeStyle = '#00ff00';
                            ctx.lineWidth = 4;
                            ctx.stroke();

                            // Relleno semitransparente suave opcional para destacar el área
                            ctx.fillStyle = 'rgba(0, 255, 0, 0.15)';
                            ctx.fill();

                            // 2. Dibujar vértices
                            puntos.forEach(p => {
                                ctx.fillStyle = '#ff0000';
                                ctx.beginPath();
                                ctx.arc(p.x, p.y, 6, 0, Math.PI * 2);
                                ctx.fill();
                            });
                        }
                    } catch (e) {
                        console.error(`Error al procesar la máscara de la muestra #${idx}:`, e);
                    }
                }
            };

            // Ejecutar el renderizado cuando la imagen esté lista
            if (img.complete) {
                renderMascara();
            } else {
                img.onload = renderMascara;
            }

            // Renderizar la información del Análisis debajo de la imagen
            const container = document.getElementById(`analisis-container-${idx}`);
            if (item.analisis && container) {
                try {
                    // Reemplazar comillas simples por dobles para parsear JSON válido
                    let jsonStr = item.analisis.replace(/'/g, '"');
                    let data = JSON.parse(jsonStr);

                    let decisionBadge = data.decision === 'CARGA APTA' 
                        ? '<span class="badge bg-success fs-6"><i class="bi bi-check-circle"></i> APTA</span>' 
                        : '<span class="badge bg-danger fs-6"><i class="bi bi-x-circle"></i> NO APTA</span>';

                    let html = `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="mb-0 fw-bold">${data.etapa_predominante || 'Sin Etapa'}</h6>
                            ${decisionBadge}
                        </div>
                        <p class="small text-muted mb-2">${data.descripcion || ''}</p>
                        <div class="row g-2 text-center mb-3">
                            <div class="col-6">
                                <div class="p-2 border rounded bg-light">
                                    <small class="text-muted d-block">Tomates Detectados</small>
                                    <strong>${data.tomates_detectados ?? 0}</strong>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="p-2 border rounded bg-light">
                                    <small class="text-muted d-block">Inapto (%)</small>
                                    <strong class="text-danger">${data.inapto_pct || '0%'}</strong>
                                </div>
                            </div>
                        </div>
                    `;

                    if (data.metricas) {
                        html += `<small class="fw-bold d-block mb-1">Métricas por Etapa:</small><div class="progress-stacked mb-2" style="height: 20px;">`;
                        const colors = ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545', '#6c757d'];
                        let colorIdx = 0;

                        for (const [etapa, pct] of Object.entries(data.metricas)) {
                            let val = parseFloat(pct);
                            if (val > 0) {
                                let bg = colors[colorIdx % colors.length];
                                html += `
                                    <div class="progress" role="progressbar" style="width: ${val}%" title="${etapa}: ${pct}">
                                        <div class="progress-bar" style="background-color: ${bg}">${etapa}: ${pct}</div>
                                    </div>`;
                            }
                            colorIdx++;
                        }
                        html += `</div>`;
                    }

                    container.innerHTML = html;
                } catch (e) {
                    console.error(`Error al procesar el JSON de análisis de la muestra #${idx}:`, e);
                    container.innerHTML = `<p class="text-muted small">${item.analisis}</p>`;
                }
            }
        });
    } catch (e) {
        console.error("Error al parsear el JSON global de clasificaciones:", e);
    }
});