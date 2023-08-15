setInterval(function(){
    $.get('/notification/hr/badge/',function(data) {
        document.getElementById("hrNotifLeave").innerHTML = data.data3;
    });
}, 3000);