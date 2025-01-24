from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from models import mod_acceso
from flask import flash
from flask import request
from flask import session
from device_detector import DeviceDetector
import json

acceso_bp = Blueprint("acceso", __name__)

def guardar_login(request):
    if helpers.session_on():
        ip = None
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            # Si no hay cabecera 'X-Forwarded-For', usamos 'remote_addr'
            ip = request.remote_addr
        
        dispositivo = DeviceDetector(request.user_agent.string).parse()
        # devicedetector obj no es serializable, por eso lo casteo
        dispositivo = f"{dispositivo.all_details}"
        dispositivo = json.dumps(dispositivo)
        
        result = mod_acceso.guardar_login(ip, dispositivo, session["id"])
        
        if result:
            return True
    else:
        return False