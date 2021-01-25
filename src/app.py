from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, session, abort, send_file
from os import environ as env

from src.auth import CrearUsuario, HacerLogin, Usuario
from src.mail import enviarEmail

from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__, static_url_path="/src/web/static")
app.secret_key = "myllavecitasecretita123"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

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
                Usuario().destruir(Usuario(session['user_id']).cojer()["mail"])
                return None
            if not usr["abierto"] == True: 
                usr = None
            return usr
    except Exception as e:
        return None

@app.route("/")
def PaginaPrincipal():

    usr = check_usuario()

    return render_template("index.html", user=usr, usrAdmin=len(Usuario().cojer_admins()), usuarios=len(Usuario().cojer_usuarios()), docs=docs)

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
            return redirect(url_for("Cuenta"))

        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join("./src/static/pfp/", filename))
            Usuario().imagen(session['user_id'], filename)

    return redirect(url_for("Cuenta"))

@app.route("/update", methods=["GET", "POST"])
def Actualizar():

    if request.method == "POST":

        mail = request.args.get("mail", None)
        nombre = request.args.get("nm", None)

        if mail is None or nombre is None:
            abort(404)

        pm = request.args.get("pm", "")
        ap = request.args.get("ap", "")

        direccion = request.args.get("dir", "")
        ci = request.args.get("ci", "")
        pa = request.args.get("pa", "")
        co = request.args.get("co", "")

        bio = request.args.get("bio", "")

        Usuario().actualizar(mail, nombre, pm, ap, direccion, ci, pa, co, bio)
        return {}
    
    return redirect(url_for("Cuenta"))

@app.route("/login", methods=["GET", "POST"])
def LogIn():
    
    if request.method == "POST":
        
        mail = request.args.get("mail")
        psw = request.args.get("psw")

        usr = HacerLogin(mail, psw).ejecutar()
        print(usr)
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

    url = f"{url_main}register/activation/{Usuario(session['user_id']).cojer()['tokenEntrada']}"
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
    except:
        pass
    return redirect(url_for("Cuenta"))

# Dashboard

@app.route("/dashboard")
def Cuenta():

    usr = check_usuario()

    if usr is None:
        return redirect(url_for('Registrarse'))

    return render_template("dashboard/index.html", user=usr, docs=docs)
    
@app.route("/dashboard/account/delete")
def EliminarCuenta():

    usr = check_usuario()

    if usr is not None:
        Usuario(session['user_id']).eliminar()

    return redirect(url_for('PaginaPrincipal'))

def run():
    app.run()