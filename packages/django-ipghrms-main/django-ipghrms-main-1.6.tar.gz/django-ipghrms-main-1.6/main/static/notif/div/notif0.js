setInterval(function(){
    $.get('/notification/div/all/',function(data) {
        document.getElementById("divNotifTot").innerHTML = data.value;
    });
    
}, 3000);

setInterval(function(){
    var span = document.getElementById("divNotifTot");
    if (span.innerHTML > 0) {
        span.classList.toggle("blink");
    }
},900)