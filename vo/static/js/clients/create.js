async function create_client(event) {
    event.preventDefault()

    if (!document.getElementById('alertRes').classList.contains('hidden')) {
        document.getElementById('alertRes').classList.add('hidden')
    }
   
    var url = event.target.action;
    const data = serializeForm(event.target)
    const response = await sendData(url, 'POST', data)
    if (response.status == 201) {
        response.json().then(data => {
            console.log({data1: data['id']});
            var clientUrl = document.getElementById('urls').dataset.client;
            var url = clientUrl.replace('0', data['id'])
            window.location.href = url
        })
    }
    if (response.status = 400) {
        response.json().then(data => {
            console.log(data)
            if (typeof data['phone'] !== "undefined") {
                console.log("Клиент с таким телефоном уже существует!")
                document.getElementById('alertRes').textContent = "Клиент с таким телефоном уже существует!"
                document.getElementById('alertRes').classList.remove('hidden')
            } else if (typeof data['non_field_errors'] !== "undefined") {
                console.log("Клиент с такими ФИО и датой рождения уже существует!")
                document.getElementById('alertRes').textContent = "Клиент с такими ФИО и датой рождения уже существует!"
                document.getElementById('alertRes').classList.remove('hidden')
            }
        })
    }
  }

document.addEventListener("DOMContentLoaded", function(event) { 
    document.getElementById('client').addEventListener('submit', create_client)
})