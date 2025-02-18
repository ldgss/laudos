from flask import session
from flask import abort
import pytz

fecha_local = pytz.timezone('America/Argentina/Buenos_Aires')

def convertir_a_local(fecha):
    if fecha.tzinfo is None:
        fecha = pytz.utc.localize(fecha)
    return fecha.astimezone(fecha_local)

def session_on():
    if 'nombre' in session:
        return True
    return False

def esta_activo():
    if session["esta_activo"]:
        return True
    return False

def authorized_to(section):
    if section in session:
        if session[section] is True:
            return True
    return abort(401)