setInterval(function(){
    $.get('/notification/dep/all/',function(data) {
        document.getElementById("depNotifTot").innerHTML = data.value;
    });
    
}, 3000);

setInterval(function(){
    var span = document.getElementById("depNotifTot");
    if (span.innerHTML > 0) {
        span.classList.toggle("blink");
    }
},900)