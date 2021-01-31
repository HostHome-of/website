import json, random, datetime, requests
import io

def abrir():
    with open("./src/data/users.json", "r") as f:
        usrs = json.load(f)

    return usrs

def cerrar(usrs):
    with open("./src/data/users.json", "w") as f:
        json.dump(usrs, f, indent=4)

class HacerLogin():
    def __init__(self, email, psw):
        self.email = email
        self.psw = psw

    def ejecutar(self):
        usuarios = abrir()

        if self.email in usuarios:
            if usuarios[str(self.email)]["psw"] == self.psw:
                tk = CrearUsuario().tokenizar()
                usuarios[str(self.email)]["cuentas"][str(tk)] = True
                cerrar(usuarios)
                return str(tk)
        return False

class Usuario():

    def __init__(self, tk: str=None):
        self.tk = tk

    def activar(self, mail, codigo):
        usuarios = abrir()
        if int(usuarios[mail]["tokenEntrada"]) == int(codigo): # Bien
            del usuarios[mail]["tokenEntrada"]
            usuarios[mail]["autorizado"] = True
            cerrar(usuarios)
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
            usuarios[str(self.mail)]["psw"] = self.psw 
            usuarios[str(self.mail)]["cuentas"] = {}
            tkN = self.tokenizar()
            usuarios[str(self.mail)]["cuentas"][str(tkN)] = True 
            usuarios[str(self.mail)]["pfp"] = "/src/web/static/pfp/default.png" 
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