from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_motivosdebloqueo
from flask import flash
from flask import request
from flask import session


motivosdebloqueo_bp = Blueprint("motivosdebloqueo", __name__)
# cantidad para paginacion
resultados_por_pagina = 20
title = "Motivos de bloqueo"

@motivosdebloqueo_bp.get("/motivosdebloqueo")
def motivosdebloqueo():
    if helpers.session_on():
        section = "Listado de motivos de bloqueo"
        motivosdebloqueo = mod_motivosdebloqueo.get_motivosdebloqueo()
        return render_template("motivosdebloqueo/index.html", 
                                motivosdebloqueo=motivosdebloqueo,
                                title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))    
