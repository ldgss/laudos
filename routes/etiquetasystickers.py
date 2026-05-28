from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_etiquetasystickers
from flask import flash
from flask import request
from flask import jsonify
import json


etiquetasystickers_bp = Blueprint("etiquetasystickers", __name__)
# cantidad para paginacion
resultados_por_pagina = 20
title = 'Etiquetas y stickers'

@etiquetasystickers_bp.get("/etiquetasystickers")
def etiquetasystickers():
    if helpers.session_on() and helpers.authorized_to("etiquetasystickers"):
        etiquetasystickers = mod_etiquetasystickers.listar_etiquetas_y_stickers_arballon()
        section = "Etiquetas y stickers"
        return render_template(
            "etiquetasystickers/index.html", 
            title=title, 
            section=section,
            etiquetasystickers=etiquetasystickers
            )
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetasystickers_bp.get("/etiquetasystickers/listado")
def etiquetasystickers_listado():
    if helpers.session_on() and helpers.authorized_to("etiquetasystickers"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_etiquetasystickers.get_listado_etiquetasystickers(resultados_por_pagina, offset)
        section = "Lista de etiquetas y stickers"
        return render_template("etiquetasystickers/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetasystickers_bp.post("/etiquetasystickers/buscar")
def etiquetasystickers_buscar():
    if helpers.session_on() and helpers.authorized_to("etiquetasystickers"):
        resultado = mod_etiquetasystickers.get_etiquetasystickers()
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({})
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetasystickers_bp.post("/etiquetasystickers/guardar")
def etiquetasystickers_guardar():
    if helpers.session_on() and helpers.authorized_to("etiquetasystickers"):
        result = mod_etiquetasystickers.guardar_etiquetasystickers()
        if result:
            flash("Imagen guardada con éxito.")
            return redirect(url_for("etiquetasystickers.etiquetasystickers"))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("etiquetasystickers.etiquetasystickers"))
    else:
        return redirect(url_for("login.login_get"))
