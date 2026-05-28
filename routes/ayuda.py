from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint


ayuda_bp = Blueprint("ayuda", __name__)
# cantidad para paginacion
resultados_por_pagina = 20
title = "Ayuda"

@ayuda_bp.get("/ayuda")
def ayuda():
    if helpers.session_on():
        section = "Ayuda"
        return render_template("ayuda/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))