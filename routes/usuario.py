from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session

# global object
active_users = []

usuario_bp = Blueprint("usuario", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@usuario_bp.get("/usuario")
def usuario():
    if helpers.session_on() and helpers.authorized_to("usuario"):
        title = "Usuario"
        section = "Usuario"
        return render_template("usuario/index.html", 
                               title=title, 
                               section=section, 
                               active_users=active_users)
    else:
        return redirect(url_for("login.login_get"))
    
@usuario_bp.get("/usuario/agregar")
def usuario_agregar():
    if helpers.session_on() and helpers.authorized_to("usuario"):
        proximo_id = mod_mercaderia.get_ultimo_id()
        title = "Usuario"
        section = "Usuario"
        return render_template("usuario/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@usuario_bp.post("/usuario/agregar")
def usuario_agregar_post():
    if helpers.session_on() and helpers.authorized_to("usuario"):
        # obtenemos el id solo del vencimiento necesario
        vto = mod_mercaderia.get_vencimiento(request.form)
        # ensamblo el lote
        lote = f"{request.form["lote_a"]}-{request.form["lote_b"]}-{request.form["lote_c"]}"
        barcode = mod_mercaderia.guardar_usuario(request.form, vto, lote)
        title = "Usuario"
        section = "Usuario"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("usuario.usuario_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("usuario.usuario_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@usuario_bp.get("/usuario/imprimir/<numero_unico>")
def usuario_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("usuario"):
        usuario = mod_mercaderia.get_usuario(numero_unico)
        title = "Usuario"
        section = "Usuario"
        return render_template("usuario/imprimir.html", 
                               title=title, section=section, 
                               usuario=usuario)
    else:
        return redirect(url_for("login.login_get"))
    
@usuario_bp.post("/usuario/buscar")
def usuario_buscar():
    if helpers.session_on() and helpers.authorized_to("usuario"):
        return redirect(url_for("usuario.usuario_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@usuario_bp.get("/usuario/listado/<terminos_de_busqueda>")
def usuario_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("usuario"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_mercaderia.get_listado_usuario(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Usuario"
        section = "Usuario"
        return render_template("usuario/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
