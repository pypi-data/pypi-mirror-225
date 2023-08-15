setInterval(function(){
    $.get('/notification/staff/badge/',function(data) {
        console.log(data.value1)
        document.getElementById("staffNotifLeave").innerHTML = data.data1;
    });
}, 3000);