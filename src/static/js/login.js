function alertNoty(text, typeAlert, fill) {
    new Noty({
        text: text,
        theme: 'nest',
        timeout: 4000,
        type: typeAlert,
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
        alertNoty('Email o contraseña no validos (Espera unos segundos)', 'error', '#c0392b');

        setTimeout(function() {
            window.location.reload();
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