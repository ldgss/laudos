from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session


energia_bp = Blueprint("energia", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@energia_bp.get("/energia")
def energia():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        title = "energia"
        section = "energia"
        return render_template("energia/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.get("/energia/agregar")
def energia_agregar():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        proximo_id = mod_mercaderia.get_ultimo_id()
        title = "energia"
        section = "energia"
        return render_template("energia/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.post("/energia/agregar")
def energia_agregar_post():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        # obtenemos el id solo del vencimiento necesario
        vto = mod_mercaderia.get_vencimiento(request.form)
        # ensamblo el lote
        lote = f"{request.form["lote_a"]}-{request.form["lote_b"]}-{request.form["lote_c"]}"
        barcode = mod_mercaderia.guardar_energia(request.form, vto, lote)
        title = "energia"
        section = "energia"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("energia.energia_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("energia.energia_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.get("/energia/imprimir/<numero_unico>")
def energia_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        energia = mod_mercaderia.get_energia(numero_unico)
        title = "energia"
        section = "energia"
        return render_template("energia/imprimir.html", 
                               title=title, section=section, 
                               energia=energia)
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.post("/energia/buscar")
def energia_buscar():
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        return redirect(url_for("energia.energia_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@energia_bp.get("/energia/listado/<terminos_de_busqueda>")
def energia_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mantenimiento"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_mercaderia.get_listado_energia(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "energia"
        section = "energia"
        return render_template("energia/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
