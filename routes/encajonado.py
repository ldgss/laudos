from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint

encajonado_bp = Blueprint("encajonado", __name__)

@encajonado_bp.route("/encajonado")
def encajonado():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Encajonado"
        section = "Encajonado"
        return render_template("encajonado/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@encajonado_bp.get("/encajonado/agregar")
def encajonado_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Encajonado"
        section = "Encajonado"
        return render_template("encajonado/agregar.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))