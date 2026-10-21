document.addEventListener("DOMContentLoaded", function () {
    const dataElement = document.getElementById("clasificacion-data");
    if (!dataElement) return;

    try {
        const clasificaciones = JSON.parse(dataElement.textContent);

        const parsePuntos = (str) => {
            const puntos = [];
            const re = /\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)/g;
            let m;
            while ((m = re.exec(str || "")) !== null) {
                puntos.push({ x: parseFloat(m[1]), y: parseFloat(m[2]) });
            }
            return puntos;
        };

        // El backend manda un repr de dict de Python (comillas simples, None/True/False)
        const parseAnalisis = (raw) => {
            if (!raw) return null;
            if (typeof raw === "object") return raw;
            try { return JSON.parse(raw); } catch (_) { }
            return JSON.parse(
                raw.replace(/'/g, '"')
                    .replace(/\bNone\b/g, 'null')
                    .replace(/\bTrue\b/g, 'true')
                    .replace(/\bFalse\b/g, 'false')
            );
        };

        clasificaciones.forEach((item, index) => {
            const idx = index + 1;
            const img = document.getElementById(`img-${idx}`);
            const canvas = document.getElementById(`canvas-${idx}`);

            if (!img || !canvas) return;

            const renderMascara = () => {
                // Canvas en píxeles reales de la imagen: las coordenadas se dibujan tal cual se guardaron
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;

                const ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                const puntos = parsePuntos(item.coordenadas_mascara);
                if (!puntos.length) return;

                const k = Math.max(1, canvas.width / 600); // escala de grosor/radio

                ctx.beginPath();
                ctx.moveTo(puntos[0].x, puntos[0].y);
                for (let i = 1; i < puntos.length; i++) ctx.lineTo(puntos[i].x, puntos[i].y);
                ctx.closePath();
                ctx.strokeStyle = '#00ff00';
                ctx.lineWidth = 4 * k;
                ctx.stroke();

                ctx.fillStyle = '#ff0000';
                puntos.forEach(p => {
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, 6 * k, 0, Math.PI * 2);
                    ctx.fill();
                });
            };

            if (img.complete && img.naturalWidth > 0) {
                renderMascara();
            } else {
                img.addEventListener("load", renderMascara);
            }

            // Renderizar la información del Análisis debajo de la imagen
            const container = document.getElementById(`analisis-container-${idx}`);
            if (item.analisis && container) {
                try {
                    const data = parseAnalisis(item.analisis);
                    
                    let decisionBadge = data.decision == 'CARGA APTA'
                        ? `<span class="badge bg-success"><i class="bi bi-check-circle"></i> ${ data.decision } </span>`
                        : `<span class="badge bg-danger"><i class="bi bi-x-circle"></i> ${ data.decision } </span>`;

                    let html = `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="mb-0 fw-bold">${data.etapa_predominante || 'Sin Etapa'}</h6>
                            ${decisionBadge}
                        </div>
                        <p class="small text-muted mb-2">${data.descripcion || ''}</p>
                        <div class="row g-2 text-center mb-3">
                            <div class="col-12">
                                <div class="p-2 border rounded bg-light">
                                    <small class="text-muted d-block">Inapto (%)</small>
                                    <strong class="text-danger">${data.inapto_pct || '0%'}</strong>
                                </div>
                            </div>
                        </div>
                    `;

                    if (data.metricas) {
    html += `<small class="fw-bold d-block mb-2">Métricas por Etapa:</small>`;
    const colors = ['#4C8B2F', '#A8B545', '#E3A23B', '#EE7B6C', '#E0442F', '#B5171B'];

    Object.entries(data.metricas).forEach(([etapa, pct], i) => {
        const val = Math.min(100, Math.max(0, parseFloat(pct) || 0));
        html += `
            <div class="mb-2">
                <div class="d-flex justify-content-between small">
                    <span class="text-capitalize">${etapa}</span>
                    <span class="fw-bold">${pct}</span>
                </div>
                <div class="progress" role="progressbar" style="height: 14px;"
                     aria-valuenow="${val}" aria-valuemin="0" aria-valuemax="100">
                    <div class="progress-bar" style="width: ${val}%; background-color: ${colors[i % colors.length]}"></div>
                </div>
            </div>`;
    });
}

                    const overlay = document.getElementById(`overlay-${idx}`);
                    if (overlay) {
                        const apta = data.decision == 'CARGA APTA'
                        overlay.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <strong>${data.etapa_predominante || 'Sin Etapa'}</strong>
            <span class="badge ${apta ? 'bg-success' : 'bg-danger'}"></span>
        </div>
        <div>${data.descripcion || ''}</div>
        <div>Inapto: ${data.inapto_pct || '0%'}</div>`;
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