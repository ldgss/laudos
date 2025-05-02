from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_retiro
from flask import request
from flask import flash

retiro_bp = Blueprint("retiro", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@retiro_bp.get("/retiro")
def retiro():
    if helpers.session_on() and helpers.authorized_to("materia"):
        title = "Retiro"
        section = "Retiro"
        return render_template("retiro/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@retiro_bp.post("/retiro/buscar")
def retiro_buscar():
    if helpers.session_on() and helpers.authorized_to("materia"):
        return redirect(url_for("retiro.retiro_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))

@retiro_bp.get("/retiro/agregar")
def retiro_agregar():
    if helpers.session_on() and helpers.authorized_to("materia"):
        clientes_proveedores = mod_retiro.get_clientes_proveedores()
        title = "Retiro"
        section = "Retiro"
        return render_template("retiro/agregar.html", 
                               title=title, section=section, 
                               clientes_proveedores = clientes_proveedores
                               )
    else:
        return redirect(url_for("login.login_get"))

@retiro_bp.post("/retiro/agregar")
def retiro_agregar_post():
    if helpers.session_on() and helpers.authorized_to("materia") and not helpers.authorized_to_action("limitado"):
        resultado = mod_retiro.guardar_retiro()
        if resultado:
            return redirect(url_for("retiro.retiro_imprimir", id=resultado))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("retiro.retiro_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@retiro_bp.get("/retiro/imprimir/<id>")
def retiro_imprimir(id):
    if helpers.session_on() and helpers.authorized_to("materia"):
        retiro = mod_retiro.get_retiro(id)
        title = "Retiro"
        section = "Retiro"
        return render_template("retiro/imprimir.html", 
                               title=title, section=section, 
                               retiro=retiro)
    else:
        return redirect(url_for("login.login_get"))
    
@retiro_bp.get("/retiro/listado/<terminos_de_busqueda>")
def retiro_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("materia"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_retiro.get_listado_retiro(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Retiro"
        section = "Retiro"
        return render_template("retiro/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))