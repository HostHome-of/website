
import random
import json
import git, os

class Projecto():

    def __init__(self):
        self.nums = "0123456789"
        self.letras = "qwertyuiopasdfghjklzxcvbnm"

    def abrir(self):
        with open("./src/data/projectos.json", "r") as f:
            pr = json.load(f)

        return pr

    def cerrar(self, pr):
        with open("./src/data/projectos.json", "w") as f:
            json.dump(pr, f, indent=4)

    def cojer(self, id):
        data = self.abrir()
        if id in data:
            return data[id]
        return None

    def crear(self, nombre: str, repo: str):
        self.token = ''.join(random.choice(self.letras + str(self.nums)) for i in range(20))
        prs = self.abrir()
        if not self.token in str(prs):

            open(f"./src/data/logs/{self.token}.log", "a")
            os.mkdir(f"./src/data/projectos/{self.token}")

            git.Git(f"./src/data/projectos/{self.token}").clone(repo)

            prs[self.token] = {}
            prs[self.token]["nombre"] = nombre
            prs[self.token]["repo"] = repo
            prs[self.token]["parado"] = False
            self.cerrar(prs)

            return self.token

        return self.crear()
