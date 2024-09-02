from flask import render_template
from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from models import mod_login
from utils import helpers
from db import db


login_bp = Blueprint('login', __name__)

@login_bp.get("/login")
def login_get():
    if helpers.session_on():
        return redirect(url_for("index.index"))
    else:
        title = "Ingresar"
        body = "Ingresar"
        return render_template("login/index.html", title=title, body=body)
    
@login_bp.post("/login")
def login_post():
    usuario = request.form["usuario"]
    password = request.form["password"]
    result = mod_login.log_user(usuario, password)
    if result:
        session["id"] = result[0]
        session["usuario"] = result[1]
        session["password"] = result[2]
        session["fecha_creacion"] = result[3]
        session["fecha_modificacion"] = result[4]
        session["esta_activo"] = result[5]

        return redirect(url_for("index.index"))
    else:
        flash("usuario o contraseña incorrecta")
        return redirect(url_for("login.login_get"))