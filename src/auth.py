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
                usuarios[str(self.email)]["abierto"] = True
                tk = CrearUsuario().tokenizar()
                usuarios[str(self.email)]["cuentas"].append(tk)
                cerrar(usuarios)
                return str(tk)
        return False

class Usuario():

    def __init__(self, tk: str=None):
        self.tk = tk

    def activar(self, mail, codigo):
        usuarios = abrir()
        print(usuarios[mail]["tokenEntrada"])
        print(codigo)
        if int(usuarios[mail]["tokenEntrada"]) == int(codigo): # Bien
            del usuarios[mail]["tokenEntrada"]
            usuarios[mail]["autorizado"] = True
            cerrar(usuarios)
            return True
        else: # Mal
            return False

    def destruir(self, mail):
        usuarios = abrir()
        del usuarios[mail]
        cerrar(usuarios)

    def cojer(self):
        usuarios = abrir()

        for usr in usuarios:
            for token in usuarios[usr]["cuentas"]:
                if self.tk == token:
                    return usuarios[usr]
        return None

    def eliminar(self):
        usuarios = abrir()

        for usr in usuarios:
            for token in usuarios[usr]["cuentas"]:
                if self.tk == token:
                    usuarios[usr]["abierto"] = False
                    # del usuarios[usr]["cuentas"][self.tk]
                    cerrar(usuarios)

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

    def actualizar(self, mail, nombre, pm, ap, direccion, ci, pa, co, bio):
        usuarios = abrir()

        usuarios[str(mail)]["nombre"] = nombre

        usuarios[str(mail)]["primerNombre"] = pm
        usuarios[str(mail)]["segundoNombre"] = ap

        usuarios[str(mail)]["direccion"] = direccion
        usuarios[str(mail)]["ciudad"] = ci 
        usuarios[str(mail)]["pais"] = pa
        usuarios[str(mail)]["codigoPostal"] = co

        usuarios[str(mail)]["info"] = bio

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

    def autorizar(self):
        pass


    def crear(self):
        usuarios = abrir()

        if not self.mail in usuarios:

            usuarios[str(self.mail)] = {}
            usuarios[str(self.mail)]["mail"] = self.mail
            usuarios[str(self.mail)]["nombre"] = self.nombre
            usuarios[str(self.mail)]["psw"] = self.psw 
            usuarios[str(self.mail)]["cuentas"] = [] 
            tkN = self.tokenizar()
            usuarios[str(self.mail)]["cuentas"].append(str(tkN)) 
            usuarios[str(self.mail)]["pfp"] = "/src/web/static/pfp/default.png" 
            now = datetime.datetime.now()
            usuarios[str(self.mail)]["entrada"] = f"{now.day}/{now.month}/{now.year}"
            usuarios[str(self.mail)]["abierto"] = True 

            usuarios[str(self.mail)]["primerNombre"] = "" 
            usuarios[str(self.mail)]["segundoNombre"] = "" 

            usuarios[str(self.mail)]["direccion"] = "" 
            usuarios[str(self.mail)]["ciudad"] = "" 
            usuarios[str(self.mail)]["pais"] = "" 
            usuarios[str(self.mail)]["codigoPostal"] = "" 

            usuarios[str(self.mail)]["info"] = ""

            usuarios[str(self.mail)]["autorizado"] = False
            usuarios[str(self.mail)]["tokenEntrada"] = random.randint(1000, 9000)

            cerrar(usuarios)
            return str(tkN)
        
        return False