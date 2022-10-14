function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
   }
   

function serializeForm(formNode) {
    const { elements } = formNode

    const data = {}

    if (formNode.id === 'client') {
        var phones =[]
        Array.from(elements)
        .filter((item) => !!item.name)
        .forEach((element) => {
          const { name, type } = element
          const value = type === 'checkbox' ? element.checked : element.value
          if (name === 'bday') {
            var bday = value.split('.')
            data['birthday'] = bday.reverse().join('-')
          } else if (name === 'phone') {
            phones.push(value)
          } else {
            data[name] = value
          }
          
        })
        console.log(phones)
        data['phone'] = phones.join(';')
    } else {
        Array.from(elements)
        .filter((item) => !!item.name)
        .forEach((element) => {
          const { name, type } = element
          const value = type === 'checkbox' ? element.checked : element.value
  
          data[name] = value
        })
    }

    console.log(data)
    return JSON.stringify(data)
  }

async function sendData(url, method, data) {
    const csrftoken = getCookie('csrftoken'); 
    return await fetch(url, {
      method: method,
      headers: { 
        'Content-Type': 'application/json', 
        'X-CSRFToken': csrftoken
    },
      withCredentials: true,
      body: data,
    })
}