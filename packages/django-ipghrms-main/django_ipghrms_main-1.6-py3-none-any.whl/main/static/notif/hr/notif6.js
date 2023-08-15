setInterval(function(){
    $.get('/notification/hr/badge/',function(data) {
        document.getElementById("hrNotifLeaveEnd").innerHTML = data.data5;
    });
}, 3000);