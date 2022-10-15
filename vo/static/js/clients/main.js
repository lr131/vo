async function get_states(url) {
    var statesElem= document.getElementById('states');
    var state = document.getElementById('state');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
          return;
      }
      const response = xhr.response;
      var resp = JSON.parse(response);
      for (let i = 0; i < resp['results']['length']; i += 1) {
        var option = document.createElement('option');
        option.setAttribute('value', resp['results'][i]['id']);
        option.textContent = resp['results'][i]['name'];
        state.append(option);

        stateId = resp['results'][i]['id'];
        statesElem.setAttribute('data-state' + stateId, resp['results'][i]['name']);
      }
    }
    xhr.send();
  }

  document.addEventListener("DOMContentLoaded", function(event) { 
    var urls = document.getElementById('urls');

    get_states(urls.dataset.states);

  });

  $(document).ready(function() {
    /*добавляем маску к input с ID = phone*/
    // $("[name=phone]").mask("+7 (999) 999-99-99");
    $("[name=phone]").mask("79999999999");
    $("[name=bday]").mask("99.99.9999");
  })
