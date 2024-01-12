let elements = document.getElementsByClassName("ranges")

for (let el of elements) {
    let name = el.attributes["name"]
    el.prop('checked', true)
}

