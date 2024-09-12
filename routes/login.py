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
import pytz
from datetime import datetime


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
        session.update(result)
        session["fecha_creacion"] = helpers.convertir_a_local(session["fecha_creacion"])
        session["fecha_modificacion"] = helpers.convertir_a_local(session["fecha_creacion"])
        session["fecha_registro"] = helpers.convertir_a_local(session["fecha_creacion"])
        return redirect(url_for("index.index"))
    else:
        flash("usuario o contraseña incorrecta")
        return redirect(url_for("login.login_get"))
    
@login_bp.get("/logout")
def logout(): 
    session.clear()
    return redirect(url_for("login.login_get"))