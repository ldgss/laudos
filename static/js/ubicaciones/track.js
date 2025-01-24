document.addEventListener('DOMContentLoaded', () => {
    const anularButtons = document.querySelectorAll('.btn-anular');
    const modalFecha = document.getElementById('modalFecha');
    const modalSector = document.getElementById('modalSector');
    const modalPosicion = document.getElementById('modalPosicion');
    const modalProfundidad = document.getElementById('modalProfundidad');
    const modalAltura = document.getElementById('modalAltura');
    const modalResponsable = document.getElementById('modalResponsable');
    const modalId = document.getElementById('modalId');
    const modal_numero_unico = document.getElementById('modal_numero_unico');

    anularButtons.forEach(button => {
        button.addEventListener('click', () => {
            modalFecha.textContent = button.getAttribute('data-fecha');
            modalSector.textContent = button.getAttribute('data-sector');
            modalPosicion.textContent = button.getAttribute('data-posicion');
            modalProfundidad.textContent = button.getAttribute('data-profundidad');
            modalAltura.textContent = button.getAttribute('data-altura');
            modalResponsable.textContent = button.getAttribute('data-responsable');
            modalId.value = button.getAttribute('data-id');
            modal_numero_unico.value = button.getAttribute('data-numero-unico');
        });
    });
});
