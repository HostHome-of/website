from flask import Flask, render_template, request, redirect, url_for, session

from src.auth import CrearUsuario, HacerLogin, Usuario

app = Flask(__name__, static_url_path="/src/web/static")
app.secret_key = "myllavecitasecretita123"

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

@app.route("/")
def PaginaPrincipal():

    usr = None

    try:
        if session['user_id']:
            usr = Usuario(session['user_id']).cojer()
            if not usr["abierto"] == True: 
                usr = None
    except Exception as e:
        pass

    return render_template("index.html", user=usr)

@app.route("/account")
def Cuenta():

    usr = None

    try:
        if session['user_id']:
            usr = Usuario(session['user_id']).cojer()
            if not usr["abierto"] == True: 
                return redirect(url_for('Registrarse'))
    except Exception as e:
        print(e)
        return redirect(url_for('Registrarse'))

    return render_template("account.html", user=usr)

@app.route("/features")
def Features():

    usr = None

    try:
        if session['user_id']:
            usr = Usuario(session['user_id']).cojer()
            if not usr["abierto"] == True: 
                usr = None
    except Exception as e:
        pass

    return render_template("features.html", user=usr)

@app.route("/docs")
def Docs():

    usr = None

    try:
        if session['user_id']:
            usr = Usuario(session['user_id']).cojer()
            if not usr["abierto"] == True: 
                usr = None
    except Exception as e:
        pass

    return render_template("docs.html", user=usr)

@app.route("/account/delete")
def EliminarCuenta():

    usr = None

    try:
        if session['user_id']:
            usr = Usuario(session['user_id']).eliminar()
    except Exception as e:
        pass

    return redirect(url_for('PaginaPrincipal'))

# @app.route("/project/<id>", methods=["POST", "GET"])
# def ProjectoView(id=None):

#     usr = None

#     try:
#         if session['user_id']:
#             usr = Usuario(session['user_id']).cojer()
#             if usr is not None:
#                 p = Projecto().cojer(id)
#                 if p is not None:
#                     return render_template("projecto.html", projecto=p)
#                 return redirect(url_for("CrearProjecto"))
#     except Exception as e:
#         pass

#     return redirect(url_for('Registrarse'))   

# @app.route("/project/new", methods=["POST", "GET"])
# def CrearProjecto():

#     usr = None

#     if request.method == "POST":

#         nombre = request.form["nombre"]
#         repo = request.form["repo"]

#         p = Projecto().crear(nombre, repo)
#         return redirect("/project/{p}")

#     try:
#         if session['user_id']:
#             usr = Usuario(session['user_id']).cojer()
#             if usr is not None:
#                 return render_template("projectos/cli.html", user=usr)
#     except Exception as e:
#         pass

#     return redirect(url_for('Registrarse'))

@app.route("/project/new/github", methods=["POST", "GET"])
def CrearProjectoGithub():

    usr = None

    if request.method == "POST":

        nombre = request.form["nombre"]
        repo = request.form["repo"]

        p = Projecto().crear(nombre, repo)
        return redirect("/project/{p}")

    try:
        if session['user_id']:
            usr = Usuario(session['user_id']).cojer()
            if usr is not None:
                return render_template("projectos/github.html", user=usr)
    except Exception as e:
        pass

    return redirect(url_for('Registrarse'))

@app.route("/login", methods=["GET", "POST"])
def LogIn():

    try:
        if session['user_id']:
            if Usuario(session['user_id']).cojer()["abierto"] == True:
                return redirect(url_for('PaginaPrincipal'))
    except:
        pass

    if request.method == "POST":
    
        mail = request.args.get("mail")
        psw = request.args.get("psw")
        nombre = request.args.get("nm")

        usr = HacerLogin(mail, psw).ejecutar()
        if usr == False:
            return {}
        session['user_id'] = usr
        return {"estado": 200}

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def Registrarse():

    try:
        if session['user_id']:
            if Usuario(session['user_id']).cojer()["abierto"] == True:
                return redirect(url_for('PaginaPrincipal'))
    except:
        pass

    if request.method == "POST":

        mail = request.args.get("mail")
        psw = request.args.get("psw")
        nombre = request.args.get("nm")

        usr = CrearUsuario(nombre, psw, mail).crear()
        if usr == False:
            return {}
        session['user_id'] = usr
        return {"estado": 200}

    return render_template("register.html")

def run():
    app.run()