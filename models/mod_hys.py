from sqlalchemy.sql import text
from flask import session
from db import db
from datetime import datetime
import shlex
from flask import request
import traceback


def anular_hys():
    # CUIDADO - DANGER - DELETE ZONE
    try:
        anulacion = text("""
                    DELETE FROM hys
                    WHERE id=:id;
                """
                )
        anulacion = db.db.session.execute(anulacion,
                                            {
                                                "id": request.form["id_hys"]                                                
                                            })
        db.db.session.commit()
        return True
    except Exception as e:
        db.db.session.rollback()
        print(f"Error: {e}")
        return None   

def guardar_hys():
    try:
        sql = text("""
                    INSERT INTO hys
                        (afectado, incidente, sector, 
                        tarea_que_realizaba, detalle, epp_si_no, 
                        area_limpia_si_no, informado_art_si_no, habilidades_si_no, 
                        gravedad, tipo_de_atencion, agente_origen, 
                        testigos, responsable, fecha_registro)
                    VALUES
                        (:afectado, :incidente, :sector, 
                        :tarea_que_realizaba, :detalle, :epp_si_no, 
                        :area_limpia_si_no, :informado_art_si_no, :habilidades_si_no, 
                        :gravedad, :tipo_de_atencion, :agente_origen, 
                        :testigos, :responsable, CURRENT_TIMESTAMP)
                   RETURNING id;
                """
                )
        
        incidente = db.db.session.execute(sql,
                                            {
                                                "afectado": request.form.get("afectado"),
                                                "incidente": request.form.get("incidente"),
                                                "sector": request.form.get("sector"),
                                                "tarea_que_realizaba": request.form.get("tarea_que_realizaba"),
                                                "detalle": request.form.get("detalle"),
                                                "epp_si_no": request.form.get("epp_si_no"),
                                                "area_limpia_si_no": request.form.get("area_limpia_si_no"),
                                                "informado_art_si_no": request.form.get("informado_art_si_no"),
                                                "habilidades_si_no": request.form.get("habilidades_si_no"),
                                                "gravedad": request.form.get("gravedad"),
                                                "tipo_de_atencion": request.form.get("tipo_de_atencion"),
                                                "agente_origen": request.form.get("agente_origen"),
                                                "testigos": request.form.get("testigos"),
                                                "responsable": session["id"]
                                            })
        new_id = incidente.scalar()
        db.db.session.commit()
        return new_id
    except Exception as e:
        db.db.session.rollback()
        error_traceback = traceback.format_exc()
        print(f"e: {e}")
        print(f"tb: {error_traceback}")
        return None
    
def get_hys(id_hys):
    try:
        sql = text("""
                    SELECT 
                        h.afectado,
                        h.incidente,
                        h.sector,
                        h.tarea_que_realizaba,
                        h.detalle,
                        h.epp_si_no,
                        h.area_limpia_si_no,
                        h.informado_art_si_no,
                        h.habilidades_si_no,
                        h.gravedad,
                        h.tipo_de_atencion,
                        h.agente_origen,
                        h.testigos,
                        u.nombre as responsable,
                        h.fecha_registro
                    FROM hys h
                    INNER JOIN usuario u ON u.id = h.responsable
                    WHERE h.id = :id
                """
                )
        
        medicion = db.db.session.execute(sql,{
                                                "id": id_hys
                                        })
        return medicion.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_estadisticas():
    try:
        sql = text("""
                    SELECT 
                    m.electricidad_acometida_norte_kw,
                    m.electricidad_acometida_este_kw,
                    m.gas_natural_m3,
                    m.agua_pozo_m3x100,
                    m.agua_caldera1_m3,
                    m.agua_caldera2_m3,
                    m.agua_caldera3_m3,
                    m.efluente_generado_m3,
                    u.nombre as responsable,
                    m.fecha_registro,
                    observaciones
                    FROM mediciones_de_energia m
                    inner join usuario u on u.id = m.responsable
                    ORDER BY m.id ASC
                    LIMIT 12;
                """
                )
        
        medicion = db.db.session.execute(sql)
        # return medicion.mappings().fetchall()
        return [dict(row) for row in medicion.mappings().all()]
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_listado_hys(terminos_de_busqueda, resultados_por_pagina, offset):
    try:
        # todo 7
        terminos_de_busqueda = shlex.split(terminos_de_busqueda)
        condiciones_ilike = []
        
        for termino in terminos_de_busqueda:
            subcondicion = []
            subcondicion.append(f"h.afectado::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.incidente::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.sector::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.tarea_que_realizaba::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.detalle::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.gravedad::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.tipo_de_atencion::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.agente_origen::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.testigos::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"h.fecha_registro::TEXT ILIKE '%{termino}%'")
            subcondicion.append(f"u.nombre::TEXT ILIKE '%{termino}%'")
            
            condiciones_ilike.append(f"({' OR '.join(subcondicion)})")
        # refinamos la busqueda
        condicion_final_ilike = ' AND '.join(condiciones_ilike)

        query_sql = f"""
            SELECT 
                h.id,
                h.afectado,
                h.incidente,
                h.sector,
                h.tarea_que_realizaba,
                h.detalle,
                h.epp_si_no,
                h.area_limpia_si_no,
                h.informado_art_si_no,
                h.habilidades_si_no,
                h.gravedad,
                h.tipo_de_atencion,
                h.agente_origen,
                h.testigos,
                u.nombre as responsable,
                h.fecha_registro
            FROM hys h
            INNER JOIN usuario u ON u.id = h.responsable
            WHERE {condicion_final_ilike}
            ORDER BY h.id DESC
            LIMIT :limit OFFSET :offset;
        """
        resultados = db.db.session.execute(text(query_sql),
                    {"limit": resultados_por_pagina, "offset": offset})
    
        # calculo el numero de paginas
        total_resultados = f"""
                                SELECT COUNT(*)
                                FROM (
                                    SELECT 
                                        h.afectado,
                                        h.incidente,
                                        h.sector,
                                        h.tarea_que_realizaba,
                                        h.detalle,
                                        h.epp_si_no,
                                        h.area_limpia_si_no,
                                        h.informado_art_si_no,
                                        h.habilidades_si_no,
                                        h.gravedad,
                                        h.tipo_de_atencion,
                                        h.agente_origen,
                                        h.testigos,
                                        u.nombre as responsable,
                                        h.fecha_registro
                                    FROM hys h
                                    INNER JOIN usuario u ON u.id = h.responsable
                                    WHERE {condicion_final_ilike}
                                ) AS total_count;
                            """

        total_resultados_scalar = db.db.session.execute(text(total_resultados)).scalar()
        total_paginas = total_resultados_scalar // resultados_por_pagina
        if total_resultados_scalar % resultados_por_pagina != 0:
            total_paginas += 1
        return [resultados.fetchall(), total_paginas]

    except Exception as e:
        print(f"Error: {e}")
        return None