import json, random, datetime

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

    def __init__(self, tk: str):
        self.tk = tk

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
            usuarios[str(self.mail)]["cuentas"] = [] 
            tkN = self.tokenizar()
            usuarios[str(self.mail)]["cuentas"].append(str(tkN)) 
            usuarios[str(self.mail)]["abierto"] = True 
            now = datetime.datetime.now()
            usuarios[str(self.mail)]["entrada"] = f"{now.day}/{now.month}/{now.year}" 

            cerrar(usuarios)
            return str(tkN)
        
        return False