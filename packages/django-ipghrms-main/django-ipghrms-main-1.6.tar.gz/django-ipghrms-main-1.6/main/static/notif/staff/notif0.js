setInterval(function(){
    $.get('/notification/staff/all/',function(data) {
        document.getElementById("staffNotifTot").innerHTML = data.value;
    });
    
}, 3000);

setInterval(function(){
    var span = document.getElementById("staffNotifTot");
    if (span.innerHTML > 0) {
        span.classList.toggle("blink");
    }
},900)