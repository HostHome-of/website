from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, session, abort, send_file, flash
from os import environ as env

from src.auth import CrearUsuario, HacerLogin, Password, Usuario 
from src.mail import enviarEmail

from werkzeug.utils import secure_filename
import os
import requests

from flask_dance.contrib.github import make_github_blueprint, github
from functools import wraps
from flask.json import jsonify
import datetime
import json

from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session

app = Flask(__name__, static_url_path="/src/web/static")
app.secret_key = "myllavecitasecretita123"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# GitHub login
github_blueprint = make_github_blueprint(client_id=str(env["GITHUB_ID"]),
                                        client_secret=str(env["GITHUB_KEY"]),
                                        redirect_to="quitarWindow")

app.register_blueprint(github_blueprint, url_prefix="/github_login")

# Google login
GOOGLE_CLIENT_ID     = env["GOOGLE_ID"]
GOOGLE_CLIENT_SECRET = env["GOOGLE_SECRETE"]

# Esto es un mal gasto
@app.route("/quitar/window")
def quitarWindow():
    return """<html><body onload="cerrar()"><script>function cerrar() {opener.location.reload(1);window.close();}</script></body></html>"""

# Repos
def get_repositories(url, usr):
    result = {}
    r = requests.get(url=url)
    if 'next' in r.links :
        get_repositories(r.links['next']['url'], usr)

    for repository in r.json():
        try:
            result[repository.get('name')] = {}
            result[repository.get('name')]["len"] = repository.get('language')
            result[repository.get('name')]["branch"] = repository.get("default_branch")
            result[repository.get('name')]["url"] = repository.get("html_url")
            result[repository.get('name')]["usr"] = usr
            
        except:
            pass

    return result

# Docs / Url
docs     = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["docs"]
url_main = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]

# Google url
google_url_login = f"{url_main}authorize/google/login"
google_url_register = f"{url_main}authorize/google/register"

client_google = WebApplicationClient(GOOGLE_CLIENT_ID)

# Aplicacion instalable
@app.route('/service-worker.js')
@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js'), 200, {'Content-Type': 'text/javascript'}

@app.route("/src/web/static/images/favicon.png")
@app.route("/favicon.ico")
def iconos():
    return app.send_static_file('images/favicon.png'), 200, {'Content-Type': 'image/png'}

# Errores

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html', docs=docs), 404

# -----------------------------------------------------------------------------

# Resto de la web

def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        if user_id:
            user = Usuario(request.cookies.get('user_id')).cojer()
            if not user:
                flash("Porfavor haz login")
                return redirect(url_for('login'))
            if user:
                if not user.get("autorizado"):
                    Usuario().petar(user["mail"])
                    return redirect(url_for('login'))
                return function_to_protect(*args, **kwargs)
            else:
                return redirect(url_for('login'))
        else:
            flash("Porfavor haz login")
            return redirect(url_for('login'))
    return wrapper 

def already_logedin(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        user = Usuario(user_id).cojer()
        if user:
            return redirect("/")
        else:
            return function_to_protect(*args, **kwargs)
    return wrapper 

def check_usuario():
    if request.cookies.get('user_id'):
        usr = Usuario(request.cookies.get('user_id')).cojer()
        if usr is None:
            return None
        if not usr["autorizado"]:
            Usuario().petar(Usuario(request.cookies.get('user_id')).cojer()["mail"])
            return None
        if not usr["cuentas"][str(request.cookies.get('user_id'))]: 
            return None
        return usr
    return None

@app.route("/")
def PaginaPrincipal():

    usr = check_usuario()
    # if request.args.get("g", None) == "1":
    #     return redirect(url_for("crearHost"))

    if usr and request.args.get("r", None) == "true" or not usr:
        return render_template("index.html", user=usr, usrAdmin=len(Usuario().cojer_admins()), usuarios=len(Usuario().cojer_usuarios()), docs=docs)

    return redirect(url_for("Cuenta"))

def allowed_image(filename):
    
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/img", methods=["GET", "POST"])
def Imagen():
    
    if request.method == "POST":
        
        image = request.files["imgInp"]

        if image.filename == "":
            return redirect("/dashboard/edit/imagen")

        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join("./src/static/pfp/", filename))
            Usuario().imagen(request.cookies.get('user_id'), filename)

    return redirect("/dashboard/edit/imagen")

@app.route("/update", methods=["GET", "POST"])
def Actualizar():

    if request.method == "POST":

        email = request.args.get("email", None)

        mail = request.args.get("mail", None)
        nombre = request.args.get("nm", None)

        if mail is None or nombre is None:
            abort(404)

        if email is not None:
            uno = request.args.get("uno", "false")
            dos = request.args.get("dos", "false")
            tres = request.args.get("tres", "false")
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
    
    return redirect(url_for("Cuenta"))

# ============================================== Autentificacion

@app.route("/login", methods=["GET", "POST"])
@already_logedin
def login():
    
    if request.args.get("google", None):
        authorization_endpoint = requests.get(("https://accounts.google.com/.well-known/openid-configuration")).json()["authorization_endpoint"]
        request_uri = client_google.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=url_main + "authorize/google/login",
            scope=["openid", "email", "profile"]
        )
        return redirect(request_uri)
    
    if request.method == "POST":
        
        mail = request.args.get("mail")
        psw = request.args.get("psw")

        consola = request.args.get("consola", None)

        if consola is not None:
            usr = HacerLogin(mail, psw).ejecutar()
            if usr == False:
                return {}
            
            return usr

        usr = HacerLogin(mail, psw).ejecutar(request.cookies.get('user_id'))
        if usr == False:
            return {}
        out = jsonify(state=0, msg=Usuario(usr).cojer())
        
        out.set_cookie('user_id', usr, expires=datetime.datetime.now() + datetime.timedelta(days=60))
        return out

    return render_template("login.html", key=env["CAPTCHA_WEB"])

@app.route("/authorize/google/login")
def google_login():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": request.args.get("code"),
        "grant_type": "authorization_code",
        "redirect_uri": google_url_login
    })

    code = request.args.get("code")
    google_provider_cfg = requests.get(("https://accounts.google.com/.well-known/openid-configuration")).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client_google.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    print(token_response.json())
    # client_google.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    # print(userinfo_endpoint)
    # uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(token_url, headers=headers, data=body)

    mail = userinfo_response.json()["email"]
    print(mail)

    # r_mail = requests.get('https://www.googleapis.com/oauth/email?access_token=' + r.json()['access_token'], data={"scope":["https://www.googleapis.com/auth/userinfo.email"]})
    # mail   = json.loads(r.text)
    # data   = HacerLogin().google(mail, request.cookies.get('user_id'))

    # if not data:
    #     return redirect("/login?err=google")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
@already_logedin
def Registrarse():

    if request.method == "POST":

        mail = request.args.get("mail")
        psw = request.args.get("psw")
        nombre = request.args.get("nm")

        usr = CrearUsuario(nombre, psw, mail).crear()
        if usr == False:
            return {}
        out = jsonify(state=0, msg={"estado": 200})
        out.set_cookie('user_id', usr, expires=datetime.datetime.now() + datetime.timedelta(days=60))
        return out

    return render_template("register.html", key=env["CAPTCHA_WEB"])

@app.route("/psw/check", methods=["GET", "POST"])
def mirarPsw():

    if request.method == "POST":

        psw = request.headers.get("psw")
        pswCheck = Password(Usuario(request.cookies.get('user_id')).cojer()["psw"]).check(psw)
        return {"valido": pswCheck}


    return redirect("/")

@app.route("/register/activation", methods=["GET", "POST"])
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

@app.route("/register/activation/<codigo>", methods=["GET", "POST"])
def activarCuentaCodigo(codigo):

    if request.method == "POST":
        data = Usuario().activar(Usuario(request.cookies.get('user_id')).cojer()["mail"], codigo)
        if data == False:
            return {"codigo": 500}

        try:
            email = render_template("mails/recien.html", url=url_main)
            enviarEmail(Usuario(request.cookies.get('user_id')).cojer(), email, "Gracias por unirte", True)
        except Exception as e:
            return {"codigo": 500}

        return {"codigo": 200}

# ============================================== FIN Autentificacion


# ============================================== Dashboard

@app.route("/dashboard")
@login_required
def Cuenta():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))

    return render_template("dashboard/index.html", user=usr, docs=docs)
    
@app.route("/dashboard/edit")
@login_required
def editarCuenta():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))

    githubUsr = None

    if github.authorized:
        info_github = github.get("/user")

        if info_github.ok:
            githubUsr = info_github.json()

    return render_template("dashboard/edit.html", user=usr, docs=docs, github=githubUsr)

@app.route("/dashboard/host")
@login_required
def mirarHosts():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))
    
    hosts = {}

    return render_template("projectos/hosts.html", hostsLen=len(hosts), user=usr, docs=docs, hosts=hosts)

@app.route("/dashboard/friends")
@login_required
def amigos():

    usr    = check_usuario()
    invite = Usuario().cojerInvite(usr["mail"])

    return render_template("dashboard/amigos.html", user=usr, invites=invite, url=url_main)

@app.route("/host/new", methods=["GET", "POST"])
@login_required
def crearHost():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))

    if not github.authorized:
        return redirect("/dashboard/edit#apps")

    info_github = github.get("/user")

    if info_github.ok:
        info_json_github = info_github.json()
        repos = get_repositories(str(f"https://api.github.com/users/{info_json_github['login']}/repos"), info_json_github['login'])
        return render_template("projectos/new.html", user=usr, docs=docs, info_github=info_json_github, repos=repos, key=env["CAPTCHA_WEB"])

    del github_blueprint.token
    return redirect(url_for("crearHost"))

@app.route("/dashboard/edit/<string:pagina>")
@login_required
def editarCuentaConPagina(pagina):

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))

    try:
        return render_template(f"dashboard/{pagina}.html", user=usr, docs=docs, pfp=usr["pfp"], key=env["CAPTCHA_WEB"])
    except:
        abort(404)


@app.route("/dashboard/account/delete")
@login_required
def EliminarCuenta():

    usr = check_usuario()

    if usr is not None:
        Usuario(request.cookies.get('user_id')).eliminar()

    return redirect(url_for('Cuenta'))

@app.route("/dashboard/account/destroy")
@login_required
def DestruirCuenta():

    usr = check_usuario()

    if usr is not None:
        Usuario(request.cookies.get('user_id')).destruir()

    return redirect(url_for('PaginaPrincipal'))

@app.route("/dashboard/logout/<string:field>", methods=["GET", "POST"])
@login_required
def quitarTerceros(field):
    if request.method == "POST":
        if field == "github":
            if github.authorized:
                del github_blueprint.token
        
        return "ok"

    return redirect(url_for("Cuenta"))

# ============================================== FIN Dashboard


def run():
    app.run()