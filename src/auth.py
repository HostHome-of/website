import json, random, datetime, requests
import io

import hashlib
import os

from src.db import *
    
_config = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()
docs = _config["docs"]
main_url = _config["url"]
salt = open("salt.txt", "r").read().encode()

def abrir():

    conn = connect("./src/data/users.db")
    q = "SELECT * FROM users"
    return get_db_data( conn, q, json_dict=True )

def cerrar(q):
    conn = connect("./src/data/users.db")
    execute_db(conn, query=q)


class HacerLogin():
    def __init__(self, email=None, psw=None):
        self.email = email
        self.psw = psw

    def google(self, mail):
        usuarios = abrir()

        for usr in usuarios:
            usr_mail = usuarios[usr]["mail"]

            if mail == usr_mail:
                usuarios[usr]["google"] = True
                cerrar(usuarios)
                return usr

        return False

    def ejecutar(self):
        usuarios = abrir()

        for usr in usuarios:
            if usr["mail"] == self.email:
                self.email = usr

        if Password(self.email["psw"]).check(self.psw):
            return self.email

        return False

class Password():
    def __init__(self, texto: str):
        self.texto = texto

    def crear(self):
        pswNueva = hashlib.pbkdf2_hmac('sha256', self.texto.encode('utf-8'), salt, 100000)
        return pswNueva

    def check(self, psw):
        psw = hashlib.pbkdf2_hmac('sha256', psw.encode('utf-8'), salt, 100000)

        key = self.texto
        psw = str(psw)
        print(psw)
        print(key)
        # psw = psw[2:-1]
        
        return key == psw

class Usuario():

    def __init__(self, tk: str=None):
        self.tk = tk

    @property
    def cojerInvite(self):
        usrs = abrir()

        for i in usrs:
            if i["id"] == self.tk:
                invites = {}

                invites["codigo"] = i["id"]
                invites["link"] = main_url + "invite/" + i["id"]

                return invites

    def activar(self, tk, codigo):
        usuarios = abrir()
        for i in usuarios:
            if i["id"] == tk:
                usuario = i

        if int(usuario["tokenEntrada"]) == int(codigo): # Bien
            del usuario["tokenEntrada"]
            usuario["autorizado"] = True

            q = "UPDATE users SET tokenEntrada = {}, autorizado = 1 WHERE id = {}".format(random.randint(1000, 9999), tk)
            cerrar(q)

            
            
            return True
        else: # Mal
            return False

    def cojer(self):
        usuarios = abrir()

        for usr in usuarios:

            if usr["id"] == self.tk:
                return usr

        return None

    def petar(self):
        usrs = abrir()

        for usr in usrs:
            if usr["id"] == self.tk:
                q = "DELETE FROM users WHERE id = " + self.tk
                cerrar(q)

    @property
    def cojer_admins(self):
        data = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()

        return data["admins"]

    @property
    def cojer_usuarios(self):
        return abrir()

    def imagen(self, nm):
        
        q = "UPDATE users SET pfp = \"/src/web/static/pfp/{}\" WHERE id = {}"
        q = q.format(nm, self.tk)

        cerrar(q)

    def actualizar(self, nombre, ap, edad):

        q = "UPDATE users SET segundoNombre = \"{}\", nombre = \"{}\", edad = {} WHERE id = {}"
        q = q.format(ap, nombre, edad, self.tk)

        cerrar(q)

    def actualizarPreferencias(self, uno, dos, tres, cuatro):

        q = "UPDATE users SET emails_uno = {}, emails_dos = {}, emails_tres = {}, emails_cuatro = {} WHERE id = {}"
        q = q.format(uno, dos, tres, cuatro, self.tk)

        cerrar(q)

class CrearUsuario():
    def __init__(self, nombre: str=None, psw: str=None, mail: str=None):
        self.nombre = nombre
        self.psw = psw
        self.mail = mail

    def google(self, usuario, id, psw: bool=False): 
        """Si psw es True usuario se cambiara a psw e id a el email del usuario"""
        usuarios = abrir()

        if psw:

            usuarios[id]["psw"] = str(Password(usuario).crear())
            usuarios[id]["autorizado"] = True

            cerrar(usuarios)
            return id

        USUARIO_EXISTENTE = False

        for usr in usuarios:
            if usuario["email"] == usr["mail"]:
                USUARIO_EXISTENTE = True

        if not USUARIO_EXISTENTE:
            email     = usuario["email"]
            pfp       = usuario["picture"]
            nombre    = usuario["given_name"]
            
            try:
                sn    = usuario["family_name"]
            except KeyError:
                sn    = ""


            # TODO Contraseña

            tkN                     = self.tokenizar()
            now                     = datetime.datetime.now()
            usr                     = {}
            usr["mail"]             = email
            usr["nombre"]           = nombre
            usr["pfp"]              = pfp
            usr["entrada"]          = f"{now.day}/{now.month}/{now.year}"
            usr["segundoNombre"]    = sn
            usr["edad"]             = ""
            usr["autorizado"]       = False
            usr["emails"]           = {}
            usr["emails"]["uno"]    = True
            usr["emails"]["dos"]    = False
            usr["emails"]["tres"]   = False
            usr["emails"]["cuatro"] = True
            usr["google"]           = True
            usr["id"]               = tkN

            cerrar(usr)

            return str(tkN)
        else:
            return None

    def check(self, usuario, token: str):
        if token in usuario:
            return False

    def tokenizar(self):
        usuarios = abrir()
        token_valido = False
        token = ""

        while not token_valido:
            token = str(random.randint(10000000, 90000000))
            for usr in usuarios:
                valido = self.check(usuarios, token)
                if not valido:
                    break
            token_valido = True

        return token

    def crear(self):
        usuarios = abrir()

        if not self.mail in usuarios:

            # En orden para la base de datos

            tkN                     = self.tokenizar()
            usr                     = {}
            now                     = datetime.datetime.now()
            usr["nombre"]           = self.nombre
            usr["mail"]             = self.mail
            usr["psw"]              = Password(self.psw).crear()
            usr["entrada"]          = f"{now.day}/{now.month}/{now.year}"
            usr["segundoNombre"]    = "" 
            usr["edad"]             = "" 
            usr["autorizado"]       = False
            usr["tokenEntrada"]     = random.randint(1000, 9000)
            usr["emails_uno"]       = True
            usr["emails_dos"]       = False
            usr["emails_tres"]      = False
            usr["emails_cuatro"]    = True
            usr["id"]               = tkN
            usr["pfp"]              = f"/src/web/static/pfp/default_hosthome.png" 
            usr["google"]           = False

            q = "INSERT INTO users VALUES ("

            for i in usr:
                if type(usr[i]) == str:
                    q += f" \"{usr[i]}\","
                elif type(usr[i]) == int:
                    q += f" {int(usr[i])},"
                elif type(usr[i]) == bool:
                    if usr[i]:
                        q += f" 1,"
                    else:
                        q += f" 0,"
                elif type(usr[i]) == bytes:
                    i = str(usr[i]).replace('\\', '\\\\')
                    q += f" \"{i}\","

            cerrar(q[:-1] + " )")

            return str(tkN)
        
        return False
