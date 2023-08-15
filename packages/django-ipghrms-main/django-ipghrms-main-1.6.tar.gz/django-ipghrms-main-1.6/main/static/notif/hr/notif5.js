setInterval(function(){
    $.get('/notification/hr/badge/',function(data) {
        document.getElementById("hrNotifEval").innerHTML = data.data4;
    });
}, 3000);