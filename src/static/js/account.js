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

var noEsRobotNew = true;

function validateRobotitoCaptchaNewHost() {
    noEsRobotNew = false;
    updateBtnForNewHosting()
}

function updateBtnForNewHosting() {
    const btn = document.getElementById("btnSubmityHostNew");
    const nombre = document.getElementById("hostNombre").value;
    var input = document.getElementById("inputrepo").value;

    if (input != "" && nombre != "" && !noEsRobotNew) {
        if (input.startsWith("github.com/")) {
            btn.disabled = false;
        } else {
            btn.disabled = true;
        }
    } else {
        btn.disabled = true;
    }
}

function createHost() {
    const repo = document.getElementById("inputrepo").value;
    const url = "https://api."+repo.replace('github.com/', 'github.com/repos/')
    fetch(url).then(response => response.json()).then(data => { 
        if(!data.hasOwnProperty('git_url')){ 
            Notiflix.Notify.Failure('Ese repositorio no existe o no es de GitHub');
            return false;
        } else {
            var git_url = data['git_url']
            fetch("/host/new?nombre="+document.getElementById("hostNombre").value, {
                method: "POST",
                headers: {
                    "url": git_url
                }
            }).then(response => response.json()).then(data => {
                console.log(data)
                if (!data.hasOwnProperty('error')) {
                    Notiflix.Notify.Failure(data["error"]);
                } else {
                    alert("Hecho!")
                }
            });
        }
    });
}