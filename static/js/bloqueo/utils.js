function mostrarModal(id, nombre, estado, planilla, motivo, observaciones) {
    document.getElementById('modalId').value = id;
    document.getElementById('modalNombre').value = nombre;
    document.getElementById('modalEstado').checked = estado;
    document.getElementById('modalPlanilla').value = planilla;
    document.getElementById('modalMotivo').value = motivo;
    document.getElementById('modalObservaciones').value = observaciones;
    
    let modal = new bootstrap.Modal(document.getElementById('modalCambiar'));
    modal.show();
}