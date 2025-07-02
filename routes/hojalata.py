from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_hojalata
from models import mod_mercaderia
from flask import flash
from flask import request
from flask import session


hojalata_bp = Blueprint("hojalata", __name__)
# cantidad para paginacion
resultados_por_pagina = 20

@hojalata_bp.get("/hojalata")
def hojalata():
    if helpers.session_on() and helpers.authorized_to("hojalata"):
        title = "Hojalata"
        section = "Hojalata"
        return render_template("hojalata/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@hojalata_bp.get("/hojalata/agregar")
def hojalata_agregar():
    if helpers.session_on() and helpers.authorized_to("hojalata"):
        proximo_id = mod_hojalata.get_ultimo_id()
        proximo_pallet_interno = mod_hojalata.get_ultimo_pallet_interno()
        title = "Hojalata"
        section = "Hojalata"
        return render_template("hojalata/agregar.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               proximo_pallet_interno=proximo_pallet_interno,
                               productos_arballon=session["productos_arballon"])
    else:
        return redirect(url_for("login.login_get"))
    
@hojalata_bp.post("/hojalata/agregar")
def hojalata_agregar_post():
    if helpers.session_on() and helpers.authorized_to("hojalata"):
        vto = mod_mercaderia.get_vencimiento(request.form)
        lote = f"{request.form["lote_a"]}-{request.form["lote_b"]}-{request.form["lote_c"]}"
        barcode = mod_hojalata.guardar_hojalata(request.form, vto, lote)
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("hojalata.hojalata_imprimir", numero_unico=request.form["numero_unico"]))
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("hojalata.hojalata_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@hojalata_bp.get("/hojalata/imprimir/<numero_unico>")
def hojalata_imprimir(numero_unico):
    if helpers.session_on() and helpers.authorized_to("hojalata"):
        hojalata = mod_hojalata.get_hojalata(numero_unico)
        title = "Hojalata"
        section = "Hojalata"
        return render_template("hojalata/imprimir.html", 
                               title=title, section=section, 
                               hojalata=hojalata)
    else:
        return redirect(url_for("login.login_get"))
    
@hojalata_bp.post("/hojalata/buscar")
def hojalata_buscar():
    if helpers.session_on() and helpers.authorized_to("hojalata"):
        return redirect(url_for("hojalata.hojalata_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@hojalata_bp.get("/hojalata/listado/<terminos_de_busqueda>")
def hojalata_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("hojalata"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
        
        resultado = mod_hojalata.get_listado_hojalata(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Hojalata"
        section = "Hojalata"
        return render_template("hojalata/listado.html", 
                               max=max,
                               min=min,
                               offset=offset,
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))
