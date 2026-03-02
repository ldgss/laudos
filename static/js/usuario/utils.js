function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

document.addEventListener("DOMContentLoaded", function () {
    let device = document.getElementById("device");
    
    const savedDevice = getCookie("device_id");
    if (savedDevice) {
        device.value = savedDevice;
    }

    const guardar = document.getElementById("guardar");
    guardar.addEventListener("click", function () {
        if (device.value.length <= 12) {
            document.cookie = `device_id=${device.value}; max-age=31536000; path=/`;
            alert("Dispositivo identificado correctamente");
        } else {
            alert('Utilice 12 caracteres o menos para identificar el dispositivo');
        }
    });
});