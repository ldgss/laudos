


function updateDateTimeField() {
    const field = document.getElementById('fecha');
    const now = new Date();

    // Ajusta la fecha y hora al huso horario UTC-3
    now.setHours(now.getUTCHours() - 6);

    // Formatea la fecha y hora ajustada en formato YYYY-MM-DDTHH:mm
    const formattedDateTime = now.toISOString().slice(0, 16);

    // Actualiza el campo
    if (field) {
        field.value = formattedDateTime;
    } else {
        console.warn("El campo con ID 'fecha' no fue encontrado.");
    }
}


try {
    window.addEventListener('load', updateDateTimeField);
    setInterval(updateDateTimeField, 1000);
} catch (error) {
    console.log(error)
}


