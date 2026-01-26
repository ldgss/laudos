// Función para cargar y mostrar el gráfico de stock
async function cargarGraficoStock() {
  try {
    const response = await fetch('/reporte/dashboard/stock', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    // Verificar si hay datos
    if (!data || data.length === 0) {
      document.getElementById('stock_no_hay_datos').style.display = 'block';
      document.getElementById('stock_container').style.display = 'none';
      return;
    }

    // Ocultar mensaje de "no hay datos"
    document.getElementById('stock_no_hay_datos').style.display = 'none';
    document.getElementById('stock_container').style.display = 'block';

    // Preparar los datos para el gráfico
    const labels = data.map(item => item.den);
    const valores = data.map(item => item.disponible);

    // Calcular altura necesaria
    const alturaMinimaPorBarra = 50;
    const alturaTotal = Math.max(400, data.length * alturaMinimaPorBarra);
    
    const canvas = document.getElementById('stock');
    canvas.style.height = alturaTotal + 'px';

    // Crear el gráfico
    const ctx = canvas.getContext('2d');
    const chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Stock Disponible',
          data: valores,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 2,
          barPercentage: 0.7,
          categoryPercentage: 0.8
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 25,
            right: 100,
            top: 25,
            bottom: 25
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: true,
            callbacks: {
              label: function(context) {
                return 'Stock: ' + context.parsed.x.toLocaleString();
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: {
              font: {
                size: 14
              },
              callback: function(value) {
                return value.toLocaleString();
              }
            },
            grid: {
              display: true
            }
          },
          y: {
            ticks: {
              autoSkip: false,
              font: {
                size: 14
              },
              padding: 20,
              align: 'start',
              crossAlign: 'far'
            },
            grid: {
              display: false
            }
          }
        }
      },
      plugins: [{
        afterDatasetsDraw: function(chart) {
          const ctx = chart.ctx;
          chart.data.datasets.forEach(function(dataset, i) {
            const meta = chart.getDatasetMeta(i);
            meta.data.forEach(function(bar, index) {
              const data = dataset.data[index];
              ctx.fillStyle = '#333';
              ctx.font = 'bold 14px Arial';
              ctx.textAlign = 'left';
              ctx.textBaseline = 'middle';
              
              // Posicionar el texto al final de la barra + un offset
              const xPos = bar.x + 10;
              const yPos = bar.y;
              
              ctx.fillText(data.toLocaleString(), xPos, yPos);
            });
          });
        }
      }]
    });

  } catch (error) {
    console.error('Error al cargar el gráfico de stock:', error);
    document.getElementById('stock_no_hay_datos').style.display = 'block';
    document.getElementById('stock_container').style.display = 'none';
  }
}

// Llamar la función cuando cargue la página
cargarGraficoStock();

// Función para cargar y mostrar el gráfico de stock
async function cargarGraficoHojalata() {
  try {
    const response = await fetch('/reporte/dashboard/hojalata', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    // Verificar si hay datos
    if (!data || data.length === 0) {
      document.getElementById('hojalata_no_hay_datos').style.display = 'block';
      document.getElementById('hojalata_container').style.display = 'none';
      return;
    }

    // Ocultar mensaje de "no hay datos"
    document.getElementById('hojalata_no_hay_datos').style.display = 'none';
    document.getElementById('hojalata_container').style.display = 'block';

    // Preparar los datos para el gráfico
    const labels = data.map(item => item.den);
    const valores = data.map(item => item.disponible);

    // Calcular altura necesaria
    const alturaMinimaPorBarra = 50;
    const alturaTotal = Math.max(400, data.length * alturaMinimaPorBarra);
    
    const canvas = document.getElementById('hojalata');
    canvas.style.height = alturaTotal + 'px';

    // Crear el gráfico
    const ctx = canvas.getContext('2d');
    const chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'hojalata Disponible',
          data: valores,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 2,
          barPercentage: 0.7,
          categoryPercentage: 0.8
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 25,
            right: 100,
            top: 25,
            bottom: 25
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: true,
            callbacks: {
              label: function(context) {
                return 'hojalata: ' + context.parsed.x.toLocaleString();
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: {
              font: {
                size: 14
              },
              callback: function(value) {
                return value.toLocaleString();
              }
            },
            grid: {
              display: true
            }
          },
          y: {
            ticks: {
              autoSkip: false,
              font: {
                size: 14
              },
              padding: 20,
              align: 'start',
              crossAlign: 'far'
            },
            grid: {
              display: false
            }
          }
        }
      },
      plugins: [{
        afterDatasetsDraw: function(chart) {
          const ctx = chart.ctx;
          chart.data.datasets.forEach(function(dataset, i) {
            const meta = chart.getDatasetMeta(i);
            meta.data.forEach(function(bar, index) {
              const data = dataset.data[index];
              ctx.fillStyle = '#333';
              ctx.font = 'bold 14px Arial';
              ctx.textAlign = 'left';
              ctx.textBaseline = 'middle';
              
              // Posicionar el texto al final de la barra + un offset
              const xPos = bar.x + 10;
              const yPos = bar.y;
              
              ctx.fillText(data.toLocaleString(), xPos, yPos);
            });
          });
        }
      }]
    });

  } catch (error) {
    console.error('Error al cargar el gráfico de stock:', error);
    document.getElementById('stock_no_hay_datos').style.display = 'block';
    document.getElementById('stock_container').style.display = 'none';
  }
}

// Llamar la función cuando cargue la página
cargarGraficoHojalata();