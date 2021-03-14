from flask import Blueprint, render_template, abort, redirect, url_for, request
from werkzeug.utils import secure_filename
from flask.json import jsonify

from os import environ as env

from src.utilities import Utils
from src.auth import Usuario, CrearUsuario, HacerLogin, Password
from src.app import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, app, github, github_blueprint, api_key
from src.mail import enviarEmail

import requests
import os
import datetime

main_page           = Blueprint('main_page', __name__)
utils               = Utils()

docs                = utils.docs
check_usuario       = utils.check_usuario
google_url_login    = utils.google_url_login
google_url_register = utils.google_url_register
url_main            = utils.main_url
login_required      = utils.login_required
already_logedin     = utils.already_logedin
check_usuario       = utils.check_usuario
get_repositories    = utils.get_repositories

# Esto es un mal gasto
@main_page.route("/quitar/window")
def quitarWindow():
    return """<html><body onload="cerrar()"><script>function cerrar() {opener.location.reload(1);window.close();}</script></body></html>"""

# Errores
@app.errorhandler(404)
def error_404(e):
    return render_template('404.html', docs=docs), 404

# -----------------------------------------------------------------------------

# Resto de la web

@main_page.route("/")
def PaginaPrincipal():

    usr = check_usuario()
    # if request.args.get("g", None) == "1":
    #     return redirect(url_for("main_page.crearHost"))

    if usr and request.args.get("r", None) == "true" or not usr:
        return render_template("index.html", user=usr, usrAdmin=len(Usuario().cojer_admins), usuarios=len(Usuario().cojer_usuarios), docs=docs)

    return redirect(url_for("main_page.Cuenta"))

def allowed_image(filename):
    
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@main_page.route("/img", methods=["GET", "POST"])
def Imagen():
    
    if request.method == "POST":
        
        image = request.files["imgInp"]

        if image.filename == "":
            return redirect("/dashboard/edit")

        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join("./src/static/pfp/", filename))
            Usuario().imagen(request.cookies.get('user_id'), filename)

    return redirect("/dashboard/edit")

@main_page.route("/update", methods=["GET", "POST"])
def Actualizar():

    if request.method == "POST":

        email = request.args.get("email", None)

        mail = request.args.get("mail", None)
        nombre = request.args.get("nm", None)

        if mail is None or nombre is None:
            abort(404)

        if email is not None:
            uno    = request.args.get("uno", "false")
            dos    = request.args.get("dos", "false")
            tres   = request.args.get("tres", "false")
            cuatro = request.args.get("cuatro", "false")
            
            uno    = uno    if uno    != "false" else ""
            dos    = dos    if dos    != "false" else ""
            tres   = tres   if tres   != "false" else ""
            cuatro = cuatro if cuatro != "false" else ""

            Usuario().actualizarPreferencias(mail, uno, dos, tres, cuatro)
            return {"estado": 200}

        segundo = request.args.get("segundo", "")
        edad = request.args.get("edad", "") 

        Usuario().actualizar(mail, nombre, segundo, edad)
        return {}
    
    return redirect(url_for("main_page.Cuenta"))

# ============================================== Autentificacion

@main_page.route("/login", methods=["GET", "POST"])
@already_logedin
def login():
    
    if request.args.get("google", None):
        return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?scope=email&access_type=offline&include_granted_scopes=true&response_type=code&redirect_uri={google_url_login}&client_id={GOOGLE_CLIENT_ID}")
    
    if request.method == "POST":
        
        mail    = request.args.get("mail")
        psw     = request.args.get("psw")
        consola = request.args.get("consola", None)
        usr     = HacerLogin(mail, psw).ejecutar()

        if not usr:
            return {}

        out = jsonify(state=0, msg=Usuario(usr).cojer())
        
        if not consola:
            out.set_cookie('user_id', usr, expires=datetime.datetime.now() + datetime.timedelta(days=60))
        return out

    error = None
    if request.args.get("err") == "google":
        error = "google"

    return render_template("login.html", key=env["CAPTCHA_WEB"], error=error)

@main_page.route("/authorize/google/login")
@already_logedin
def google_login():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": request.args.get("code"),
        "grant_type": "authorization_code",
        "redirect_uri": google_url_login
    })

    user   = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={r.json()["access_token"]}').json()
    data   = HacerLogin().google(user["email"])

    if not data:
        return redirect("/login?err=google")
    res = redirect("/")
    res.set_cookie('user_id', data, expires=datetime.datetime.now() + datetime.timedelta(days=60))
    return res

@main_page.route("/register", methods=["GET", "POST"])
@already_logedin
def Registrarse():

    if request.args.get("google", None):
        return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?scope=email profile&access_type=offline&include_granted_scopes=true&response_type=code&redirect_uri={google_url_register}&client_id={GOOGLE_CLIENT_ID}")

    if request.method == "POST":

        mail = request.args.get("mail")
        psw = request.args.get("psw")
        nombre = request.args.get("nm")

        usr = CrearUsuario(nombre, psw, mail).crear()
        if not usr:
            return {}
        out = jsonify(state=0, msg={"estado": 200})
        out.set_cookie('user_id', usr, expires=datetime.datetime.now() + datetime.timedelta(days=60))
        return out

    return render_template("register.html", key=env["CAPTCHA_WEB"])

@main_page.route("/psw")
def psw_for_google():
    if request.args.get("ctx") == "253681d6-48f8-421d-a393-2f7c26a01313":
        return render_template("google_psw.html")
    abort(404)

@main_page.route("/authorize/google/register", methods=["POST", "GET"])
def google_register():
    if request.method == "POST":
        psw = request.args.get("psw")
        if psw:
            cookie = CrearUsuario().google(psw, request.cookies.get('user_id'), psw=True)
            res = redirect("/psw?ctx=253681d6-48f8-421d-a393-2f7c26a01313")
            res.set_cookie('user_id', cookie, expires=datetime.datetime.now() + datetime.timedelta(days=60))
            return res
        return redirect("/")

    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": request.args.get("code"),
        "grant_type": "authorization_code",
        "redirect_uri": google_url_register
    })

    user   = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={r.json()["access_token"]}').json()
    data   = CrearUsuario().google(user, request.cookies.get('user_id'))

    if data is None:
        return redirect("/register?err=google")

    res = redirect("/psw?ctx=253681d6-48f8-421d-a393-2f7c26a01313")
    res.set_cookie('user_id', data, expires=datetime.datetime.now() + datetime.timedelta(days=60))
    return res

@main_page.route("/psw/check", methods=["GET", "POST"])
def mirarPsw():

    if request.method == "POST":

        psw = request.headers.get("psw")
        pswCheck = Password(Usuario(request.cookies.get('user_id')).cojer()["psw"]).check(psw)
        return {"valido": pswCheck}


    return redirect("/")

@main_page.route("/register/activation", methods=["GET", "POST"])
def activarCuenta():

    if request.method == "POST":
        usuario = Usuario(request.cookies.get('user_id')).cojer()
        codigo = str(usuario["tokenEntrada"])
        nombre = usuario["nombre"]
        
        email = render_template("mails/codigo.html", codigo=codigo, nombre=nombre)
        try:
            enviarEmail(Usuario(request.cookies.get('user_id')).cojer(), email, "Codigo de verificacion", True)
        except Exception as e:
            return {"codigo": 500}
        return {"codigo": Usuario(request.cookies.get('user_id')).cojer()['tokenEntrada']}
    return "tu que haces aqui?"

@main_page.route("/register/activation/<codigo>", methods=["GET", "POST"])
def activarCuentaCodigo(codigo):

    if request.method == "POST":
        data = Usuario().activar(request.cookies.get('user_id'), codigo)
        if not data:
            return {"codigo": 500}

        try:
            email = render_template("mails/recien.html", url=url_main)
            enviarEmail(Usuario(request.cookies.get('user_id')).cojer(), email, "Gracias por unirte", True)
        except Exception as e:
            return {"codigo": 500}

        return {"codigo": 200}

# ============================================== FIN Autentificacion


# ============================================== Dashboard

@main_page.route("/dashboard")
@login_required
def Cuenta():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('main_page.Registrarse'))

    return render_template("dashboard/index.html", user=usr, docs=docs)
    
@main_page.route("/dashboard/edit")
@login_required
def editarCuenta():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('main_page.Registrarse'))

    githubUsr = None

    if github.authorized:
        info_github = github.get("/user")

        if info_github.ok:
            githubUsr = info_github.json()

    return render_template("dashboard/edit.html", user=usr, docs=docs, github=githubUsr, gitReq=True if request.args.get("ctx") == "b1c923ca-66d7-4488-976c-d6b7f9794dfc" else False)

@main_page.route("/dashboard/host")
@login_required
def mirarHosts():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('main_page.Registrarse'))
    
    hosts = {}

    return render_template("projectos/hosts.html", hostsLen=len(hosts), user=usr, docs=docs, hosts=hosts)

@main_page.route("/dashboard/friends")
@login_required
def amigos():

    usr    = check_usuario()
    invite = Usuario(request.cookies.get("user_id")).cojerInvite

    return render_template("dashboard/amigos.html", user=usr, invites=invite, url=url_main)

@main_page.route("/host/new", methods=["GET", "POST"])
@login_required
def crearHost():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('main_page.Registrarse'))

    if not github.authorized:
        return redirect("/dashboard/edit?ctx=b1c923ca-66d7-4488-976c-d6b7f9794dfc")

    info_github = github.get("/user")

    if info_github.ok:
        info_json_github = info_github.json()
        repos = get_repositories(str(f"https://api.github.com/users/{info_json_github['login']}/repos"), info_json_github['login'])
        return render_template("projectos/new.html", user=usr, docs=docs, info_github=info_json_github, repos=repos, key=env["CAPTCHA_WEB"])

    del github_blueprint.token
    return redirect(url_for("main_page.crearHost"))

@main_page.route("/dashboard/edit/<string:pagina>")
@login_required
def editarCuentaConPagina(pagina):

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('main_page.Registrarse'))

    try:
        return render_template(f"dashboard/{pagina}.html", user=usr, docs=docs, pfp=usr["pfp"], key=env["CAPTCHA_WEB"])
    except:
        abort(404)


@main_page.route("/dashboard/account/delete")
@login_required
def EliminarCuenta():

    usr = check_usuario()

    if usr is not None:
        res = redirect(url_for('main_page.Cuenta'))
        res.set_cookie('user_id', '', expires=0)
        return res

    return redirect(url_for('main_page.Cuenta'))

@main_page.route("/dashboard/account/destroy")
@login_required
def DestruirCuenta():

    usr = check_usuario()

    if usr is not None:
        Usuario(request.cookies.get('user_id')).destruir()

    return redirect(url_for('main_page.PaginaPrincipal'))

@main_page.route("/dashboard/logout/<string:field>", methods=["GET", "POST"])
@login_required
def quitarTerceros(field):
    if request.method == "POST":
        if field == "github":
            if github.authorized:
                del github_blueprint.token
        
        return "ok"

    return redirect(url_for("main_page.Cuenta"))
