from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint

insumos_bp = Blueprint("insumos", __name__)

@insumos_bp.route("/insumos")
def insumos():
    if helpers.session_on() and helpers.authorized_to("insumo"):
        title = "Insumos"
        section = "Insumos"
        return render_template("insumos/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))