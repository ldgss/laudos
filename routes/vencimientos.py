from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_vencimientos
from flask import flash
from flask import request
from flask import session


vencimientos_bp = Blueprint("vencimientos", __name__)
# cantidad para paginacion
resultados_por_pagina = 20
title = "Meses de vencimiento de los productos por clase"

@vencimientos_bp.get("/vencimientos")
def vencimientos():
    if helpers.session_on():
        section = "Listado de vencimientos"
        vencimientos = mod_vencimientos.get_vencimientos()
        return render_template("vencimientos/index.html", 
                                vencimientos=vencimientos,
                                title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))    
