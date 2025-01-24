from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_insumos
from flask import flash
from flask import request
from flask import session
from flask import jsonify

insumos_bp = Blueprint("insumos", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@insumos_bp.get("/insumos")
def insumos():
    if helpers.session_on() and helpers.authorized_to("insumo"):
        title = "Insumos"
        section = "Insumos"
        return render_template("insumos/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@insumos_bp.get("/insumos/agregar")
def insumos_agregar():
    if helpers.session_on() and helpers.authorized_to("insumo"):
        title = "Insumos"
        section = "Insumos"
        return render_template("insumos/agregar.html", 
                               title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))

@insumos_bp.post("/insumos/buscar_insumo")
def insumos_buscar_insumo():
    if helpers.session_on() and helpers.authorized_to("insumo"):
        result = mod_insumos.get_buscar_insumo_para_guardar()
        return jsonify(result)
    else:
        return redirect(url_for("login.login_get"))

@insumos_bp.post("/insumos/agregar")
def insumos_agregar_post():
    if helpers.session_on() and helpers.authorized_to("insumo"):
        result = mod_insumos.guardar_insumos()
        if result:
            flash("Insumo guardado con éxito")
            return redirect(url_for("insumos.insumos_agregar"))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("insumos.insumos_agregar"))
    else:
        return redirect(url_for("login.login_get"))

@insumos_bp.post("/insumos/buscar")
def insumos_buscar():
    if helpers.session_on() and helpers.authorized_to("insumo"):
        return redirect(url_for("insumos.insumos_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@insumos_bp.get("/insumos/listado/<terminos_de_busqueda>")
def insumos_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("insumo"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_insumos.get_listado_insumos(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Insumos"
        section = "Insumos"
        return render_template("insumos/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
    
@insumos_bp.post("/insumos/anular")
def insumos_anular_post():
    if helpers.session_on() and helpers.authorized_to("insumo"):
        referer = request.headers.get('Referer', '/')
        result = mod_insumos.anular_insumos()
        if result:
            return redirect(referer)
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(referer)
    else:
        return redirect(url_for("login.login_get"))
