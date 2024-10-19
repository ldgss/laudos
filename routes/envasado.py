from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session


envasado_bp = Blueprint("envasado", __name__)
# cantidad para paginacion
resultados_por_pagina = 2

@envasado_bp.get("/envasado")
def envasado():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Envasado"
        section = "Envasado"
        return render_template("envasado/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@envasado_bp.get("/envasado/agregar")
def envasado_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        proximo_id = mod_mercaderia.get_ultimo_id()
        title = "Envasado"
        section = "Envasado"
        return render_template("envasado/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@envasado_bp.post("/envasado/agregar")
def envasado_agregar_post():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # obtenemos el id solo del vencimiento necesario
        vto = mod_mercaderia.get_vencimiento(request.form)
        # el insert devuelve True si todo salio bien
        barcode = mod_mercaderia.insert_mercaderia(request.form, vto)
        title = "Envasado"
        section = "Envasado"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("envasado.envasado_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("envasado.envasado_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@envasado_bp.get("/envasado/imprimir/<numero_unico>")
def envasado_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        envasado = mod_mercaderia.get_envasado(numero_unico)
        title = "Envasado"
        section = "Envasado"
        return render_template("envasado/imprimir.html", 
                               title=title, section=section, 
                               envasado=envasado)
    else:
        return redirect(url_for("login.login_get"))
    
@envasado_bp.post("/envasado/buscar")
def envasado_buscar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        return redirect(url_for("envasado.envasado_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@envasado_bp.get("/envasado/listado/<terminos_de_busqueda>")
def envasado_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_mercaderia.get_listado(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Envasado"
        section = "Envasado"
        return render_template("envasado/listado.html", 
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
   
@envasado_bp.get("/envasado/anular/<numero_unico>")
def envasado_anular(numero_unico):
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        # todo 8
        # decidir como anular el pallet
        pass
    else:
        return redirect(url_for("login.login_get"))