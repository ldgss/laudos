document.getElementById('form_buscar').addEventListener('submit', async function (e) {
    e.preventDefault();

    const numeroUnico = document.getElementById('numero_unico').value;
    const tipo = numeroUnico.match(/-(T1|H1|E1)-/);

    if (!tipo) {
        alert('El número único no es válido.');
        return;
    }

    try {
        const response = await fetch('/correccion/seleccionar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ numero_unico: numeroUnico })
        });

        if (!response.ok) {
            alert('Error al obtener datos del servidor.');
            return;
        }

        const data = await response.json();

        let modalId;

        if (tipo[1] === 'T1') {
            modalId = 'modal1';
        } else if (tipo[2] === 'H1') {
            modalId = 'modal2';
        } else {
            modalId = 'modal3';
        }

        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
        console.log(data)
        // Popular los campos del formulario (modal1 en este caso)
        if (modalId === 'modal1') {
            document.getElementById('denominacion_modal1').value = data['den'] || '';

            // Manejo de fecha y hora
            const fechaHora = data['fecha_elaboracion'] || data['fecha_etiquetado'] || data['fecha_encajonado'] || '';
            let tipoFechaSeleccionada = '';

            if (fechaHora) {
                const fechaObj = new Date(fechaHora); // Convertir la fecha al objeto Date
                if (!isNaN(fechaObj)) {
                    // Formatear fecha y hora
                    const fecha = fechaObj.toISOString().split('T')[0]; // Formato YYYY-MM-DD
                    const hora = fechaObj.toTimeString().split(' ')[0]; // Formato HH:MM:SS
                    document.getElementById('fecha_modal1').value = fecha;
                    document.getElementById('hora_modal1').value = hora.slice(0, 5); // HH:MM

                    // Determinar el tipo de fecha seleccionada
                    if (data['fecha_elaboracion']) {
                        tipoFechaSeleccionada = 'tipo_fecha_elaboracion';
                    } else if (data['fecha_etiquetado']) {
                        tipoFechaSeleccionada = 'tipo_fecha_etiquetado';
                    } else if (data['fecha_encajonado']) {
                        tipoFechaSeleccionada = 'tipo_fecha_encajonado';
                    }
                }
            } else {
                document.getElementById('fecha_modal1').value = '';
                document.getElementById('hora_modal1').value = '';
            }

            // Seleccionar el radio correspondiente
            if (tipoFechaSeleccionada) {
                const radio = document.querySelector(`input[name="tipo_fecha_modal1"][value="${tipoFechaSeleccionada}"]`);
                if (radio) {
                    radio.checked = true;
                }
            } else {
                // Si no hay una fecha válida, deseleccionar todos los radios
                document.querySelectorAll('input[name="tipo_fecha_modal1"]').forEach(radio => {
                    radio.checked = false;
                });
            }


            // Manejo del lote
            const lote = data['lote'] || ''; // Suponiendo que la llave sea "lote"
            if (lote) {
                const [lote_a, lote_b, lote_c] = lote.split('-');
                document.getElementById('lote_a_modal1').value = lote_a || '';
                document.getElementById('lote_b_modal1').value = lote_b || '';
                document.getElementById('lote_c_modal1').value = lote_c || '';
            } else {
                document.getElementById('lote_a_modal1').value = '';
                document.getElementById('lote_b_modal1').value = '';
                document.getElementById('lote_c_modal1').value = '';
            }

            document.getElementById('cantidad_modal1').value = data['cantidad'] || '';
            document.getElementById('observaciones_modal1').value = data['observacion'] || '';

            // Popular campos ocultos si existen en los datos
            document.getElementById('cod_cls_modal1').value = data['cod_cls'] || '';
            document.getElementById('cod_mae_modal1').value = data['producto'] || '';
            document.getElementById('id_modal1').value = data['id'] || '';
            document.getElementById('numero_unico_modal1').value = data['numero_unico'] || '';
        }

        if (modalId === 'modal2') {
            // Popular el nombre de usuario y su ID
            // document.getElementById('user_name').value = data['nombre'] || '';
            // document.getElementById('user_id').value = data['id'] || '';
        
            // Popular la denominación
            document.getElementById('denominacion_modal2').value = data['den'] || '';
            document.getElementById('cod_cls_modal2').value = data['cod_cls'] || '';
            document.getElementById('cod_mae_modal2').value = data['cod_mae'] || '';
        
            // Manejo de la fecha
            const fechaHora = data['fecha_elaboracion'] || '';
            if (fechaHora) {
                const fechaObj = new Date(fechaHora); // Convertir la fecha al objeto Date
                if (!isNaN(fechaObj)) {
                    document.getElementById('fecha_modal2').value = fechaObj.toISOString().split('T')[0]; // Formato YYYY-MM-DD
                    document.getElementById('hora_modal2').value = fechaObj.toTimeString().split(' ')[0].slice(0, 5); // HH:MM
                }
            } else {
                document.getElementById('fecha_modal2').value = '';
                document.getElementById('hora_modal2').value = '';
            }
        
            // Manejo del lote
            const lote = data['lote'] || '';
            document.getElementById('lote_modal2').value = lote;
        
            // Número único
            document.getElementById('numero_unico_modal2').value = data['numero_unico'] || '';
        
            // Antecedentes
            document.getElementById('antecedentes_modal2').value = data['antecedentes'] || '';
        
            // Cantidad
            document.getElementById('cantidad_modal2').value = data['cantidad'] || '';
        
            // Observaciones
            document.getElementById('observaciones_modal2').value = data['observacion'] || '';
        }
        

        // Popular los campos del formulario (modal3 en este caso)
        if (modalId === 'modal3') {
            document.getElementById('denominacion_modal3').value = data['den'] || '';

            // Manejo de fecha y hora
            const fechaHora = data['fecha_elaboracion'] || '';
            if (fechaHora) {
                const fechaObj = new Date(fechaHora); // Convertir la fecha al objeto Date
                if (!isNaN(fechaObj)) {
                    // Formatear fecha y hora
                    const fecha = fechaObj.toISOString().split('T')[0]; // Formato YYYY-MM-DD
                    const hora = fechaObj.toTimeString().split(' ')[0]; // Formato HH:MM:SS
                    document.getElementById('fecha_modal3').value = fecha;
                    document.getElementById('hora_modal3').value = hora.slice(0, 5); // HH:MM
                }
            } else {
                document.getElementById('fecha_modal3').value = '';
                document.getElementById('hora_modal3').value = '';
            }

            // Manejo del lote
            const lote = data['lote'] || '';
            if (lote) {
                const [lote_a, lote_b, lote_c] = lote.split('-');
                document.getElementById('lote_a_modal3').value = lote_a || '';
                document.getElementById('lote_b_modal3').value = lote_b || '';
                document.getElementById('lote_c_modal3').value = lote_c || '';
            } else {
                document.getElementById('lote_a_modal3').value = '';
                document.getElementById('lote_b_modal3').value = '';
                document.getElementById('lote_c_modal3').value = '';
            }

            // Manejo de Brix
            document.getElementById('brix_modal3').value = data['brix'] || '';

            // Manejo del número de recipiente
            document.getElementById('numero_recipiente_modal3').value = data['numero_recipiente'] || '';

            // Manejo de observaciones
            document.getElementById('observaciones_modal3').value = data['observaciones'] || '';
            
            // Popular campos ocultos si existen en los datos
            document.getElementById('cod_cls_modal3').value = data['cod_cls'] || '';
            document.getElementById('cod_mae_modal3').value = data['producto'] || '';
            document.getElementById('id_modal3').value = data['id'] || '';
            document.getElementById('numero_unico_modal3').value = data['numero_unico'] || '';
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al comunicarse con el servidor.');
    }
});