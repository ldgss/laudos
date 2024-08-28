from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import session

app = Flask(__name__)

@app.route("/")
def index():
    title = "Laudos Solvencia S.A"
    body = "Bienvenidos!"
    return render_template("index.html", title=title, body=body)

@app.route("/login")
def login():
    title = "Ingresar"
    body = "Ingresar"
    return render_template("login/index.html", title=title, body=body)

@app.route("/mercaderia")
def mercaderia():
    title = "Mercaderia"
    body = "Mercaderia"
    return render_template("mercaderia/index.html", title=title, body=body)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("pagina_no_encontrada.html"), 404
