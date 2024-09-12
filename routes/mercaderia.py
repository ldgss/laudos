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
        body = "Mercaderia"
        return render_template("mercaderia/index.html", title=title, body=body)
    else:
        return redirect(url_for("login.login_get"))