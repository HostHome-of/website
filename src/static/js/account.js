// $("#imgInp").change(function(){
//     $("#formImg").submit();
// });

function guardar() {
    const nombre = document.getElementById("nombre").value;
    const email = document.getElementById("mail").value;

    if (nombre == "" || email == "") {
        Notiflix.Notify.Failure('Email o nombre no pueden ser vacios');
        return;
    }

    let url = "/update?mail="+email+"&nm="+nombre

    const sn = document.getElementById("sn").value;

    if (sn != "") {
        url += "&segundo="+sn
    }

    const eddad = document.getElementById("eddad").value;

    if (eddad != "") {
        url += "&edad="+eddad
    }

    fetch(url, {
        method: 'POST'
    })

    window.location.reload()
}

try {
    var eddadAnterior = document.getElementById("eddad").value;
    var apellidoAnterior = document.getElementById("sn").value;
    var nombreAnterior = document.getElementById("nombre").value;
} catch (e) {

}

function cambiarBtn() {
    let btn = document.getElementById("btnSubmity");

    if (document.getElementById("eddad").value != eddadAnterior || document.getElementById("sn").value != apellidoAnterior || document.getElementById("nombre").value != nombreAnterior) {
        btn.disabled = false;
    } else {
        btn.disabled = true;
    }
}

function upadeEmail(mail, nombre) {
    checky1 = !document.getElementsByName("checky1")[0].checked;
    checky2 = !document.getElementsByName("checky2")[0].checked;
    checky3 = !document.getElementsByName("checky3")[0].checked;
    checky4 = !document.getElementsByName("checky4")[0].checked;

    console.log(mail)
    console.log(nombre)

    fetch("/update?email=true&mail="+mail+"&nm="+nombre+"&uno="+checky1+"&dos="+checky2+"&tres="+checky3+"&cuatro="+checky4, {
        method: "POST"
    })

}

function updatePasswordCheck() {
    const psw = document.getElementById("password").value;
    const npsw = document.getElementById("npassword").value;
    const rpsw = document.getElementById("rpassword").value;

    const btn = document.getElementById("spassword");

    if (psw != "" && npsw != "" && rpsw != "") {
        if (npsw == rpsw) {
            btn.disabled = false;
        } else {
            btn.disabled = true;
        }
    } else {
        btn.disabled = true;
    }
}

function updatePassword() {
    const psw = document.getElementById("password").value;
    const npsw = document.getElementById("npassword").value;

    if (psw != npsw) {

    } else {
        Notiflix.Notify.Failure('La contraseña nueva es igual a la anterior que has introducido');
    }
}