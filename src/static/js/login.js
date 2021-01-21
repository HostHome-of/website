async function enviar(e) {
    e.preventDefault();
    let no_es_valido = false;
    await fetch("/login?psw=" + document.getElementById("password").value + "&mail=" + document.getElementById("email").value, {
        method: 'POST'
    }).then(response => response.json()).then(function (data) {
        if (JSON.stringify(data) == "{}") {
            no_es_valido = true;
        }
    });

    if (no_es_valido == true) {
        Notiflix.Report.Failure('Un error',
                                'Es posible que una de estas dos cosas esten mal <br /><ul><li> Email</li><li> Contraseña</li></ul>',
                                'Aceptar');
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