from sqlalchemy.sql import text
from db import db

def get_mercaderia():
    try:
        # Abre la conexión a SQL Server usando el bind
        with db.db.get_engine(bind='sqlserver').connect() as connection:
            # Ejecuta la consulta SQL directa en SQL Server
            result = connection.execute(text("""
                SELECT cod_mae, den, cod_cls FROM genmae
                WHERE tip_mae = 4 AND (
                    cod_cls = 'Extrac' OR
                    cod_cls = 'Pas500' OR
                    cod_cls = 'Pelado' OR
                    cod_cls = 'Pulpa' OR
                    cod_cls = 'Pure' OR
                    cod_cls = 'Tri500' OR
                    cod_cls = 'Tri8' OR
                    cod_cls = 'Tri910' OR
                    cod_cls = 'Tri950' OR
                    cod_cls = 'Tritur'
                )
            """))
            return result.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return None
    
def insert_envasado(form):
    try:
        sql = text("""
                    SELECT *
                    FROM vencimiento
                    WHERE producto = :producto
                    ORDER BY id DESC;
                """
                )
        
        result = db.db.session.execute(sql,{"producto": form["cod_cls"]})
        print(form)
        print(result.mappings().first())
        # return result.mappings().first()
    except Exception as e:
        print(f"Error: {e}")
        return None
