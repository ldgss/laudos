from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint

mercaderia_bp = Blueprint("mercaderia", __name__)

@mercaderia_bp.route("/mercaderia")
def mercaderia():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Mercaderia"
        section = "Mercaderia"
        return render_template("mercaderia/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
    
@mercaderia_bp.get("/mercaderia/agregar")
def mercaderia_agregar():
    if helpers.session_on() and helpers.authorized_to("mercaderia"):
        title = "Mercaderia"
        section = "Mercaderia"
        return render_template("mercaderia/agregar.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))