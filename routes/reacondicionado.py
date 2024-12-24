from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from models import mod_reacondicionado
from flask import flash
from flask import request
from flask import session
from flask import jsonify


reacondicionado_bp = Blueprint("reacondicionado", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@reacondicionado_bp.get("/reacondicionado")
def reacondicionado():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Reacondicionado"
        section = "Reacondicionado"
        return render_template("reacondicionado/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@reacondicionado_bp.get("/reacondicionado/agregar")
def reacondicionado_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        proximo_id = mod_reacondicionado.get_ultimo_id()
        title = "Reacondicionado"
        section = "Reacondicionado"
        return render_template("reacondicionado/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@reacondicionado_bp.post("/reacondicionado/agregar")
def reacondicionado_agregar_post():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        barcode = mod_reacondicionado.guardar_reacondicionado()
        if barcode:
            return redirect(url_for("reacondicionado.reacondicionado_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("reacondicionado.reacondicionado_agregar"))
    else:
        return redirect(url_for("login.login_get"))

@reacondicionado_bp.get("/reacondicionado/buscart1t2t/<numero_unico>")
def reacondicionado_buscart1t2(numero_unico):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        reacondicionado = mod_reacondicionado.get_reacondicionado(numero_unico)
        return jsonify(reacondicionado)
    else:
        return redirect(url_for("login.login_get"))

@reacondicionado_bp.get("/reacondicionado/imprimir/<numero_unico>")
def reacondicionado_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        reacondicionado = mod_reacondicionado.get_reacondicionado(numero_unico)
        title = "Reacondicionado"
        section = "Reacondicionado"
        return render_template("reacondicionado/imprimir.html", 
                               title=title, section=section, 
                               reacondicionado=reacondicionado)
    else:
        return redirect(url_for("login.login_get"))
    
@reacondicionado_bp.post("/reacondicionado/buscar")
def reacondicionado_buscar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        return redirect(url_for("reacondicionado.reacondicionado_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@reacondicionado_bp.get("/reacondicionado/listado/<terminos_de_busqueda>")
def reacondicionado_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_reacondicionado.get_listado_reacondicionado(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Reacondicionado"
        section = "Reacondicionado"
        return render_template("reacondicionado/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
