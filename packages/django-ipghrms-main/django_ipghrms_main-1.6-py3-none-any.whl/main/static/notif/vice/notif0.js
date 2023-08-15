setInterval(function(){
    $.get('/notification/vice/all/',function(data) {
        document.getElementById("viceNotifTot").innerHTML = data.value;
    });
    
}, 3000);

setInterval(function(){
    var span = document.getElementById("viceNotifTot");
    if (span.innerHTML > 0) {
        span.classList.toggle("blink");
    }
},2000)