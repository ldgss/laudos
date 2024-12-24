from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_hojalata
from models import mod_mercaderia
from models import mod_bloqueos
from flask import flash
from flask import request
from flask import session
from datetime import datetime
from dateutil.relativedelta import relativedelta


bloqueos_bp = Blueprint("bloqueos", __name__)
resultados_por_pagina = 10
@bloqueos_bp.get("/bloqueos")
def bloqueos():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        title = "Bloqueo"
        section = "Bloqueo"
        return render_template("bloqueados/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    

@bloqueos_bp.get("/bloqueos/agregar")
def bloqueos_agregar():
     if helpers.session_on() and helpers.authorized_to("bloqueo"):
        # hojalata = mod_hojalata.get_hojalata(numero_unico)
        
        title = "Bloqueados"
        section = "Bloqueados"
        return render_template("bloqueados/agregarid.html", 
                               title=title, section=section, 
                               productos_arballon = session["productos_arballon"])
     else:
        return redirect(url_for("login.login_get"))

@bloqueos_bp.post("/bloqueos/agregar/agregarbloq")
def bloqueos_agregar_post():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        # obtenemos el id solo del vencimiento necesario
        
        # el insert devuelve True si todo salio bien
        barcode = mod_bloqueos.insert_bloqueados_envasado(request.form)
        title = "Bloqueados"
        section = "Bloqueados"
        if barcode:
            # enviar a imprimir/detalle el producto recien creado
            return redirect(url_for("bloqueos.bloqueados_imprimir", id_unico=request.form["id_unico"]))
        
         
            
        else:
            flash("Se ha producido un error al intentar guardar los cambios. Intente de nuevo por favor.")
            return redirect(url_for("hojalata.hojalata_agregar"))
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.get("/bloqueos/imprimir/<id_unico>")
def bloqueados_imprimir(id_unico):
    print(id_unico)
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        bloqueados = mod_bloqueos.get_bloqueados(id_unico)
        title = "Bloqueados"
        section = "Bloqueados"
        return render_template("bloqueados/imprimir.html", 
                               title=title, section=section, 
                               bloqueados=bloqueados)
    else:
        return redirect(url_for("login.login_get"))

@bloqueos_bp.get("/bloqueos/agregar/<numero_unico>")
def bloqueos_agregar_id(numero_unico):
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        hojalata = mod_mercaderia.get_envasado(numero_unico)
        title = "bloqueados"
        section = "bloqueados"
        return render_template("bloqueados/agregar.html", 
                               title=title, section=section, 
                               hojalata=hojalata)
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.get("/bloqueos/agregarmultiple")
def bloqueos_agregar_multiple():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        proximo_id = mod_hojalata.get_ultimo_id()
        title = "Bloqueados"
        section = "Bloqueados"
        return render_template("bloqueados/agregarmultiple.html", 
                               title=title, section=section, 
                               proximo_id=proximo_id,
                               productos_arballon_hojalata=session["productos_arballon_hojalata"])
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.post("/bloqueos/buscar")
def bloqueos_buscar():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        return redirect(url_for("bloqueos.bloqueados_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    
@bloqueos_bp.post("/bloqueos/buscarbloqueados")
def bloqueos_buscarbloqueados():
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        return redirect(url_for("bloqueos.bloqueados_listado", terminos_de_busqueda=request.form["buscar"]))
    else:
        return redirect(url_for("login.login_get"))
    

@bloqueos_bp.get("/bloqueos/listado/<terminos_de_busqueda>")
def bloqueados_listado(terminos_de_busqueda):
    if helpers.session_on() and helpers.authorized_to("bloqueo"):
        # paginacion
        pagina = request.args.get('page', 1, type=int)
        offset = (pagina - 1) * resultados_por_pagina
      
        resultado = mod_bloqueos.get_listado_envasado(terminos_de_busqueda, resultados_por_pagina, offset)
        title = "Bloqueados"
        section = "Bloqueados"
        return render_template("bloqueados/listado.html",
                               max=max,
                               min=min, 
                               title=title, section=section, 
                               terminos_de_busqueda=terminos_de_busqueda,
                               listado=resultado[0], pagina_actual=pagina, total_paginas=resultado[1])
    else:
        return redirect(url_for("login.login_get"))

    
