from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_hys
from flask import flash
from flask import request
from flask import session


hys_bp = Blueprint("hys", __name__)
# cantidad para paginacion
resultados_por_pagina = 20
title = "Higiene y seguridad"

@hys_bp.get("/hys")
def hys():
    if helpers.session_on() and helpers.authorized_to("hys"):
        section = "Higiene y seguridad"
        return render_template("hys/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.get("/hys/agregar")
def hys_agregar():
    if helpers.session_on() and helpers.authorized_to("hys"):
        section = "Agregar incidente"
        return render_template("hys/agregar.html", 
                               title=title, section=section, 
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.post("/hys/agregar")
def hys_agregar_post():
    if helpers.session_on() and helpers.authorized_to("hys"):
        result = mod_hys.guardar_hys()
        if result:
            return redirect(url_for("hys.hys_imprimir", id_hys=result))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("hys.hys_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.get("/hys/imprimir/<id_hys>")
def hys_imprimir(id_hys):
    if helpers.session_on() and helpers.authorized_to("hys"):
        hys = mod_hys.get_hys(id_hys)
        section = "Visualizando incidente de higiene y seguridad"
        return render_template("hys/imprimir.html", 
                               title=title, section=section, 
                               hys=hys)
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.post("/hys/buscar")
def hys_buscar():
    if helpers.session_on() and helpers.authorized_to("hys"):
        return redirect(url_for("hys.hys_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.get("/hys/listado/<terminos_de_busqueda>")
def hys_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("hys"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_hys.get_listado_hys(terminos_de_busqueda, resultados_por_pagina, offset)
        section = "Listado de incidentes de higiene y seguridad"
        return render_template("hys/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.post("/hys/anular")
def hys_anular_post():
    if helpers.session_on() and helpers.authorized_to("hys") and not helpers.authorized_to_action("limitado"):
        referer = request.headers.get('Referer', '/')
        result = mod_hys.anular_hys()
        if result:
            return redirect(referer)
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(referer)
    else:
        return redirect(url_for("login.login_get"))    
