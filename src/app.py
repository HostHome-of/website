from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, session, abort, send_file
from os import environ as env

from src.auth import CrearUsuario, HacerLogin, Usuario
from src.mail import enviarEmail
from src.sockets import enviar

from werkzeug.utils import secure_filename
import os
import requests

from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__, static_url_path="/src/web/static")
app.secret_key = "myllavecitasecretita123"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# GitHub login
github_blueprint = make_github_blueprint(client_id=str(env["GITHUB_ID"]),
                                        client_secret=str(env["GITHUB_KEY"]),
                                        redirect_to="crearHost")

app.register_blueprint(github_blueprint, url_prefix="/github_login")

# Repos
def get_repositories(url, usr):
    result = []
    r = requests.get(url=url)
    if 'next' in r.links :
        result += get_repositories(r.links['next']['url'], usr)

    for repository in r.json():
        try:
            result.append(f"{usr}/{repository.get('name')}")
        except:
            result.append(f"{usr}/{repository}")

    return result

# Docs / Url
docs = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["docs"]
url_main = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]

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

def check_usuario():
    try:
        if session['user_id']:
            usr = Usuario(session['user_id']).cojer()
            if usr["autorizado"] == False:
                Usuario().petar(Usuario(session['user_id']).cojer()["mail"])
                return None
            if not usr["cuentas"][str(session['user_id'])] == True: 
                usr = None
            return usr
    except Exception as e:
        return None 

@app.route("/")
def PaginaPrincipal():

    usr = check_usuario()
    if request.args.get("g", None) == "1":
        return redirect(url_for("crearHost"))

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
        print(request.files)

        if image.filename == "":
            return redirect("/dashboard/edit/imagen")

        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join("./src/static/pfp/", filename))
            Usuario().imagen(session['user_id'], filename)

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

@app.route("/login", methods=["GET", "POST"])
def LogIn():
    
    if request.method == "POST":
        
        mail = request.args.get("mail")
        psw = request.args.get("psw")

        usr = HacerLogin(mail, psw).ejecutar()
        if usr == False:
            return {}
        session['user_id'] = usr
        return Usuario(usr).cojer()

    usr = check_usuario()
    if usr is not None:
        return redirect(url_for('PaginaPrincipal'))

    return render_template("login.html", key=env["CAPTCHA_WEB"])

@app.route("/register", methods=["GET", "POST"])
def Registrarse():

    if request.method == "POST":

        mail = request.args.get("mail")
        psw = request.args.get("psw")
        nombre = request.args.get("nm")

        usr = CrearUsuario(nombre, psw, mail).crear()
        if usr == False:
            return {}
        session['user_id'] = usr

        return {"estado": 200}

    usr = check_usuario()
    if usr is not None:
        return redirect(url_for('PaginaPrincipal'))

    return render_template("register.html", key=env["CAPTCHA_WEB"])

@app.route("/register/activation")
def activarCuenta():

    try:
        url = f"{url_main}register/activation/{Usuario(session['user_id']).cojer()['tokenEntrada']}"
    except:
        return redirect(url_for("Registrarse"))
    print(url)
    email = render_template("mails/codigo.html", url=url)
    try:
        enviarEmail(Usuario(session['user_id']).cojer(), email, "Codigo de verificacion", True)
    except Exception as e:
        print(e)
    return render_template("checkmail.html")

@app.route("/register/activation/<codigo>")
def activarCuentaCodigo(codigo):

    data = Usuario().activar(Usuario(session['user_id']).cojer()["mail"], codigo)
    if data == False:
        return redirect("/")

    try:
        enviarEmail(Usuario(session['user_id']).cojer(), "./src/templates/mails/recien.html", "Gracias por unirte")
    except Exception as e:
        print(e)

    return redirect(url_for("Cuenta"))

# Dashboard

@app.route("/dashboard")
def Cuenta():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))

    return render_template("dashboard/index.html", user=usr, docs=docs)
    
@app.route("/dashboard/edit")
def editarCuenta():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))

    return render_template("dashboard/edit.html", user=usr, docs=docs)

@app.route("/dashboard/host")
def mirarHosts():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))
    
    hosts = {}

    return render_template("projectos/hosts.html", hostsLen=len(hosts), user=usr, docs=docs, hosts=hosts)

@app.route("/host/new", methods=["GET", "POST"])
def crearHost():

    if request.method == "POST":
        nombre = request.args.get("nombre")
        url    = request.headers.get("url") 
        if url is None:
            abort(404)
        data = enviar(f"crear|{nombre}|{url}")
        print(data)
        print(data[0])
        if bool(data[0]) == False:
            return {"error": data[1]}
        return {"estado": 200}

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
def editarCuentaConPagina(pagina):

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))

    try:
        return render_template(f"dashboard/{pagina}.html", user=usr, docs=docs, pfp=usr["pfp"], key=env["CAPTCHA_WEB"])
    except:
        abort(404)


@app.route("/dashboard/account/delete")
def EliminarCuenta():

    usr = check_usuario()

    if usr is not None:
        Usuario(session['user_id']).eliminar()

    return redirect(url_for('PaginaPrincipal'))

@app.route("/dashboard/account/destroy")
def DestruirCuenta():

    usr = check_usuario()

    if usr is not None:
        Usuario(session['user_id']).destruir()

    return redirect(url_for('PaginaPrincipal'))

@app.route("/dashboard/logout/<string:field>")
def quitarTerceros(field):
    if field == "github":
        if github.authorized:
            del github_blueprint.token
    
    return "ok"

def run():
    app.run()