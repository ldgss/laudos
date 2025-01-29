from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_despacho
from flask import flash
from flask import request
from flask import session


despacho_bp = Blueprint("despacho", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@despacho_bp.get("/despacho")
def despacho():
    if helpers.session_on() and helpers.authorized_to("despacho"):
        title = "despacho"
        section = "despacho"
        return render_template("despacho/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@despacho_bp.get("/despacho/agregar")
def despacho_agregar():
    if helpers.session_on() and helpers.authorized_to("despacho"):
        fleteros = mod_despacho.get_fleteros()
        title = "despacho"
        section = "despacho"
        return render_template("despacho/agregar.html", 
                               title=title, section=section, 
                               fleteros = fleteros
                               )
    else:
        return redirect(url_for("login.login_get"))
    
@despacho_bp.post("/despacho/agregar")
def despacho_agregar_post():
    if helpers.session_on() and helpers.authorized_to("despacho"):
        despacho = mod_despacho.guardar_despacho()
        title = "despacho"
        section = "despacho"
        if despacho:
            flash("Despacho agregado con éxito.")
            return redirect(url_for("despacho.despacho_agregar"))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("despacho.despacho_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@despacho_bp.post("/despacho/buscar")
def despacho_buscar():
    if helpers.session_on() and helpers.authorized_to("despacho"):
        return redirect(url_for("despacho.despacho_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@despacho_bp.get("/despacho/listado/<terminos_de_busqueda>")
def despacho_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("despacho"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        resultado = mod_despacho.get_listado_despacho(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "despacho"
        section = "despacho"
        return render_template("despacho/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
    
@despacho_bp.post("/despacho/anular")
def despacho_anular_post():
    if helpers.session_on() and helpers.authorized_to("insumo"):
        referer = request.headers.get('Referer', '/')
        result = mod_despacho.anular_despacho()
        if result:
            return redirect(referer)
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(referer)
    else:
        return redirect(url_for("login.login_get"))
