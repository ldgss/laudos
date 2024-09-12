from flask import render_template
from flask import Blueprint

errors_bp = Blueprint("errors", __name__)

@errors_bp.app_errorhandler(404)
def not_found(error):
    return render_template("error/pagina_no_encontrada.html"), 404

@errors_bp.app_errorhandler(401)
def unauthorized(error):
    return render_template("error/no_autorizado.html"), 401