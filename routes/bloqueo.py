from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_bloqueo
from flask import flash
from flask import request
from flask import session


bloqueo_bp = Blueprint("bloqueo", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@bloqueo_bp.get("/bloqueo")
def bloqueo():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        title = "bloqueo"
        section = "bloqueo"
        return render_template("bloqueo/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueo_bp.post("/bloqueo/cambiar")
def bloqueo_cambiar_post():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        referer = request.headers.get('Referer', '/')
        cambio = mod_bloqueo.cambiar_bloqueo()
        title = "bloqueo"
        section = "bloqueo"
        if cambio:
            flash("Los cambios se han guardado correctamente")
            return redirect(referer)
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(referer)

    else:
        return redirect(url_for("login.login_get"))
    
@bloqueo_bp.get("/bloqueo/imprimir/<numero_unico>")
def bloqueo_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        bloqueo = mod_bloqueo.get_bloqueo(numero_unico)
        title = "bloqueo"
        section = "bloqueo"
        return render_template("bloqueo/imprimir.html", 
                               title=title, section=section, 
                               bloqueo=bloqueo)
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueo_bp.post("/bloqueo/buscar")
def bloqueo_buscar():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        return redirect(url_for("bloqueo.bloqueo_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueo_bp.get("/bloqueo/listado/<terminos_de_busqueda>")
def bloqueo_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        motivos = mod_bloqueo.listar_motivo_bloqueo()
        resultado = mod_bloqueo.get_listado_bloqueo(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "bloqueo"
        section = "bloqueo"
        return render_template("bloqueo/listado.html", 
                               max=max,
                               min=min,
                               motivos=motivos,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
