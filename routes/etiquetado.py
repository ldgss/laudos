from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint

etiquetado_bp = Blueprint("etiquetado", __name__)

@etiquetado_bp.route("/etiquetado")
def etiquetado():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Etiquetado"
        section = "Etiquetado"
        return render_template("etiquetado/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@etiquetado_bp.get("/etiquetado/agregar")
def etiquetado_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Etiquetado"
        section = "Etiquetado"
        return render_template("etiquetado/agregar.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))