from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_materia
from flask import flash
from flask import request
from flask import session


materia_bp = Blueprint("materia", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@materia_bp.get("/materia")
def materia():
    if helpers.session_on() and helpers.authorized_to("materia"):
        title = "Materia"
        section = "Materia"
        return render_template("materia/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@materia_bp.get("/materia/agregar")
def materia_agregar():
    if helpers.session_on() and helpers.authorized_to("materia"):
        productores = mod_materia.get_productores()
        productores = [
            {'cod_mae': cod_mae.strip(), 'den': den.strip(), 'cod_cls': cod_cls}
            for cod_mae, den, cod_cls in productores
        ]
        variedades = mod_materia.get_variedades()
        variedades = [
            {'cod_mae': cod_mae.strip(), 'den': den.strip(), 'cod_cls': cod_cls}
            for cod_mae, den, cod_cls in variedades
        ]
        fleteros = mod_materia.get_fleteros()
        fleteros = [
            {'cod_mae': cod_mae.strip(), 'den': den.strip(), 'cod_cls': cod_cls}
            for cod_mae, den, cod_cls in fleteros
        ]
        title = "Materia"
        section = "Materia"
        return render_template("materia/agregar.html", 
                               title=title, section=section, 
                               productores=productores,
                               variedades=variedades,
                               fleteros=fleteros
                               )
    else:
        return redirect(url_for("login.login_get"))
    
@materia_bp.post("/materia/agregar")
def materia_agregar_post():
    if helpers.session_on() and helpers.authorized_to("materia"):
        resultado = mod_materia.guardar_materia()
        title = "Materia"
        section = "Materia"
        if resultado:
            return redirect(url_for("materia.materia_imprimir", id=resultado))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("materia.materia_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@materia_bp.get("/materia/imprimir/<id>")
def materia_imprimir(id):
    if helpers.session_on() and helpers.authorized_to("materia"):
        materia = mod_materia.get_materia(id)
        title = "Materia"
        section = "Materia"
        return render_template("materia/imprimir.html", 
                               title=title, section=section, 
                               materia=materia)
    else:
        return redirect(url_for("login.login_get"))
    
@materia_bp.post("/materia/buscar")
def materia_buscar():
    if helpers.session_on() and helpers.authorized_to("materia"):
        return redirect(url_for("materia.materia_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@materia_bp.get("/materia/listado/<terminos_de_busqueda>")
def materia_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("materia"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_materia.get_listado_materia(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Materia"
        section = "Materia"
        return render_template("materia/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
