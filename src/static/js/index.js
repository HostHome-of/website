const nombre = document.getElementById("nombre");
const mail = document.getElementById("email");
const psw = document.getElementById("psw");

function crear() {
    data = fetch("/register?nm=" + nombre.value + "&psw=" + psw.value + "&mail=" + mail.value, {
        method: 'POST'
    })
    .then(response => response.json())
    .catch (function() {
        alert("Ese email ya existe")
        window.location.replace("/")
        return false;
    });

    window.location.replace("/account")
    return false;
}