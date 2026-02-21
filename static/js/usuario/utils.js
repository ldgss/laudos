document.addEventListener("DOMContentLoaded", function(){
    const guardar = document.getElementById("guardar");
    guardar.addEventListener("click", function(){
        let device = document.getElementById("device").value;
        if(device.length <= 12){
            document.cookie = `device_id=${device}; max-age=31536000; path=/`;
        }else{
            alert('Utilice 12 caracteres o menos para identificar el dispositivo')
        }
    })
})