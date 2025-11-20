fetch("estadisticas/filtrar", { method: "POST" })
  .then(resp => resp.json())
  .then(data => {
    // Si no hay datos → mostrar mensajes en todos los gráficos
    if (!data || data.length === 0) {
      ["acometidas", "gas", "agua_pozo", "agua_calderas", "efluente_generado"].forEach(id => {
        document.getElementById(id).style.display = "none";
        document.getElementById(id + "_null").style.display = "block";
      });
      return;
    }
        
    // FECHAS
    const labels = data.map(d => new Date(d.fecha_registro).toLocaleDateString());

    // --- ACOMETIDAS ---
    const norte = data.map(d => parseFloat(d.electricidad_acometida_norte_kw));
    const este = data.map(d => parseFloat(d.electricidad_acometida_este_kw));

    crearGraficoBarras(
      "acometidas",
      labels,
      [
        {
          label: "Acometida Norte (kW)",
          data: norte,
          backgroundColor: "rgba(250, 64, 43, 0.6)",
        },
        {
          label: "Acometida Este (kW)",
          data: este,
          backgroundColor: "rgba(255, 251, 44, 0.6)",
        }
      ],
      "kW"
    );

    // --- GAS NATURAL ---
    const gas = data.map(d => parseFloat(d.gas_natural_m3));
    crearGraficoBarras(
      "gas",
      labels,
      [
        {
          label: "Gas Natural (m³)",
          data: gas,
          backgroundColor: "rgba(154, 154, 152, 0.51)",
          tension: 0.3
        }
      ],
      "m³"
    );
    // --- AGUA POZO ---
    const agua_pozo = data.map(d => parseFloat(d.gas_natural_m3));
    crearGraficoBarras(
      "agua_pozo",
      labels,
      [
        {
          label: "Agua Pozo (m³x100)",
          data: gas,
          backgroundColor: "rgba(59, 99, 200, 0.71)",
          tension: 0.3
        }
      ],
      "m³x100"
    );
    // --- AGUA CALDERAS ---
    const agua_caldera1_m3 = data.map(d => parseFloat(d.agua_caldera1_m3));
    const agua_caldera2_m3 = data.map(d => parseFloat(d.agua_caldera2_m3));
    const agua_caldera3_m3 = data.map(d => parseFloat(d.agua_caldera3_m3));
    crearGraficoBarras(
      "agua_calderas",
      labels,
      [
        {
          label: "Caldera 1 (m³)",
          data: agua_caldera1_m3,
          backgroundColor: "rgba(104, 52, 226, 0.42)",
          tension: 0.3
        },
        {
          label: "Caldera 2 (m³)",
          data: agua_caldera2_m3,
          backgroundColor: "rgba(104, 52, 226, 0.62)",
          tension: 0.3
        },
        {
          label: "Caldera 3 (m³)",
          data: agua_caldera3_m3,
          backgroundColor: "rgba(104, 52, 226, 0.82)",
          tension: 0.3
        }
      ],
      "m³"
    );
    // --- EFLUENTE GENERADO ---
    const efluente_generado = data.map(d => parseFloat(d.efluente_generado_m3));
    crearGraficoBarras(
      "efluente_generado",
      labels,
      [
        {
          label: "Efluente generado (m³)",
          data: efluente_generado,
          backgroundColor: "rgba(51, 136, 36, 0.56)",
          tension: 0.3
        }
      ],
      "m³"
    );
  })
  .catch(err => {
    console.error("Error al cargar datos:", err);
    ["acometidas", "gas", "agua_pozo", "agua_calderas", "efluente_generado"].forEach(id => {
      document.getElementById(id).style.display = "none";
      document.getElementById(id + "_null").textContent =
        "Error al cargar los datos";
      document.getElementById(id + "_null").style.display = "block";
    });
  });


// ---------------- FUNCIONES AUXILIARES ----------------

function crearGraficoBarras(id, labels, datasets, unidad) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  new Chart(ctx, {
    type: "bar",
    data: { labels, datasets },
    options: opcionesBase(unidad)
  });
}

function crearGraficoLinea(id, labels, datasets, unidad) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  new Chart(ctx, {
    type: "line",
    data: { labels, datasets },
    options: opcionesBase(unidad)
  });
}

function opcionesBase(unidad) {
  return {
    responsive: true,
    scales: {
      x: {
        title: { display: true, text: "Fecha de registro" },
        ticks: { maxRotation: 45, minRotation: 45 }
      },
      y: {
        beginAtZero: true,
        title: { display: true, text: unidad }
      }
    },
    plugins: { legend: { position: "top" } }
  };
}

document.querySelectorAll('.btn-anular').forEach(button => {
    button.addEventListener('click', function () {
        const energia_id = this.getAttribute('data-id');
        document.getElementById('energia_id').value = energia_id;
    });
});
