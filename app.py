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
    return render_template("index.html", body="index content", title="index title")

@app.route("/login")
def login():
    return render_template("login/index.html", body="login content", title="login title")

@app.route("/mercaderia")
def mercaderia():
    return render_template("mercaderia/index.html", body="mercaderia content", title="mercaderia title")
