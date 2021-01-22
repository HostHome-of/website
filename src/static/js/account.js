function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function (e) {
            $('#img__prev').attr('src', e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}

$("#imgInp").change(function(){
    readURL(this);
});

function guardar() {
    const nombre = document.getElementById("input-username").value;
    const email = document.getElementById("input-email").value;

    if (nombre == "" || email == "") {
        Notiflix.Notify.Failure('Email o nombre no pueden ser vacios');
        return;
    }

    const url = "/update?mail="+email+"&nm="+nombre

    const pm = document.getElementById("input-first-name").value;

    if (pm != "") {
        url.concat("&pm="+pm)
    }

    const ap = document.getElementById("input-last-name").value;
    if (ap != "") {
        url.concat("&ap="+ap)
    }

    const dir = document.getElementById("input-address").value;
    if (dir != "") {
        url.concat("&dir="+dir)
    }

    const ci = document.getElementById("input-city").value;
    if (ci != "") {
        url.concat("&ci="+ci)
    }
    
    const co = document.getElementById("input-country").value;
    if (co != "") {
        url.concat("&pa="+co)
    }
    
    const po = document.getElementById("input-postal-code").value;
    if (po != "") {
        url.concat("&co="+ po)
    }

    const bio = document.getElementById("bio").value;
    if (bio != "") {
        url.concat("&bio="+bio)
    }

    fetch(url, {
        method: 'POST'
    })

    window.location.replace("/account")
}