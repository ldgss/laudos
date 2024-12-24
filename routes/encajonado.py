from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session


encajonado_bp = Blueprint("encajonado", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@encajonado_bp.get("/encajonado")
def encajonado():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Encajonado"
        section = "Encajonado"
        return render_template("encajonado/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@encajonado_bp.get("/encajonado/agregar")
def encajonado_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        proximo_id = mod_mercaderia.get_ultimo_id()
        title = "Encajonado"
        section = "Encajonado"
        return render_template("encajonado/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@encajonado_bp.post("/encajonado/agregar")
def encajonado_agregar_post():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # obtenemos el id solo del vencimiento necesario
        vto = mod_mercaderia.get_vencimiento(request.form)
        # ensamblo el lote
        lote = f"{request.form["lote_a"]}-{request.form["lote_b"]}-{request.form["lote_c"]}"
        barcode = mod_mercaderia.guardar_encajonado(request.form, vto, lote)
        title = "Encajonado"
        section = "Encajonado"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("encajonado.encajonado_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("encajonado.encajonado_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@encajonado_bp.get("/encajonado/imprimir/<numero_unico>")
def encajonado_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        encajonado = mod_mercaderia.get_encajonado(numero_unico)
        title = "Encajonado"
        section = "Encajonado"
        return render_template("encajonado/imprimir.html", 
                               title=title, section=section, 
                               encajonado=encajonado)
    else:
        return redirect(url_for("login.login_get"))
    
@encajonado_bp.post("/encajonado/buscar")
def encajonado_buscar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        return redirect(url_for("encajonado.encajonado_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@encajonado_bp.get("/encajonado/listado/<terminos_de_busqueda>")
def encajonado_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_mercaderia.get_listado_encajonado(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Encajonado"
        section = "Encajonado"
        return render_template("encajonado/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
