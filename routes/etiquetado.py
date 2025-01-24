from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session


etiquetado_bp = Blueprint("etiquetado", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@etiquetado_bp.get("/etiquetado")
def etiquetado():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Etiquetado"
        section = "Etiquetado"
        return render_template("etiquetado/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetado_bp.get("/etiquetado/agregar")
def etiquetado_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        proximo_id = mod_mercaderia.get_ultimo_id()
        title = "Etiquetado"
        section = "Etiquetado"
        return render_template("etiquetado/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetado_bp.post("/etiquetado/agregar")
def etiquetado_agregar_post():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # obtenemos el id solo del vencimiento necesario
        vto = mod_mercaderia.get_vencimiento(request.form)
        # ensamblo el lote
        lote = f"{request.form['lote_a']}-{request.form['lote_b']}-{request.form['lote_c']}"
        barcode = mod_mercaderia.guardar_etiquetado(request.form, vto, lote)
        title = "Etiquetado"
        section = "Etiquetado"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("etiquetado.etiquetado_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("etiquetado.etiquetado_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetado_bp.get("/etiquetado/imprimir/<numero_unico>")
def etiquetado_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        etiquetado = mod_mercaderia.get_etiquetado(numero_unico)
        title = "Etiquetado"
        section = "Etiquetado"
        return render_template("etiquetado/imprimir.html", 
                               title=title, section=section, 
                               etiquetado=etiquetado)
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetado_bp.post("/etiquetado/buscar")
def etiquetado_buscar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        return redirect(url_for("etiquetado.etiquetado_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetado_bp.get("/etiquetado/listado/<terminos_de_busqueda>")
def etiquetado_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        resultado = mod_mercaderia.get_listado_etiquetado(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Etiquetado"
        section = "Etiquetado"
        return render_template("etiquetado/listado.html", 
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
