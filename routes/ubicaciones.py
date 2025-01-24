from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_ubicaciones
from flask import flash
from flask import request
from flask import session
from flask import jsonify


ubicaciones_bp = Blueprint("ubicaciones", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@ubicaciones_bp.get("/ubicaciones")
def ubicaciones():
    if helpers.session_on() and helpers.authorized_to("ubicacion"):
        title = "Ubicaciones"
        section = "Ubicaciones"
        return render_template("ubicaciones/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@ubicaciones_bp.get("/ubicaciones/agregar")
def ubicaciones_agregar():
    if helpers.session_on() and helpers.authorized_to("ubicacion"):
        ubicacion_nombre = mod_ubicaciones.get_ubicacion_nombre()
        title = "Ubicaciones"
        section = "Ubicaciones"
        return render_template("ubicaciones/agregar.html", 
                               title=title, section=section, 
                               ubicacion_nombre=ubicacion_nombre,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@ubicaciones_bp.post("/ubicaciones/agregar")
def ubicaciones_agregar_post():
    if helpers.session_on() and helpers.authorized_to("ubicacion"):
        barcode = mod_ubicaciones.guardar_ubicaciones()
        if barcode:
            return redirect(url_for("ubicaciones.ubicaciones_track", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("ubicaciones.ubicaciones_agregar"))
    else:
        return redirect(url_for("login.login_get"))

@ubicaciones_bp.get("/ubicaciones/track/<numero_unico>")
def ubicaciones_track(numero_unico):
    if helpers.session_on() and helpers.authorized_to("ubicacion"):
        ubicaciones = mod_ubicaciones.get_ubicaciones(numero_unico)
        title = "Ubicaciones"
        section = "Ubicaciones"
        return render_template("ubicaciones/track.html", 
                               title=title, section=section, 
                               numero_unico=numero_unico,
                               ubicaciones=ubicaciones)
    else:
        return redirect(url_for("login.login_get"))
    
@ubicaciones_bp.post("/ubicaciones/buscar")
def ubicaciones_buscar():
    if helpers.session_on() and helpers.authorized_to("ubicacion"):
        return redirect(url_for("ubicaciones.ubicaciones_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@ubicaciones_bp.get("/ubicaciones/listado/<terminos_de_busqueda>")
def ubicaciones_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("ubicacion"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_ubicaciones.get_listado_ubicaciones(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Ubicaciones"
        section = "Ubicaciones"
        return render_template("ubicaciones/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))

@ubicaciones_bp.post("/ubicaciones/anular")
def ubicaciones_anular_post():
    if helpers.session_on() and helpers.authorized_to("ubicacion"):
        result = mod_ubicaciones.anular_ubicaciones()
        if result:
            return redirect(url_for("ubicaciones.ubicaciones_track", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("ubicaciones.ubicaciones_track", numero_unico=request.form["numero_unico"]))

    else:
        return redirect(url_for("login.login_get"))