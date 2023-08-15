setInterval(function(){
    $.get('/notification/pr/all/',function(data) {
        document.getElementById("prNotifTot").innerHTML = data.value;
    });
    
}, 3000);

setInterval(function(){
    var span = document.getElementById("prNotifTot");
    if (span.innerHTML > 0) {
        span.classList.toggle("blink");
    }
},900)