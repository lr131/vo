function searchInput(event) {
    event.preventDefault()
    console.log(event.target)
}

function searchClient(event) {
    event.preventDefault()
    console.log(event.target.action)
    var url = new URL(event.target.action)
    
    console.log(event.target.id)
    let parent = document.querySelector("#" + event.target.id);
    var value = parent.querySelector('[name="search"]').value
    
    url.searchParams.set('search', value)

    get_list(url.href, 'searchClientResults', 'search-result', 'id_client_id');
    console.log("searchClientResults")
}

function searchEvent(event) {

    event.preventDefault();

    console.log(event.target.action);

    var url = new URL(event.target.action);
    var searchResults = event.target.dataset.result
    var targetId = event.target.dataset.target
    
    console.log(event.target.id)
    let parent = document.querySelector("#" + event.target.id);
    var value = parent.querySelector('[name="search"]').value

    if (targetId.includes("client")) {
        
        //если не цифры, то сделать капиталайз

        if (!(/^\d+$/.test(value))) {
            value = capitalize(value)
          }
    }

    url.searchParams.set('search', value);

    get_list(url.href, searchResults, 'search-result', targetId);

}

function fun1(event) {
    event.preventDefault();
    targetId = event.target.dataset.target
    console.log(event.target.dataset.target)
    document.getElementById(targetId).value = event.target.getAttribute("id");

}

function formatDate(date) {

    var dd = date.getDate();
    if (dd < 10) dd = '0' + dd;
  
    var mm = date.getMonth() + 1;
    if (mm < 10) mm = '0' + mm;
  
    var yy = date.getFullYear() % 100;
    if (yy < 10) yy = '0' + yy;
  
    return dd + '.' + mm + '.' + yy;
  }

function create_client_row(p, obj) {

    p.textContent += obj['family'];
    p.textContent += " " + obj['name'];
    p.textContent += " " + obj['city'];
    p.textContent += " " + obj['phone'];
    p.textContent += " " + obj['state_name'];
}

function create_event_row(p, obj) {

    p.textContent += obj['event_name'];
    var start = new Date(obj['start_date'])
    var end = new Date(obj['end_date'])

    p.textContent += " " + start.getDate()
    if (start.getMonth() != end.getMonth()) {
        p.textContent += "." + start.getMonth();
    }
  
    p.textContent +=  "-" + formatDate(end);
}


function get_list(url, resultId, className, targetName){
    console.log("get_list", url)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4 || xhr.status !== 200) {
        return;
      }
      const response = xhr.response;
      var resp = JSON.parse(response);
      console.log(resp)
      var searchResults = document.getElementById(resultId);
      searchResults.innerHTML ='';
               
      for (let i = 0; i < resp['count']; i += 1) {
        var p = document.createElement('p');
        p.setAttribute('id', resp['results'][i]['id']);
        p.setAttribute('class', className);
        p.setAttribute('data-target', targetName);
        console.log(targetName.includes("client"))
        if (targetName.includes("client")) {
            create_client_row(p, resp['results'][i]);
        } else {
            create_event_row(p, resp['results'][i]);
        }

        p.addEventListener('click', fun1)
        searchResults.append(p);
      }

    }
    xhr.send();        
};

document.addEventListener("DOMContentLoaded", function(event) { 
    var elements = document.getElementsByName('search');

    for (let i = 0; i < elements.length; i++) { 
        elements[i].addEventListener('click', searchInput);
    }
    
    document.getElementById('searchForm').addEventListener('submit', searchEvent);
    document.getElementById('searchEvent').addEventListener('submit', searchEvent);
    
});