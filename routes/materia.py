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

materia_bp = Blueprint("materia", __name__)
# cantidad para paginacion
resultados_por_pagina = 10

@materia_bp.get("/materia")
def materia():
    if helpers.session_on() and helpers.authorized_to("hojalata"):
        title = "materia"
        section = "materia"
        return render_template("materia/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))