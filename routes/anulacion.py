from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_anulacion
from flask import flash
from flask import request
from flask import session


anulacion_bp = Blueprint("anulacion", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@anulacion_bp.get("/anulacion")
def anulacion():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Anulacion"
        section = "Anulacion"
        return render_template("anulacion/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@anulacion_bp.post("/anulacion/agregar")
def anulacion_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        
        resultado = mod_anulacion.guardar_anulacion()
        if resultado:
            flash("El producto se anulo con exito")
            return redirect(url_for("anulacion.anulacion"))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("anulacion.anulacion_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@anulacion_bp.post("/anulacion/buscar")
def anulacion_buscar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        return redirect(url_for("anulacion.anulacion_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@anulacion_bp.get("/anulacion/listado/<terminos_de_busqueda>")
def anulacion_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
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
