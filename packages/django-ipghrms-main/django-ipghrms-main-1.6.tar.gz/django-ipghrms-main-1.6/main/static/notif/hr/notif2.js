setInterval(function(){
    $.get('/notification/hr/badge/',function(data) {
        document.getElementById("hrNotifBirth").innerHTML = data.data1;
    });
}, 3000);