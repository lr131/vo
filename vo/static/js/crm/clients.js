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
        st += '(' + resp['results'][i]['city'] + ')</td>';
        st += '<td>' + resp['results'][i]['comment'] + '</td>';
        st += '<td>(' + resp['results'][i]['note'] + ')</td>';
        tr.innerHTML = st;

        tr.addEventListener('click', function(event) {
            console.log(event.currentTarget.getAttribute('id'))
          })


        results.append(tr)


      }

    }
    xhr.send();
  }