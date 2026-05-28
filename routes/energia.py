from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_energia
from flask import flash
from flask import request
from flask import session
from flask import jsonify


energia_bp = Blueprint("energia", __name__)
# cantidad para paginacion
resultados_por_pagina = 20
title = "Energía"

@energia_bp.get("/energia")
def energia():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        section = "Energía"
        return render_template("energia/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.get("/energia/agregar")
def energia_agregar():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        section = "Agregar medición de energía"
        return render_template("energia/agregar.html", 
                               title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.post("/energia/agregar")
def energia_agregar_post():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        result = mod_energia.guardar_energia()
        if result:
            return redirect(url_for("energia.energia_imprimir", id_medicion_energia=result))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("energia.energia_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.post("/energia/anular")
def energia_anular_post():
    if helpers.session_on() and helpers.authorized_to("mantenimiento") and not helpers.authorized_to_action("limitado"):
        referer = request.headers.get('Referer', '/')
        result = mod_energia.anular_energia()
        if result:
            return redirect(referer)
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(referer)
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.get("/energia/imprimir/<id_medicion_energia>")
def energia_imprimir(id_medicion_energia):
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        energia = mod_energia.get_energia(id_medicion_energia)
        section = "Visulizando registro de energía"
        return render_template("energia/imprimir.html", 
                               title=title, section=section, 
                               energia=energia)
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.post("/energia/buscar")
def energia_buscar():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        return redirect(url_for("energia.energia_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.get("/energia/listado/<terminos_de_busqueda>")
def energia_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_energia.get_listado_energia(terminos_de_busqueda, resultados_por_pagina, offset)
        section = "Listado de mediciones de energía"
        return render_template("energia/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))

@energia_bp.get("/energia/estadisticas")
def energia_estadisticas():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        section = "Estadísticas de energía"
        return render_template(
                "energia/estadisticas.html", 
                title=title, 
                section=section,
            )
    else:
        return redirect(url_for("login.login_get"))

@energia_bp.post("/energia/estadisticas/filtrar")
def energia_filtrar():
    print(f"filtro: {request.form}")
    estadisticas = mod_energia.get_estadisticas()
    print(f"resultados: {estadisticas}")
    if estadisticas and len(estadisticas) > 0:
        return jsonify(estadisticas), 200
    else:
        return jsonify([]), 200