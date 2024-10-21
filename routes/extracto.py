from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint

extracto_bp = Blueprint("extracto", __name__)

@extracto_bp.route("/extracto")
def extracto():
    if helpers.session_on() and helpers.authorized_to("extracto"):
        title = "Extracto"
        section = "Extracto"
        return render_template("extracto/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))