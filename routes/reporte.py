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

        # Convertir a XLSX
        xlsx_path = file_path.replace(".csv", ".xlsx")
        df.to_excel(xlsx_path, index=False)

        # Enviar el archivo XLSX como respuesta
        return send_file(
            xlsx_path,
            as_attachment=True,
            download_name="reporte.xlsx",  # Cambiar la extensión a .xlsx
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # Tipo MIME para XLSX
        )
    except FileNotFoundError:
        return "El archivo no se encontró.", 404
    except Exception as e:
        return f"Ocurrió un error: {e}", 500
    # try:
    #     return send_file(
    #         file_path,
    #         as_attachment=True,
    #         download_name="reporte.csv",  # Cambiar la extensión a .csv
    #         mimetype="text/csv"  # Cambiar el tipo MIME a CSV
    #     )
    # except FileNotFoundError:
    #     return "El archivo no se encontró.", 404