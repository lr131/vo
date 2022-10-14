async function login(event) {
    event.preventDefault()
    console.log(event.target.dataset.url)
    var url = event.target.dataset.url;
    const data = serializeForm(event.target)
    const response = await sendData(url, 'POST', data)
    console.log(response.ok)
    if ((response.status == 200) && (response.ok)) {
        window.location.replace("http://127.0.0.1:8000/");
    }
}

document.addEventListener("DOMContentLoaded", function(event) { 
    document.getElementById('loginForm').addEventListener('submit', login)
  });