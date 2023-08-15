setInterval(function(){
    $.get('/notification/hr/all/',function(data) {
        document.getElementById("hrNotifTot").innerHTML = data.value;
    });
    
}, 3000);

setInterval(function(){
    var span = document.getElementById("hrNotifTot");
    if (span.innerHTML > 0) {
        span.classList.toggle("blink");
    }
},900)