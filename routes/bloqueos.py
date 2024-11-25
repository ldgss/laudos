from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_hojalata
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session
from datetime import datetime
from dateutil.relativedelta import relativedelta


bloqueos_bp = Blueprint("bloqueos", __name__)

@bloqueos_bp.get("/bloqueos")
def bloqueos():
    if helpers.session_on() and helpers.authorized_to("hojalata"):
        title = "hojalata"
        section = "hojalata"
        return render_template("bloqueados/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
# @bloqueos_bp.route("/bloqueos/agregar")
# def agregar():
#     if helpers.session_on() and helpers.authorized_to("bloqueo"):
#         title = "AGRAGAR BLOQUEO"
#         body = "agregar"
#         return render_template("bloqueados/agregar.html", title=title, body=body)
#     else:
#         return redirect(url_for("login.login_get"))
    
# @bloqueos_bp.route("/bloqueos/editar")
# def editar():
#     if helpers.session_on() and helpers.authorized_to("bloqueo"):
#         title = "MODIFICACION"
#         body = "editar"
#         return render_template("bloqueados/editar.html", title=title, body=body)
#     else:
#         return redirect(url_for("login.login_get"))