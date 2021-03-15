from functools import wraps
from flask import request, flash, redirect, url_for

from src.auth import Usuario

import requests

class Utils():
    def __init__(self):
        self._config                = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()
        self.docs                   = self._config["docs"]
        self.main_url               = self._config["url"]

        self.google_url_login       = f"{self.main_url}authorize/google/login" 
        self.google_url_register    = f"{self.main_url}authorize/google/register"


    def get_repositories(self, url, usr):
        result = {}
        r = requests.get(url=url)
        if 'next' in r.links:
            self.get_repositories(r.links['next']['url'], usr)

        for repository in r.json():
            try:
                result[repository.get('name')] = {}
                result[repository.get('name')]["len"] = repository.get('language')
                result[repository.get('name')]["branch"] = repository.get("default_branch")
                result[repository.get('name')]["url"] = repository.get("html_url")
                result[repository.get('name')]["usr"] = usr
                
            except:
                pass

        return result    

    def login_required(self, function_to_protect):
        @wraps(function_to_protect)
        def wrapper(*args, **kwargs):
            user_id = request.cookies.get('user_id')
            if user_id:
                user = Usuario(user_id).cojer()
                if not user:
                    flash("Porfavor haz login")
                    return redirect(url_for('main_page.login'))
                if user:
                    if not user.get("autorizado"):
                        Usuario(user_id).petar()
                        return redirect(url_for('main_page.login'))
                    return function_to_protect(*args, **kwargs)
                else:
                    return redirect(url_for('main_page.login'))
            else:
                flash("Porfavor haz login")
                return redirect(url_for('main_page.login'))
        return wrapper 

    def already_logedin(self, function_to_protect):
        @wraps(function_to_protect)
        def wrapper(*args, **kwargs):
            user_id = request.cookies.get('user_id')
            user = Usuario(user_id).cojer()
            if user:
                return redirect("/")
            else:
                return function_to_protect(*args, **kwargs)
        return wrapper 

    def check_usuario(self):
        id = request.cookies.get('user_id')
        if id:
            usr = Usuario(id).cojer()
            if usr is None:
                return None
            if not usr["autorizado"]:
                Usuario(id).petar()
                return None
            return usr
        return None