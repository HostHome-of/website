async function enviar() {
    Notiflix.Loading.Init({svgColor:"#6493c6",});
    // e.preventDefault();

    let no_es_valido = false;
    let no_es_valido_psw = false;


    if (document.getElementById("psw").value.length < 6) {
        Notiflix.Notify.Failure('La contraseña debe de ser mas de 6 caracteres.');
        no_es_valido_psw = true;
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    }
    await fetch("/register?nm="+ document.getElementById("nombre").value + "&psw=" + document.getElementById("psw").value + "&mail=" + document.getElementById("email").value, {
        method: 'POST'
    }).then(response => response.json()).then(function (data) {
        if (JSON.stringify(data) == "{}") {
            no_es_valido = true;
        } else {
            Notiflix.Loading.Circle();
        }
    });

    if (no_es_valido == true && no_es_valido_psw == false) {
        Notiflix.Notify.Failure('Ese email ya existe');
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    } else {
        if (no_es_valido_psw == false) {
            setTimeout(function() {
                window.location.replace("/register/activation");
                return false;
            }, 3000);
        }
    }
}