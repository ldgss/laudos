CREATE OR REPLACE FUNCTION verificar_cantidad_aportada()
RETURNS TRIGGER AS '
DECLARE
    cantidad_original INT;
    cantidad_total_aportada INT;
BEGIN
    -- Obtener la cantidad original de la mercaderia antecedente
    SELECT cantidad INTO cantidad_original 
    FROM mercaderia 
    WHERE id = NEW.mercaderia_antecedente;

    -- Sumar las cantidades ya aportadas por este antecedente (excluyendo la nueva)
    SELECT COALESCE(SUM(cantidad_tomada), 0) INTO cantidad_total_aportada
    FROM antecedentes 
    WHERE mercaderia_antecedente = NEW.mercaderia_antecedente
      AND id != NEW.id; -- Excluir la fila actual si es una actualización

    -- Agregar la nueva cantidad tomada
    cantidad_total_aportada := cantidad_total_aportada + NEW.cantidad_tomada;

    -- Verificar si la cantidad excede la cantidad original
    IF cantidad_total_aportada > cantidad_original THEN
        RAISE EXCEPTION ''Cantidad total tomada % supera la cantidad original % para el antecedente %'',
                        cantidad_total_aportada, cantidad_original, NEW.mercaderia_antecedente;
    END IF;

    RETURN NEW;
END;
' LANGUAGE plpgsql;

CREATE TRIGGER trigger_verificar_cantidad_aportada
BEFORE INSERT OR UPDATE ON antecedentes
FOR EACH ROW
EXECUTE FUNCTION verificar_cantidad_aportada();
