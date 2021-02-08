async function enviar(e) {
    Notiflix.Loading.Init({svgColor:"#6493c6",});
    let no_es_valido = false;
    await fetch("/login?psw=" + document.getElementById("psw").value + "&mail=" + document.getElementById("email").value, {
        method: 'POST'
    }).then(response => response.json()).then(function (data) {
        if (JSON.stringify(data) == "{}") {
            no_es_valido = true;
        }
    });

    if (no_es_valido == true) {
        Notiflix.Notify.Failure('Email o contraseña no validos');

        setTimeout(function() {
            return false;
        }, 5000);
    } else {
        Notiflix.Loading.Circle();
        setTimeout(function() {
            window.location.replace("/dashboard");
            return false;
        }, 3000);
    }
    return false;
}