function get_clients_list(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
          return;
      }

      const response = xhr.response;
      var resp = JSON.parse(response);
      console.log(resp);

      //Результаты поиска
      var results = document.getElementById('results');
      results.innerHTML ='';

      for (let i = 0; i < resp['count']; i += 1) {

        var tr = document.createElement('tr');
        tr.setAttribute('id', resp['results'][i]['id']);
        var st = '<td>' + resp['results'][i]['family'] + ' ';
        st += resp['results'][i]['name'] + ' ';
        st += resp['results'][i]['patr'] + ' ';
        st += '(' + resp['results'][i]['city'] + ') ' + resp['results'][i]['state_name'] +'</td>';
        st += '<td>' + resp['results'][i]['comment'] + '</td>';
        st += '<td>(' + resp['results'][i]['note'] + ')</td>';
        tr.setAttribute('data-family', resp['results'][i]['family']);
        tr.setAttribute('data-name', resp['results'][i]['name']);
        tr.setAttribute('data-patr', resp['results'][i]['patr']);
        tr.setAttribute('data-city', resp['results'][i]['city']);
        tr.setAttribute('data-statename', resp['results'][i]['state_name']);
        tr.innerHTML = st;

        tr.addEventListener('click', function(event) {
            var listNotSaveWarning = document.getElementById('listNotSave');
            listNotSaveWarning.style.display = '';
            console.log('display: ', listNotSaveWarning.style.display)
            var currentElement = event.target; // элемент который вызвал функцию
            var ell = currentElement.closest("tr"); // tr element (строчка c клиентом)
            console.log(ell)
            var cid = ell.getAttribute('id');
            var clientsInput = document.getElementById('id_clients');
            var cids =  clientsInput.value + ',' + cid;
            clientsInput.value = cids;

            var clientsTable = document.getElementById('clientsTable');
            var tr_new = document.createElement('tr');
            tr_new.setAttribute('data-client', cid);
            var family = ell.getAttribute('data-family');
            var name = ell.getAttribute('data-name');
            var patr = ell.getAttribute('data-patr');
            var state_name = ell.getAttribute('data-statename');
            var city = ell.getAttribute('data-city');
            var value_td = '<td>' + family + ' ' + name + ' ' + patr + ' (' + state_name +')</td><td>' + city +'</td><td></td><td></td><td></td>';
            tr_new.innerHTML = value_td;
            clientsTable.appendChild(tr_new);


            ell.style.display = "none"; //Скрываем элемент

          })


        results.append(tr)


      }

    }
    xhr.send();
  }