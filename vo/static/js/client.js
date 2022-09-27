var pagination_listener = function (event) {
    event.preventDefault();
    url = event.target.href;
    get_clients_list(url);
  }; 

  function create_client_td(value) {
    var td = document.createElement('td');
    if (String(value) != "null") {
      td.innerHTML = value;
    }
    return td;
  };

  function create_client_bool_td(value) {
    var td = document.createElement('td');
    if (value) {
      td.textContent = '+';
    }
    return td;
  };

  function get_events(url) {
    var events = document.getElementById('events');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
          return;
      }
      const response = xhr.response;
      var resp = JSON.parse(response);
      var event = document.getElementById('event');
      for (let i = 0; i < resp['results']['length']; i += 1) {
        events.setAttribute('data-event' + resp['results'][i]['id'], resp['results'][i]['name']);
        
        var option = document.createElement('option');
        option.value = resp['results'][i]['id'];
        option.textContent = resp['results'][i]['name'];
        event.append(option);
      }
    }
    xhr.send();
  }

  function get_bday_plug(event) {
    event.preventDefault();
    document.getElementById('birthday').value = '01.01.1900';
  }

  function get_states(url) {
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

  function get_client_data(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
          return;
      }
      const response = xhr.response;
      var resp = JSON.parse(response);
      document.getElementById('family').value = resp['family'];
      document.getElementById('name').value = resp['name'];
      document.getElementById('patr').value = resp['patr'] ? resp['patr'] : '';
      var bday = resp['birthday'] ? resp['birthday'].slice(0,10) : '';
      if (bday.length) {
        let tmp = bday.split('-');
        bday = ([tmp[2], tmp[1], tmp[0]]).join('.');
      }
      document.getElementById('birthday').value = bday;

      setSelectValue('state', resp['state']);

      document.getElementById('city').value = resp['city'] ? resp['city'] : '';
      document.getElementById('phone').value = resp['phone'] ? resp['phone'] : '';
      document.getElementById('note').value = resp['note'] ? resp['note'] : '';
      document.getElementById('comment').value = resp['comment'] ? resp['comment'] : '';

      var in_black_list = resp['in_black_list'];
      if (in_black_list) {
        document.getElementById("in_black_list").checked = true;
      }
    }

    xhr.send();
  }


  function get_client_mailing(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
          return;
      }
      const response = xhr.response;
      var resp = JSON.parse(response);
     
      for (key in resp) {
        if ((key != 'comment') && (key != 'client') && (key != 'id')) {
            if (resp[key]) {
                document.getElementById(key).checked = true;
              }
        }
      }
      var comment = resp['comment'] ? resp['comment'] : "";
      document.getElementById('commentMailing').value = comment;
      
    }

    xhr.send();
  }

  function get_client_products(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
          return;
      }
      const response = xhr.response;
      var resp = JSON.parse(response);
     
      for (key in resp) {
        if ((key != 'tg') && (key != 'client') && (key != 'id') && (key != 'course_candidate')) {
            if (resp[key]) {
                document.getElementById(key).checked = true;
              }
        }
        if (key == 'tg') {
            document.getElementById('ter_gr').checked = true;
        }
      }
      var course_candidate = resp['course_candidate'] ? resp['course_candidate'] : "";
      document.getElementById('course_candidate').value = course_candidate; 
    }

    xhr.send();
  }

  function get_client_interest(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
          return;
      }
      const response = xhr.response;
      var resp = JSON.parse(response);
      console.log(resp);
      var eventTable = document.getElementById('eventTable');
      var events = document.getElementById('events');

      for (let i = 0; i < resp['results'].length; i+= 1) {
        var tr = document.createElement('tr');
        var tdEvent = document.createElement('td');
        var tdComment = document.createElement('td');
        var td = document.createElement('td');
        
        tdEvent.classList.add('col-sm-6');
        var p = document.createElement('p');

        var event_id = resp['results'][i]['event'] ? resp['results'][i]['event'] : null;
        var eventContent = '';
        if (event_id) {
            console.log(event_id);
            eventContent = events.getAttribute('data-event' + event_id);
            console.log(eventContent);
        }
        
        p.textContent = eventContent;
        tdEvent.append(p);

        
        tdComment.classList.add('col-sm-6');
        var textarea = document.createElement('textarea');
        textarea.classList.add('form-control');
        textarea.setAttribute('rows', '2')
        textarea.value = resp['results'][i]['comment'] ? resp['results'][i]['comment'] : '';
        tdComment.append(textarea);
        
        tr.append(tdEvent);
        tr.append(tdComment);
        
        tr.append(td);
        eventTable.append(tr)
      };
      
    };
    xhr.send();
  }

  function setSelectValue (id, val) {
    document.getElementById(id).value = val;
  }

  document.addEventListener("DOMContentLoaded", function(event) { 
    var urls = document.getElementById('urls');

    get_states(urls.dataset.states);
    get_events(urls.dataset.events);
    get_client_data(urls.dataset.main);
    get_client_mailing(urls.dataset.mailing)
    get_client_products(urls.dataset.products)
    get_client_interest(urls.dataset.interest)
    document.getElementById('birthdayPlug').addEventListener('click', get_bday_plug)
  });