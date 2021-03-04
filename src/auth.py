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

    def google(self, mail):
        usuarios = abrir()

        for usr in usuarios:
            usr_mail = usuarios[usr]["mail"]

            if mail == usr_mail:
                usuarios[usr]["google"] = True
                cerrar(usuarios)
                return usr

        return False

    def ejecutar(self, tk=None):
        usuarios = abrir()

        for usr in usuarios:
            if usuarios[usr]["mail"] == self.email:
                self.email = usr
   
        if self.email in usuarios:
            if Password(usuarios[str(self.email)]["psw"]).check(self.psw):
                return str(self.email)

        return False

    def tokenizar(self):
        usuarios = abrir()
        token_valido = False
        token = ""

        while not token_valido:
            token = str(random.randint(10000000, 90000000))
            for usr in usuarios:
                valido = CrearUsuario().check(usuarios[usr], token)
                if not valido:
                    break
            token_valido = True

        return token

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

    def cojerInvite(self, tk):
        return abrirInvites()[tk]

    def crearInviteLink(self):
        codigoInicial = ""
        for i in range(16):
            codigoInicial += random.choice("q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m,1,2,3,4,5,6,7,8,9,0".split(","))
        return codigoInicial

    def activar(self, tk, codigo):
        usuarios = abrir()
        if int(usuarios[tk]["tokenEntrada"]) == int(codigo): # Bien
            del usuarios[tk]["tokenEntrada"]
            usuarios[tk]["autorizado"] = True

            cerrar(usuarios)
            invites = abrirInvites()

            while True:
                codigoDeInvite = Usuario().crearInviteLink()
                for codigo_mail in invites:
                    if codigoDeInvite == invites[codigo_mail]["codigo"]:
                        continue
                break

            invites[tk] = {}
            invites[tk]["codigo"] =  codigoDeInvite

            url_main = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]

            invites[tk]["link"]   =  f"{url_main}invites/{codigoDeInvite}"

            cerrarInvites(invites)
            return True
        else: # Mal
            return False

    def cojer(self):
        usuarios = abrir()
        if self.tk in usuarios:
            return usuarios[str(self.tk)]
        return None

    def petar(self, tk):
        usrs = abrir()
        del usrs[tk]
        cerrar(usrs)

    def destruir(self):
        usuarios = abrir()
        invites = abrirInvites()

        if self.tk in usuarios:
            del usuarios[self.tk]
            del invites[self.tk]

        cerrarInvites(invites)
        cerrar(usuarios) 

    def cojer_admins(self):
        data = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()

        return data["admins"]

    def cojer_usuarios(self):
        return abrir()

    def imagen(self, usr, nm):
        mail = usr
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

    def google(self, usuario, id, psw: bool=False): 
        """Si psw es True usuario se cambiara a psw e id a el email del usuario"""
        usuarios = abrir()

        if psw:

            usuarios[id]["psw"]         = str(Password(usuario).crear())
            usuarios[id]["autorizado"]  = True

            invites = abrirInvites()

            while True:
                codigoDeInvite = Usuario().crearInviteLink()
                for codigo_mail in invites:
                    if codigoDeInvite == invites[codigo_mail]["codigo"]:
                        continue
                break

            invites[id] = {}
            invites[id]["codigo"] =  codigoDeInvite

            url_main = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]

            invites[id]["link"]   =  f"{url_main}invites/{codigoDeInvite}"

            cerrarInvites(invites)

            cerrar(usuarios)
            return id

        USUARIO_EXISTENTE = False

        for usr in usuarios:
            if usuario["email"] == usuarios[usr]["mail"]:
                USUARIO_EXISTENTE = True

        if not USUARIO_EXISTENTE:
            email     = usuario["email"]
            pfp       = usuario["picture"]
            nombre    = usuario["given_name"]
            
            try:
                sn    = usuario["family_name"]
            except KeyError:
                sn    = ""


            tkN = self.tokenizar()

            usuarios[tkN] = {}
            usuarios[tkN]["mail"] = email
            usuarios[tkN]["nombre"] = nombre

            usuarios[tkN]["pfp"] = pfp

            now = datetime.datetime.now()
            usuarios[tkN]["entrada"] = f"{now.day}/{now.month}/{now.year}"

            usuarios[tkN]["segundoNombre"] = sn
            usuarios[tkN]["edad"] = ""

            usuarios[tkN]["autorizado"] = False

            usuarios[tkN]["emails"]           = {}
            usuarios[tkN]["emails"]["uno"]    = True
            usuarios[tkN]["emails"]["dos"]    = False
            usuarios[tkN]["emails"]["tres"]   = False
            usuarios[tkN]["emails"]["cuatro"] = True

            usuarios[tkN]["google"] = True

            cerrar(usuarios)

            return str(tkN)
        else:
            return None

    def check(self, usuarios, token: str):
        if token in abrir():
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

            tkN = self.tokenizar()
            usuarios[str(tkN)] = {}
            usuarios[str(tkN)]["mail"] = self.mail
            usuarios[str(tkN)]["nombre"] = self.nombre
            usuarios[str(tkN)]["psw"] = str(Password(self.psw).crear())
            
            usuarios[str(tkN)]["pfp"] = f"/src/web/static/pfp/default_hosthome.png" 
            now = datetime.datetime.now()
            usuarios[str(tkN)]["entrada"] = f"{now.day}/{now.month}/{now.year}"

            usuarios[str(tkN)]["segundoNombre"] = "" 
            usuarios[str(tkN)]["edad"] = "" 

            usuarios[str(tkN)]["autorizado"] = False
            usuarios[str(tkN)]["tokenEntrada"] = random.randint(1000, 9000)

            usuarios[str(tkN)]["emails"]           = {}
            usuarios[str(tkN)]["emails"]["uno"]    = True
            usuarios[str(tkN)]["emails"]["dos"]    = False
            usuarios[str(tkN)]["emails"]["tres"]   = False
            usuarios[str(tkN)]["emails"]["cuatro"] = True

            cerrar(usuarios)

            return str(tkN)
        
        return False
