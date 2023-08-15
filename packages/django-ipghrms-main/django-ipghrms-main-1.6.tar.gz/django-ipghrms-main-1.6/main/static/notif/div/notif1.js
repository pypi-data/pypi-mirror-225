setInterval(function(){
    $.get('/notification/div/badge/',function(data) {
        console.log(data.value1)
        document.getElementById("divNotifLeave").innerHTML = data.data1;
    });
}, 3000);