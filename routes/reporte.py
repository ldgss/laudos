from flask import render_template
from flask import redirect
from flask import url_for
from utils import helpers
from flask import Blueprint
from flask import flash
from flask import request
from flask import session
from models import mod_reporte
from flask import send_file
import pandas as pd
from io import BytesIO

reporte_bp = Blueprint("reporte", __name__)

@reporte_bp.get("/reporte")
def reporte():
    if helpers.session_on():
        title = "Reporte"
        section = "Reporte"
        return render_template("reporte/index.html", title=title, section=section)
    else:
        return redirect(url_for("login.login_get"))
        
@reporte_bp.post("/reporte/exportar/<modulo>")
def reporte_exportar(modulo):
    if helpers.session_on():
        
        match modulo:
            case "envasado":
                return generar_reporte(mod_reporte.get_envasado())
            case "etiquetado":
                return generar_reporte(mod_reporte.get_etiquetado())
            case "encajonado":
                return generar_reporte(mod_reporte.get_encajonado())
            case "reacondicionado":
                return generar_reporte(mod_reporte.get_reacondicionado())
            case "extracto":
                return generar_reporte(mod_reporte.get_extracto())
            case "insumo":
                return generar_reporte(mod_reporte.get_insumo())
            case "ubicacion":
                return generar_reporte(mod_reporte.get_ubicacion())
            case _:
                return redirect(url_for("reporte.reporte"))
    else:
        return redirect(url_for("login.login_get"))
    
def generar_reporte(file_path):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path)

        # Convertir a Excel en un buffer de memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        # Preparar el buffer para ser leído por `send_file`
        output.seek(0)

        # Enviar el archivo Excel al cliente
        return send_file(
            output,
            as_attachment=True,
            download_name="reporte.xlsx",  # Nombre del archivo a descargar
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        return "El archivo no se encontró.", 404
    except Exception as e:
        # return f"Error al generar el reporte: {str(e)}", 500
        flash("Nada para mostrar")
        return redirect(url_for("reporte.reporte"))
    