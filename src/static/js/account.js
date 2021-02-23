// $("#imgInp").change(function(){
//     $("#formImg").submit();
// });

function alertNoty(text, typeAlert, fill) { // fil :: #EBD761
    new Noty({
        text: text,
        theme: 'nest',
        type: typeAlert,
        timeout: 4000,
        animation: {
            open: function (promise) {
                var n = this;
                var Timeline = new mojs.Timeline();
                var body = new mojs.Html({
                    el: n.barDom,
                    x: { 500: 0, delay: 0, duration: 500, easing: 'elastic.out' },
                    isForce3d: true,
                    onComplete: function () {
                        promise(function (resolve) {
                            resolve();
                        })
                    }
                });

                var parent = new mojs.Shape({
                    parent: n.barDom,
                    width: 200,
                    height: n.barDom.getBoundingClientRect().height,
                    radius: 0,
                    x: { [150]: -150 },
                    duration: 1.2 * 500,
                    isShowStart: true
                });

                n.barDom.style['overflow'] = 'visible';
                parent.el.style['overflow'] = 'hidden';

                var burst = new mojs.Burst({
                    parent: parent.el,
                    count: 10,
                    top: n.barDom.getBoundingClientRect().height + 75,
                    degree: 90,
                    radius: 75,
                    angle: { [-90]: 40 },
                    children: {
                        fill: fill,
                        delay: 'stagger(500, -50)',
                        radius: 'rand(8, 25)',
                        direction: -1,
                        isSwirl: true
                    }
                });

                var fadeBurst = new mojs.Burst({
                    parent: parent.el,
                    count: 2,
                    degree: 0,
                    angle: 75,
                    radius: { 0: 100 },
                    top: '90%',
                    children: {
                        fill: fill,
                        pathScale: [.65, 1],
                        radius: 'rand(12, 15)',
                        direction: [-1, 1],
                        delay: .8 * 500,
                        isSwirl: true
                    }
                });

                Timeline.add(body, burst, fadeBurst, parent);
                Timeline.play();
            },
            close: function (promise) {
                var n = this;
                new mojs.Html({
                    el: n.barDom,
                    x: { 0: 500, delay: 10, duration: 500, easing: 'cubic.out' },
                    skewY: { 0: 10, delay: 10, duration: 500, easing: 'cubic.out' },
                    isForce3d: true,
                    onComplete: function () {
                        promise(function (resolve) {
                            resolve();
                        })
                    }
                }).play();
            }
        }
    }).show();
}

async function guardar() {
    const nombre = document.getElementById("nombre").value;
    const email = document.getElementById("mail").value;

    if (nombre == "" || email == "") {
        alertNoty('Email o nombre no pueden ser vacios', 'error', '#c0392b')

        return;
    }

    let url = "/update?mail=" + email + "&nm=" + nombre

    const sn = document.getElementById("sn").value;

    if (sn != "") {
        url += "&segundo=" + sn
    }

    const eddad = document.getElementById("eddad").value;

    if (eddad != "") {
        url += "&edad=" + eddad
    }

    await fetch(url, {
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

    fetch("/update?email=true&mail=" + mail + "&nm=" + nombre + "&uno=" + checky1 + "&dos=" + checky2 + "&tres=" + checky3 + "&cuatro=" + checky4, {
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
        alertNoty('La contraseña nueva es igual a la anterior que has introducido', 'error', '#c0392b')
        // Notiflix.Notify.Failure('La contraseña nueva es igual a la anterior que has introducido');
    }
}

async function enviarInput() {
    const input = document.getElementById("inputByEmail")
    const texto = input.value.replace(" ", "")
    const texto_separado = texto.split(",")

    if (input.value == "") return;


    for (i = 0; i < texto_separado.length; i++) {
        if (!texto_separado[i].match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/)) {
            alertNotyAmigos(`(${texto_separado[i]}) no es un email valido`, 'error', '#c0392b')
            return;
        } else if (texto_separado[i] == "{{ user['mail'] }}") {
            alertNotyAmigos(`En la lista esto tu email, eliminalo`, 'error', '#c0392b')
            return;
        }
    }

    fetch("/friends/add?config=frendsAdd&key=headers", {
        method: "POST",
        header: {
            "mails": JSON.stringify(texto),
            "key": Math.floor(Math.random() * 10)
        }
    })
}