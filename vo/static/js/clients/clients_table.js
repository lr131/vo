var pagination_listener = function (event) {
    event.preventDefault();
    url = event.target.href;
    var objURL = new URL(url)
    if (objURL.searchParams.has('page')) {
        document.getElementById('clientUrl').dataset.page = objURL.searchParams.get('page')
    }
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


  function print_numeric_pagination_buttons(startValuePage,
                                            pageCurrent,
                                            endValuePage,
                                            objURL,
                                            container) {
    console.log("startValuePage", startValuePage)
    console.log("pageCurrent", pageCurrent)
    console.log("endValuePage", endValuePage)
    console.log("objURL", objURL)
    for (let i = startValuePage; i <= endValuePage; i += 1) {
        objURL.searchParams.set('page', i)
        var li = document.createElement('li');
        li.classList.add("page-item")
        
        if (i == pageCurrent) {
            li.classList.add("active")
            var span = document.createElement('span');
            span.classList.add("page-link")
            span.textContent = i

            var span2 = document.createElement('span');
            span2.classList.add("sr-only")
            span2.textContent = "(current)"

            span.append(span2)
            li.append(span)
        } else {
            var a = document.createElement('a');
            a.classList.add("page-link")
            a.setAttribute("href",  objURL.href)
            a.textContent = i
            a.addEventListener('click', pagination_listener)
            li.append(a)
        }
        container.append(li)  
      }

  }

  function create_pagination_button(pageCount, 
                                    pageCurrent, 
                                    url) {
    console.log("pageCount", pageCount)
    var container = document.getElementById('nav_buttons');
    container.innerHTML = ''

    if (pageCount < 2) {
        return 
    }


    var objURL = new URL(url, document.location.protocol + "//" + document.location.host)

    var previousBtn = document.createElement('li');
    previousBtn.setAttribute("id", "previousBtn")
    previousBtn.classList.add("page-item")

    var previousLink = document.createElement("a")

    previousLink.classList.add("page-link")
    previousLink.setAttribute("tabindex", "-1")
    previousLink.removeEventListener('click', pagination_listener);
    previousLink.textContent = "Назад"

    previousBtn.append(previousLink)

    var printPageCount = pageCount
      

    if (pageCurrent > 1) {
    
        objURL.searchParams.set('page', parseInt(pageCurrent) - 1)

        previousBtn.classList.remove('disabled');
        previousLink.setAttribute('href', objURL.href);

        previousLink.addEventListener('click', pagination_listener)

    } else {
        previousBtn.classList.add('disabled');
    }

    var spanDotsStart = document.createElement('span');
    var spanDotsEnd = document.createElement('span');
    spanDotsStart.textContent = '...';
    spanDotsEnd.textContent = '...';
    container.append(previousBtn)

    if (pageCount > 15) {
      console.log(((pageCurrent >= 4) && ((pageCount - pageCurrent) > 5)))
      if (pageCurrent < 4) {
        print_numeric_pagination_buttons(1, pageCurrent, 5, objURL, container);
        container.append(spanDotsEnd)
      } else if ((pageCurrent >= 4) && ((pageCount - pageCurrent) > 5)) {
        console.log("Печатаем с точками")
        // печатаем с точками
        container.append(spanDotsStart)
        print_numeric_pagination_buttons(Number(pageCurrent) - 2, pageCurrent, Number(pageCurrent) + 2, objURL, container);
        container.append(spanDotsEnd)
      } else {
        // печатаем точки и последние 5 кнопок
        container.append(spanDotsStart)
        print_numeric_pagination_buttons(pageCount - 5, pageCurrent, pageCount, objURL, container);
      }
    } else {
      print_numeric_pagination_buttons(1, pageCurrent, pageCount, objURL, container);
    }
    

    var nextBtn = document.createElement('li');
    nextBtn.setAttribute("id", "nextBtn")
    nextBtn.classList.add("page-item")

    var nextLink = document.createElement("a")

    nextLink.classList.add("page-link")
    nextLink.setAttribute("tabindex", "-1")
    nextLink.removeEventListener('click', pagination_listener);
    nextLink.textContent = "Далее"

    nextBtn.append(nextLink)
      
    if (pageCurrent < pageCount) {
    
        objURL.searchParams.set('page', parseInt(pageCurrent) + 1)

        nextBtn.classList.remove('disabled');
        nextLink.setAttribute('href', objURL.href);
        nextLink.addEventListener('click', pagination_listener)

    } else {
        nextBtn.classList.add('disabled');
    }

    container.append(nextBtn)

  }

  function get_clients_list(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
          return;
      }
      const response = xhr.response;
      var resp = JSON.parse(response);
      var clientsTable = document.getElementById('clientsTable');
      clientsTable.innerHTML ='';
      var clientUrl = document.getElementById('clientUrl').dataset.url;
      
      let countInPage = resp['results'].length
      let pageCount = 1

      if (resp['next']) {
        pageCount = Math.ceil(resp['count']/countInPage)
      } else {
        pageCount = Math.ceil(resp['count']/20)
      }

      create_pagination_button(pageCount, 
        document.getElementById('clientUrl').dataset.page, 
        document.getElementById('clientUrl').dataset.extra)

      for (let i = 0; i < countInPage; i += 1) {
        let tr = document.createElement('tr');
        tr.setAttribute('id', resp['results'][i]['id']);
        stateClient = resp['results'][i]['state_id'];
        state = resp['results'][i]['state_name'] ? resp['results'][i]['state_name'] : '';
        var url = clientUrl.replace('1', resp['results'][i]['id']) + '?back_page=' + document.getElementById('clientUrl').dataset.page
        tr.setAttribute('data-url', url);
        tr.addEventListener('click', function(event) {
          var link = event.currentTarget.dataset.url;
          location.href = link;
        })

        if (stateClient == 1) {
          tr.classList.add('table-success');
          
        }
        if (stateClient == 2) {
          tr.classList.add('table-warning');
        }

        if (stateClient == 3) {
          tr.classList.add('table-secondary');
        }

        if (stateClient == 4) {
          tr.classList.add('table-primary');
        }

        if (stateClient == 5) {
          tr.classList.add('table-danger');
        }

        if (stateClient == 6) {
          tr.classList.add('bg-danger');
        }

        let family = resp['results'][i]['family'];
        let name = resp['results'][i]['name'];
        let patr = resp['results'][i]['patr'];
        let birthday = resp['results'][i]['birthday'];
        let city = resp['results'][i]['city'];
        let phone = resp['results'][i]['phone'] ? resp['results'][i]['phone'] : '';
        let comment = resp['results'][i]['comment'];
        let note = resp['results'][i]['note'];     
        let course_candidate = resp['results'][i]['course_candidate'];      
        
        
        family = family ? family : '';
        name = name ? name : '';
        patr = patr ? patr : '';
        course_candidate = course_candidate ? course_candidate : '';

        if (birthday) {
          var birthdayList = birthday.slice(0,10).split('-');
          birthday = ([birthdayList[2], birthdayList[1], birthdayList[0]]).join('.');
        } else {
          birthday = '';
        }
        

        isGroupViber = resp['results'][i]['viber_group'] ? '<span class="badge badge-pill badge-danger">Viber</span><br />' : '';
        isGroupWa = resp['results'][i]['wa_group'] ? '<span class="badge badge-pill badge-success">WhatsApp</span> <br />' : '';
        isGroupTg = resp['results'][i]['tg_group'] ? '<span class="badge badge-pill badge-primary">Telegram</span>' : '';

        gropus = isGroupViber + isGroupWa + isGroupTg;


        isViber = resp['results'][i]['viber']  ? '<span class="badge badge-pill badge-danger">Viber</span><br />' : '';
        isWa = resp['results'][i]['wa'] ? '<span class="badge badge-pill badge-success">WhatsApp</span> <br />' : '';
        isTg = resp['results'][i]['tg'] ? '<span class="badge badge-pill badge-primary">Telegram</span><br />' : '';
        isSms = resp['results'][i]['sms'] ? '<span class="badge badge-pill badge-info">Смс</span><br />' : '';
        isCall = resp['results'][i]['call'] ? '<span class="badge badge-pill badge-secondary">Звонки</span>' : '';


        contact = isViber + isWa + isTg + isSms + isCall;

        mailing = resp['results'][i]['mailing'] ? resp['results'][i]['mailing'] : '';

        tr.append(create_client_td(state));
        tr.append(create_client_td([family, name, patr].join(' ')));
        tr.append(create_client_td(birthday));
        tr.append(create_client_td(city));
        tr.append(create_client_td(phone.replace(';',' <br />')));
        tr.append(create_client_td(comment));
        tr.append(create_client_td(note));

        tr.append(create_client_td(gropus));

        tr.append(create_client_td(contact));

        tr.append(create_client_td(mailing));
        tr.append(create_client_td(course_candidate));

        clientsTable.append(tr);
      }
    }
    xhr.send();
  }

  function filter_data(event) {
    event.preventDefault();
    document.getElementById('clientUrl').dataset.extra = event.target.href
    document.getElementById('clientUrl').dataset.page = 1
    get_clients_list(event.target.href);
  }

  document.addEventListener("DOMContentLoaded", function(event) { 
    var url_get_extra = document.getElementById("clientUrl").dataset.extra
    get_clients_list(url_get_extra);
    console.log(document.getElementById('filters').children);
    for (let element of document.getElementById('filters').children) {
      element.addEventListener('click', filter_data)
    }
    document.getElementById('search').addEventListener('click', searchInput)
    document.getElementById('searchForm').addEventListener('submit', searchClient)
  });