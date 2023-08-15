setInterval(function(){
    $.get('/notification/pr/badge/',function(data) {
        console.log(data.value1)
        document.getElementById("prNotifLeave").innerHTML = data.data1;
    });
}, 3000);