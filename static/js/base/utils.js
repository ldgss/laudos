// codigo para activar el loader
// $(document).ready(function() {
//     $('a').on('click', function(event) {
//         //
//         const href = $(this).attr('href');
//         if (!href || href === '#' || $(this).hasClass('dropdown-toggle')) {
//             event.preventDefault(); 
//             return;
//         }
//         setTimeout(function() {
//             $('#loading').show(); 
//         }, 200); 
//     });
//     $(window).on('load', function() {
//         $('#loading').hide(); 
//     });
// });

// chequear la conexion cada 5 segundos

let isDisconnected = false;
let toastEl = document.getElementById("connection-toast");
let toastBody = document.getElementById("toast-message");
let toast = new bootstrap.Toast(toastEl, { autohide: false });

function checkConnection() {
    fetch("/ping", { method: "GET", cache: "no-store" })
        .then(response => {
            if (response.ok) {
                if (isDisconnected) {
                    updateToast("Conectado nuevamente", "bg-success");
                    isDisconnected = false;
                }
            } else {
                showDisconnectionToast();
            }
        })
        .catch(() => {
            showDisconnectionToast();
        });
}

function showDisconnectionToast() {
    if (!isDisconnected) {
        updateToast("Sin conexión al servidor.", "bg-danger");
        isDisconnected = true;
    }
}

function updateToast(message, className) {
    toastBody.textContent = message;
    toastEl.className = `toast align-items-center text-white border-0 ${className}`;
    toast.show();
}

setInterval(checkConnection, 10000);