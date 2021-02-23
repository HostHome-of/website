from flask import Blueprint, render_template, abort, redirect, url_for, request
from src.app import app

serviceworker = Blueprint('serviceworker', __name__)

@serviceworker.route('/service-worker.js')
@serviceworker.route('/sw.js')
def sw():
    return app.send_static_file('sw.js'), 200, {'Content-Type': 'text/javascript'}

@serviceworker.route("/src/web/static/images/favicon.png")
@serviceworker.route("/favicon.ico")
def iconos():
    return app.send_static_file('images/favicon.png'), 200, {'Content-Type': 'image/png'}