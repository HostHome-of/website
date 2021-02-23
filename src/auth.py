import json, random, datetime, requests
import io

import hashlib
import os

salt = open("salt.txt", "r").read().encode()

def abrir():
    with open("./src/data/users.json", "r") as f:
        usrs = json.load(f)

    return usrs

def cerrar(usrs):
    with open("./src/data/users.json", "w") as f:
        json.dump(usrs, f, indent=4)

def abrirInvites():
    with open("./src/data/invites.json", "r") as f:
        links = json.load(f)

    return links

def cerrarInvites(invites):
    with open("./src/data/invites.json", "w") as f:
        json.dump(invites, f, indent=4)

class HacerLogin():
    def __init__(self, email=None, psw=None):
        self.email = email
        self.psw = psw

    def google(self, mail, tk):
        usuarios = abrir()

        if mail in usuarios:
            usuarios[mail]["cuentas"][str(tk)] = True
            usuarios[mail]["google"] = True
            cerrar(usuarios)
            return tk

        return False

    def ejecutar(self, tk=None):
        usuarios = abrir()

        if tk is None:
            if self.email in usuarios:
                if Password(usuarios[str(self.email)]["psw"]).check(self.psw):
                    return usuarios[str(self.email)]
        else:          
            if self.email in usuarios:
                if Password(usuarios[str(self.email)]["psw"]).check(self.psw):
                    usuarios[str(self.email)]["cuentas"][str(tk)] = True
                    cerrar(usuarios)
                    return str(tk)
        return False

class Password():
    def __init__(self, texto: str):
        self.texto = texto

    def crear(self):
        pswNueva = hashlib.pbkdf2_hmac('sha256', self.texto.encode('utf-8'), salt, 100000)
        return pswNueva

    def check(self, psw):
        psw = hashlib.pbkdf2_hmac('sha256', psw.encode('utf-8'), salt, 100000)

        key = self.texto[2:-1]
        psw = str(psw)[2:-1]
        # psw = psw[2:-1]
        
        return key == psw
class Usuario():

    def __init__(self, tk: str=None):
        self.tk = tk

    def cojerInvite(self, mail):
        return abrirInvites()[mail]

    def crearInviteLink(self):
        codigoInicial = ""
        for i in range(16):
            codigoInicial += random.choice("q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m,1,2,3,4,5,6,7,8,9,0".split(","))
        return codigoInicial

    def activar(self, mail, codigo):
        usuarios = abrir()
        if int(usuarios[mail]["tokenEntrada"]) == int(codigo): # Bien
            del usuarios[mail]["tokenEntrada"]
            usuarios[mail]["autorizado"] = True

            cerrar(usuarios)
            invites = abrirInvites()

            while True:
                codigoDeInvite = self.crearInviteLink()
                for codigo_mail in invites:
                    if codigoDeInvite == invites[codigo_mail]["codigo"]:
                        continue
                break

            invites[mail] = {}
            invites[mail]["codigo"] =  codigoDeInvite

            url_main = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]

            invites[mail]["link"]   =  f"{url_main}invites/{codigoDeInvite}"

            cerrarInvites(invites)
            return True
        else: # Mal
            return False

    def cojer(self):
        usuarios = abrir()

        for usr in usuarios:
            for token in usuarios[usr]["cuentas"]:
                if self.tk == token:
                    if usuarios[usr]["cuentas"][token] == True:
                        return usuarios[usr]
        return None

    def eliminar(self):
        usuarios = abrir()

        for usr in usuarios:
            for token in usuarios[usr]["cuentas"]:
                if self.tk == token:
                    usuarios[usr]["cuentas"][self.tk] = False
                    cerrar(usuarios)

    def petar(self, mail):
        usrs = abrir()
        del usrs[mail]
        cerrar(usrs)

    def destruir(self):
        usuarios = abrir()

        for usr in usuarios:
            for token in usuarios[usr]["cuentas"]:
                if self.tk == token:
                    del usuarios[usr]
                    cerrar(usuarios) 
                    return

    def cojer_admins(self):
        data = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()

        return data["admins"]

    def cojer_usuarios(self):
        return abrir()

    def imagen(self, usr, nm):
        mail = Usuario(usr).cojer()["mail"]
        usrs = abrir()
        usrs[mail]["pfp"] = f"/src/web/static/pfp/{nm}"
        cerrar(usrs)

    def actualizar(self, mail, nombre, ap, eddad):
        usuarios = abrir()

        usuarios[str(mail)]["segundoNombre"] = ap
        usuarios[str(mail)]["nombre"] = nombre

        usuarios[str(mail)]["edad"] = eddad

        cerrar(usuarios)

    def actualizarPreferencias(self, mail, uno, dos, tres, cuatro):
        uno     = bool(uno)
        dos     = bool(dos)
        tres    = bool(tres)
        cuatro  = bool(cuatro)

        usuarios = abrir()
        usuarios[str(mail)]["emails"]["uno"]    = uno
        usuarios[str(mail)]["emails"]["dos"]    = dos
        usuarios[str(mail)]["emails"]["tres"]   = tres
        usuarios[str(mail)]["emails"]["cuatro"] = cuatro
        cerrar(usuarios)

class CrearUsuario():
    def __init__(self, nombre: str=None, psw: str=None, mail: str=None):
        self.nombre = nombre
        self.psw = psw
        self.mail = mail

    def google(self, usuario, id, psw: bool=False, tk: str=None): 
        """Si psw es True usuario se cambiara a psw e id a el email del usuario"""
        usuarios = abrir()

        if psw:
            usuarios[id]["psw"]         = str(Password(usuario).crear())
            usuarios[id]["autorizado"]  = True
            usuarios[id]["cuentas"][tk] = True
            cerrar(usuarios)
            return 

        if not usuario["email"] in usuarios:
            email     = usuario["email"]
            pfp       = usuario["picture"]
            nombre    = usuario["given_name"]
            sn        = usuario["family_name"]


            usuarios[email] = {}
            usuarios[email]["mail"] = email
            usuarios[email]["nombre"] = nombre

            usuarios[email]["cuentas"] = {}
            tkN = self.tokenizar()

            usuarios[email]["cuentas"][str(tkN)] = True 
            usuarios[email]["pfp"] = pfp

            now = datetime.datetime.now()
            usuarios[email]["entrada"] = f"{now.day}/{now.month}/{now.year}"

            usuarios[email]["segundoNombre"] = sn
            usuarios[email]["edad"] = ""

            usuarios[email]["autorizado"] = False

            usuarios[email]["emails"]           = {}
            usuarios[email]["emails"]["uno"]    = True
            usuarios[email]["emails"]["dos"]    = False
            usuarios[email]["emails"]["tres"]   = False
            usuarios[email]["emails"]["cuatro"] = True

            usuarios[email]["google"] = True

            cerrar(usuarios)

            return str(tkN)
        else:
            return None

    def check(self, usuarios, token: str):
        for tk in usuarios["cuentas"]:
            if token == tk:
                return False

    def tokenizar(self):
        usuarios = abrir()
        token_valido = False
        token = ""

        while not token_valido:
            token = str(random.randint(10000000, 90000000))
            for usr in usuarios:
                valido = self.check(usuarios[usr], token)
                if not valido:
                    break
            token_valido = True

        return token

    def crear(self):
        usuarios = abrir()

        if not self.mail in usuarios:

            usuarios[str(self.mail)] = {}
            usuarios[str(self.mail)]["mail"] = self.mail
            usuarios[str(self.mail)]["nombre"] = self.nombre
            usuarios[str(self.mail)]["psw"] = str(Password(self.psw).crear())
            usuarios[str(self.mail)]["cuentas"] = {}
            tkN = self.tokenizar()
            usuarios[str(self.mail)]["cuentas"][str(tkN)] = True 
            usuarios[str(self.mail)]["pfp"] = f"/src/web/static/pfp/default_hosthome.png" 
            now = datetime.datetime.now()
            usuarios[str(self.mail)]["entrada"] = f"{now.day}/{now.month}/{now.year}"

            usuarios[str(self.mail)]["segundoNombre"] = "" 
            usuarios[str(self.mail)]["edad"] = "" 

            usuarios[str(self.mail)]["autorizado"] = False
            usuarios[str(self.mail)]["tokenEntrada"] = random.randint(1000, 9000)

            usuarios[str(self.mail)]["emails"]           = {}
            usuarios[str(self.mail)]["emails"]["uno"]    = True
            usuarios[str(self.mail)]["emails"]["dos"]    = False
            usuarios[str(self.mail)]["emails"]["tres"]   = False
            usuarios[str(self.mail)]["emails"]["cuatro"] = True

            cerrar(usuarios)

            return str(tkN)
        
        return False