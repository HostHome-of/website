async function enviar(e) {
    Notiflix.Loading.Init({svgColor:"#6493c6",});
    e.preventDefault();
    let no_es_valido = false;
    await fetch("/register?nm="+ document.getElementById("name").value + "&psw=" + document.getElementById("password").value + "&mail=" + document.getElementById("email").value, {
        method: 'POST'
    }).then(response => response.json()).then(function (data) {
        if (JSON.stringify(data) == "{}") {
            no_es_valido = true;
        }
    });

    if (no_es_valido == true) {
        Notiflix.Notify.Failure('Ese email ya existe');
        setTimeout(function() {
            return false;
        }, 5000);
    } else {
        Notiflix.Loading.Circle();
        setTimeout(function() {
            window.location.replace("/account");
            return false;
        }, 3000);
    }
    return false;
}