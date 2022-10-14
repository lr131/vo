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
      setSelectValue('group', resp['group']);

      document.getElementById('city').value = resp['city'] ? resp['city'] : '';
      document.getElementById('note').value = resp['note'] ? resp['note'] : '';
      document.getElementById('comment').value = resp['comment'] ? resp['comment'] : '';

      var phones =  resp['phone'] ? resp['phone'].split(';') : []     
      console.log("phones", phones)
      if (phones.length > 1) {
        document.getElementById('phones').innerHTML = ''
        phones.forEach(phone => {
          var container = document.getElementById('phones')

          var div = document.createElement('div')
          div.classList.add('input-group')
          div.classList.add('mb-3')

          var inputPhone = document.createElement('input')
          var span = document.createElement('span')
          var icon = document.createElement('span')

          var basicID = "id" + phone

          icon.classList.add("material-icons")
          icon.classList.add("phone-remove-icon")
          icon.innerHTML='clear'

          span.classList.add("input-group-text")
          span.setAttribute("id", basicID)

          span.append(icon)

          inputPhone.setAttribute('type', 'text')
          inputPhone.setAttribute('name', 'phone')
          inputPhone.classList.add('form-control')
          inputPhone.setAttribute('placeholder', '79027775533')
          inputPhone.setAttribute('aria-label', 'phone')
          inputPhone.setAttribute('aria-describedby', basicID)

          inputPhone.value = phone
          div.append(inputPhone)
          div.append(span)
          
          container.append(div)
        })

      } else {
        document.getElementById('phone').value = resp['phone'] ? resp['phone'] : '';
      }
      // document.getElementById('phones').value = resp['phone'] ? resp['phone'] : '';
      


      var in_black_list = resp['in_black_list'];
      if (in_black_list) {
        document.getElementById("in_black_list").checked = true;
      }
    }

    xhr.send();
  }

  async function update_client_mailing(event) {
    event.preventDefault()
    mailingID = document.getElementById('commentMailing').dataset.id
    var url = document.getElementById('urls').dataset.mailing + mailingID + '/';

    const data = serializeForm(event.target)
    const response = await sendData(url, 'PATCH', data)
  }

  async function update_client_history(event) {
    event.preventDefault()
    historyID = document.getElementById('course_candidate').dataset.id
    var url = document.getElementById('urls').dataset.products + historyID + '/';

    const data = serializeForm(event.target)
    const response = await sendData(url, 'PATCH', data)
    
  }

  async function create_client_interest(event) {
    event.preventDefault()
    var url = document.getElementById('urls').dataset.interest;
    const data = serializeForm(event.target)
    const response = await sendData(url, 'POST', data)
    var form = document.getElementById('trForm').outerHTML
    var eventTable = document.getElementById('eventTable');
    eventTable.innerHTML = form
    get_client_interest(urls.dataset.interests)
  }

  //TODO по идее удалять по id
  async function delete_client_interest(event) {
    event.preventDefault()
    var url = document.getElementById('urls').dataset.interests
    //TODO своя сериализация
    const data = serializeForm(event.target)
    const response = await sendData(url, 'DELETE', data)

  }

  async function update_client(event) {
    event.preventDefault()
    var url = document.getElementById('urls').dataset.main;
    const data = serializeForm(event.target)
    const response = await sendData(url, 'PATCH', data)
    console.log(response)
  }

  function get_client_connect(url) {
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
      document.getElementById('commentMailing').setAttribute('data-id', resp['id'])
      document.getElementById('mailing-id').value = resp['id']
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
      document.getElementById('course_candidate').setAttribute('data-id', resp['id'])
      document.getElementById('history-id').value = resp['id']
    }

    xhr.send();
  }

  function save_updates(event) {
    document.getElementById('mailingBtn').click()
    document.getElementById('historyBtn').click()
    document.getElementById('clientBtn').click()
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
      var eventTable = document.getElementById('eventTable');
      var events = document.getElementById('events');

      for (let i = 0; i < resp['results'].length; i+= 1) {
        var tr = document.createElement('tr');
        tr.setAttribute('name', 'eventTable');
        var tdEvent = document.createElement('td');
        var tdComment = document.createElement('td');
        var td = document.createElement('td');
        
        tdEvent.classList.add('col-sm-6');
        var p = document.createElement('p');

        var event_id = resp['results'][i]['event'] ? resp['results'][i]['event'] : null;
        var eventContent = '';
        if (event_id) {
            eventContent = events.getAttribute('data-event' + event_id);
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
    get_client_connect(urls.dataset.connect)
    get_client_products(urls.dataset.history)
    get_client_interest(urls.dataset.interests)
    document.getElementById('birthdayPlug').addEventListener('click', get_bday_plug)
    document.getElementById('mailing').addEventListener('submit', update_client_mailing)
    document.getElementById('history').addEventListener('submit', update_client_history)
    document.getElementById('interestCreateForm').addEventListener('submit', create_client_interest)
    document.getElementById('client').addEventListener('submit', update_client)
    document.getElementById('save').addEventListener('click', save_updates)

  });

  $(document).ready(function() {
    /*добавляем маску к input с ID = phone*/
    // $("[name=phone]").mask("+7 (999) 999-99-99");
    $("[name=phone]").mask("79999999999");
    $("[name=bday]").mask("99.99.9999");
})