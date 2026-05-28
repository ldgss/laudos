from flask import Blueprint
from models import mod_kpi
from flask import jsonify

kpi_bp = Blueprint("kpi", __name__)

@kpi_bp.get("/kpi/<key>/<producto>")
def kpi_listado(key, producto):
    if  key == '202502171357prodAPI':
        resultado = mod_kpi.get_listado_kpi(producto)
        return resultado
    else:
        return "404"
