document.addEventListener("DOMContentLoaded", function(event) { 
    var form = document.getElementById('actionForm');

    var plc = form.dataset.plc;
    var lid = form.dataset.lid;


    if (!isNaN(parseInt(plc))) {
        console.log("plc")
        document.getElementById('id_plc').value = parseInt(plc)
    }

    if (!isNaN(parseInt(lid))) {
        console.log("lid")
        document.getElementById('id_lid').value = parseInt(lid)
    }


  });