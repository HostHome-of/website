const nombre = document.getElementById("nombre");
const mail = document.getElementById("email");
const psw = document.getElementById("psw");

async function crear(event) {
    console.log("crear");
    event.preventDefault();
    await fetch("/register?nm=" + nombre.value + "&psw=" + psw.value + "&mail=" + mail.value, {
        method: 'POST'
    }).then(response => response.json()).then(function(data) {
        console.log(data)
        if (JSON.stringify(data) == "{}") {
            if (window.confirm("Ese email ya existe, quieres entrar a ru cuenta?")) {
                window.location.href = "/login";
                return false;
            }
            window.location.replace("/");
            return false;
        } else {
            window.location.replace("/account");
            return false;
        }
    });
}