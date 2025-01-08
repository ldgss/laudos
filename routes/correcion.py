from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_correccion
from flask import flash
from flask import request
from flask import session
from flask import jsonify


correccion_bp = Blueprint("correccion", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@correccion_bp.get("/correccion")
def correccion():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Correccion"
        section = "Correccion"
        return render_template("correccion/index.html", 
                               title=title, 
                               section=section,
                               productos_arballon = session["productos_arballon"]
                               )
    else:
        return redirect(url_for("login.login_get"))

@correccion_bp.post("/correccion/seleccionar/")
def correccion_seleccionar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # ajax
        data = request.get_json()
        numero_unico = data.get('numero_unico')
        result = mod_correccion.get_para_corregir(numero_unico)
        return jsonify(dict(result))
    else:
        return redirect(url_for("login.login_get"))

@correccion_bp.post("/correccion/actualizar")
def correccion_actualizar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        resultado = mod_correccion.guardar_correccion()
        if resultado:
            flash("El producto se actualizo con exito")
            return redirect(url_for("correccion.correccion"))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("correccion.correccion"))
    else:
        return redirect(url_for("login.login_get"))
    
@correccion_bp.post("/correccion/buscar")
def correccion_buscar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        return redirect(url_for("correccion.correccion_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@correccion_bp.get("/correccion/listado/<terminos_de_busqueda>")
def correccion_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_correccion.get_listado_correccion(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Correccion"
        section = "Correccion"
        return render_template("correccion/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
