from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_anulacion
from flask import flash
from flask import request
from flask import session
from flask import jsonify


anulacion_bp = Blueprint("anulacion", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@anulacion_bp.get("/anulacion")
def anulacion():
    if helpers.session_on() and helpers.authorized_to("mercaderia") and helpers.authorized_to_submodule("anulacion"):
        title = "Anulacion"
        section = "Anulacion"
        return render_template("anulacion/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@anulacion_bp.post("/anulacion/agregar")
def anulacion_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia") and helpers.authorized_to_submodule("anulacion"):
        
        resultado = mod_anulacion.guardar_anulacion()
        # un mensaje largo en flash se ignora
        if resultado:
            flash("Anulacion guardada con exito")
            return redirect(url_for("anulacion.anulacion"))
        else:
            flash("Se ha producido un error en la anulacion")
            return redirect(url_for("anulacion.anulacion"))
    else:
        return redirect(url_for("login.login_get"))
    
@anulacion_bp.post("/anulacion/detalle_t2")
def detalle_t2():
    if helpers.session_on() and helpers.authorized_to("mercaderia") and helpers.authorized_to_submodule("anulacion"):
        resultado = mod_anulacion.detalle_t2()
        if resultado:
            return resultado
        else:
            return jsonify({'error': 'Pallet no encontrado'}), 404
    else:
        return redirect(url_for("login.login_get"))

@anulacion_bp.post("/anulacion/buscar")
def anulacion_buscar():
    if helpers.session_on() and helpers.authorized_to("mercaderia") and helpers.authorized_to_submodule("anulacion"):
        return redirect(url_for("anulacion.anulacion_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@anulacion_bp.get("/anulacion/listado/<terminos_de_busqueda>")
def anulacion_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mercaderia") and helpers.authorized_to_submodule("anulacion"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_anulacion.get_listado_anulacion(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Anulacion"
        section = "Anulacion"
        return render_template("anulacion/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
