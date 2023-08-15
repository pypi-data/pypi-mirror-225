setInterval(function(){
    $.get('/notification/hr/badge/',function(data) {
        document.getElementById("hrNotifCont").innerHTML = data.data2;
    });
}, 3000);