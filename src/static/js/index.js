const nombre = document.getElementById("nombre");
const mail = document.getElementById("email");
const psw = document.getElementById("psw");

async function crear(event) {
    console.log("crear");
    event.preventDefault();
    const response = await fetch("/register?nm=" + nombre.value + "&psw=" + psw.value + "&mail=" + mail.value, {
        method: 'POST'
    }).then(response => response.json()).then(function(data) {
        console.log(data)
        if (data == {}) {
            alert("Ese email ya existe");
            return false;
        } else {
            alert("account");
            //window.location.replace("/account");
            return false;
        }
    });
}