from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from models import mod_intervenciones
from flask import flash
from flask import request
import json


intervenciones_bp = Blueprint("intervenciones", __name__)
# cantidad para paginacion
resultados_por_pagina = 20
title = 'Intervencion de línea'

@intervenciones_bp.get("/intervenciones")
def intervenciones():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        section = "Intervención de línea"
        return render_template("intervenciones/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@intervenciones_bp.get("/intervenciones/agregar")
def intervenciones_agregar():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        lineas_mantenimiento = mod_intervenciones.get_lineas_mantenimiento()
        tipo_de_fallo = mod_intervenciones.get_tipo_de_fallo()
        section = "Agregar intervención de línea"
        return render_template("intervenciones/agregar.html", 
                               title=title, section=section, 
                               lineas_mantenimiento = lineas_mantenimiento,
                               tipo_de_fallo = tipo_de_fallo
                               )
    else:
        return redirect(url_for("login.login_get"))
    
@intervenciones_bp.post("/intervenciones/agregar")
def intervenciones_agregar_post():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        files = request.files.getlist("imagenes")
        print(f'request.url = {request.url}')
        if len(files) > 2:
            flash("Máximo 2 imágenes permitidas")
            return redirect(request.url)
        result = mod_intervenciones.guardar_intervencion()
        if result:
            return redirect(url_for("intervenciones.intervenciones_imprimir", id_intervenciones=result))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("intervenciones.intervenciones_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@intervenciones_bp.get("/intervenciones/imprimir/<id_intervenciones>")
def intervenciones_imprimir(id_intervenciones):
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        intervencion = mod_intervenciones.get_intervencion(id_intervenciones)
        imagenes = json.loads(intervencion["imagenes"])
        section = "Visualizando intervención de línea"
        return render_template("intervenciones/imprimir.html", 
                               title=title, section=section, 
                               intervencion=intervencion, imagenes=imagenes)
    else:
        return redirect(url_for("login.login_get"))
    
@intervenciones_bp.post("/intervenciones/buscar")
def intervenciones_buscar():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        return redirect(url_for("intervenciones.intervenciones_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@intervenciones_bp.get("/intervenciones/listado/<terminos_de_busqueda>")
def intervenciones_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_mercaderia.intervenciones(terminos_de_busqueda, resultados_por_pagina, offset)
        section = "Listado de intervenciones de línea"
        return render_template("intervenciones/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
