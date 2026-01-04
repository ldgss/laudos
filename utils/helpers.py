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

def authorized_to_submodule(submodule):
    if submodule in session:
        if session[submodule] is True:
            return True
    return abort(401)

def authorized_to_action(action):
    if action in session:
        if session[action]:
            return abort(401)
        return False
    return abort(401)

def next_id(ultimo_id, code, year):
    if not ultimo_id:
        # primer numero unico
        return f"{year}-{code}-000000"
    elif ultimo_id and year != int(ultimo_id[:4]):
        # cambio de año
        return f"{year}-{code}-000000"
    else:
        # numero unico subsiguiente
        prefijo = str(year)
        sufijo = int(ultimo_id[-6:])
        nuevo_numero = sufijo + 1
        nuevo_numero_str = f"{nuevo_numero:06d}"
        nuevo_codigo = f"{prefijo}-{code}-{nuevo_numero_str}"

        return nuevo_codigo
        