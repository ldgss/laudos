from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session


hys_bp = Blueprint("hys", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@hys_bp.get("/hys")
def hys():
    if helpers.session_on() and helpers.authorized_to("hys"):
        title = "hys"
        section = "hys"
        return render_template("hys/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.get("/hys/agregar")
def hys_agregar():
    if helpers.session_on() and helpers.authorized_to("hys"):
        proximo_id = mod_mercaderia.get_ultimo_id()
        title = "hys"
        section = "hys"
        return render_template("hys/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.post("/hys/agregar")
def hys_agregar_post():
    if helpers.session_on() and helpers.authorized_to("hys"):
        # obtenemos el id solo del vencimiento necesario
        vto = mod_mercaderia.get_vencimiento(request.form)
        # ensamblo el lote
        lote = f"{request.form["lote_a"]}-{request.form["lote_b"]}-{request.form["lote_c"]}"
        barcode = mod_mercaderia.guardar_hys(request.form, vto, lote)
        title = "hys"
        section = "hys"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("hys.hys_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("hys.hys_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.get("/hys/imprimir/<numero_unico>")
def hys_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("hys"):
        hys = mod_mercaderia.get_hys(numero_unico)
        title = "hys"
        section = "hys"
        return render_template("hys/imprimir.html", 
                               title=title, section=section, 
                               hys=hys)
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.post("/hys/buscar")
def hys_buscar():
    if helpers.session_on() and helpers.authorized_to("hys"):
        return redirect(url_for("hys.hys_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@hys_bp.get("/hys/listado/<terminos_de_busqueda>")
def hys_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("hys"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_mercaderia.get_listado_hys(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "hys"
        section = "hys"
        return render_template("hys/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
