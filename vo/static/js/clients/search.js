function searchInput(event) {
    event.preventDefault()
    console.log(event.target)
}

function searchClient(event) {
    event.preventDefault()
    console.log(event.target.action)
    var url = new URL(event.target.action)
    //если не цифры, то сделать капиталайз
    var value = document.getElementById('search').value
    if (!(/^\d+$/.test(value))) {
      console.log("Не Цифры!")
      value = capitalize(value)
    }
    url.searchParams.set('search', value)

    console.log(url.href)
    document.getElementById('clientUrl').dataset.extra = url.href
    document.getElementById('clientUrl').dataset.page = 1;
    get_clients_list(url.href);
  }