setInterval(function(){
    $.get('/notification/vice/badge/',function(data) {
        console.log(data.value1)
        document.getElementById("viceNotifLeave").innerHTML = data.data1;
    });
}, 3000);