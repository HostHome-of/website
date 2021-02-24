from dotenv import load_dotenv
from flask import Flask
from os import environ as env

from flask_dance.contrib.github import make_github_blueprint, github

import os

# API | Key
api_key = env["API_KEY"]

# App
app = Flask(__name__, static_url_path="/src/web/static")
app.secret_key = api_key

# Config
load_dotenv()
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

GOOGLE_CLIENT_ID          = env["GOOGLE_ID"]
GOOGLE_CLIENT_SECRET      = env["GOOGLE_SECRETE"]

GITHUB_CLIENT_ID          = env["GITHUB_ID"]
GITHUB_CLIENT_SECRETE     = env["GITHUB_KEY"]

# Github init
github_blueprint = make_github_blueprint(client_id=GITHUB_CLIENT_ID, client_secret=GITHUB_CLIENT_SECRETE, redirect_to="main_page.quitarWindow")

# Blueprints
from src.routes import main_page
from src.serviceworker import serviceworker

app.register_blueprint(github_blueprint, url_prefix="/github_login")
app.register_blueprint(main_page)
app.register_blueprint(serviceworker)


# ================================== INIT
def run():
    app.run()
