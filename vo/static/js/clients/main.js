function get_bday_plug(event) {
  event.preventDefault();
  document.getElementById('birthday').value = '01.01.1900';
}

document.addEventListener("DOMContentLoaded", function(event) { 
    var urls = document.getElementById('urls');
    document.getElementById('birthdayPlug').addEventListener('click', get_bday_plug)


  });

  $(document).ready(function() {
    /*добавляем маску к input с ID = phone*/
    // $("[name=phone]").mask("+7 (999) 999-99-99");
    $("[name=phone]").mask("79999999999");
    $("[name=bday]").mask("99.99.9999");
  })
