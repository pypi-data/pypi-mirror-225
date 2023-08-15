setInterval(function(){
    $.get('/notification/dep/badge/',function(data) {
        console.log(data.value1)
        document.getElementById("depNotifLeave").innerHTML = data.data1;
    });
}, 3000);