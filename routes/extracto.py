from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session


extracto_bp = Blueprint("extracto", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@extracto_bp.get("/extracto")
def extracto():
    if helpers.session_on() and helpers.authorized_to("extracto"):
        title = "Extracto"
        section = "Extracto"
        return render_template("extracto/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@extracto_bp.get("/extracto/agregar")
def extracto_agregar():
    if helpers.session_on() and helpers.authorized_to("extracto"):
        proximo_id = mod_mercaderia.get_ultimo_id_extracto()
        title = "Extracto"
        section = "Extracto"
        return render_template("extracto/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@extracto_bp.post("/extracto/agregar")
def extracto_agregar_post():
    if helpers.session_on() and helpers.authorized_to("extracto"):
        # obtenemos el id solo del vencimiento necesario
        vto = mod_mercaderia.get_vencimiento(request.form)
        # ensamblo el lote
        lote = f"{request.form["lote_a"]}-{request.form["lote_b"]}-{request.form["lote_c"]}"
        barcode = mod_mercaderia.guardar_extracto(request.form, vto, lote)
        title = "Extracto"
        section = "Extracto"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("extracto.extracto_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("extracto.extracto_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@extracto_bp.get("/extracto/imprimir/<numero_unico>")
def extracto_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("extracto"):
        extracto = mod_mercaderia.get_extracto(numero_unico)
        title = "Extracto"
        section = "Extracto"
        return render_template("extracto/imprimir.html", 
                               title=title, section=section, 
                               extracto=extracto)
    else:
        return redirect(url_for("login.login_get"))
    
@extracto_bp.post("/extracto/buscar")
def extracto_buscar():
    if helpers.session_on() and helpers.authorized_to("extracto"):
        return redirect(url_for("extracto.extracto_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@extracto_bp.get("/extracto/listado/<terminos_de_busqueda>")
def extracto_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("extracto"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_mercaderia.get_listado_extracto(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Extracto"
        section = "Extracto"
        return render_template("extracto/listado.html", 
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
