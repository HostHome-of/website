from flask import Flask, render_template, request, redirect, url_for, session

from src.auth import Usuario, CrearUsuario

app = Flask(__name__, static_url_path="/src/web/static")
app.secret_key = "myllavecitasecretita123"

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
                return redirect(url_for('Auth'))
    except Exception as e:
        return redirect(url_for('PaginaPrincipal'))

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

@app.route("/auth")
def Auth():

    try:
        if session['user_id']:
            if Usuario(session['user_id']).cojer():
                return redirect(url_for('PaginaPrincipal'))
    except:
        pass

    return render_template("auth.html")

@app.route("/login")
def LogIn():

    return render_template("auth.html")

@app.route("/register", methods=["GET", "POST"])
def Registrarse():

    if request.method == "POST":

        mail = request.form["mail"]
        psw = request.form["password"]
        nombre = request.form["name"]

        try:
            if session['user_id']:
                usr = session['user_id']
                if usr is None:
                    usr = CrearUsuario(nombre, psw, mail).crear()
                    session['user_id'] = usr
                    return redirect(url_for("PaginaPrincipal"))
                elif not usr["abierto"]:
                    usr = CrearUsuario(nombre, psw, mail).crear()
                    session['user_id'] = usr
                    return redirect(url_for("PaginaPrincipal"))
                else:
                    return redirect(url_for("Auth"))
        except:
            usr = CrearUsuario(nombre, psw, mail).crear()
            session['user_id'] = usr
            return redirect(url_for("PaginaPrincipal"))

    return redirect(url_for("Auth"))

def run():
    app.run()