import os
import sys
import cv2
import numpy as np

# Cortes de matiz (H) por etapa: (hue_min, hue_max, etapa). El rojo cruza el 0, por eso hay hue negativo.
CORTES = [(32, 999, 1), (19, 32, 2), (11, 19, 3), (2, 11, 4), (-4.5, 2, 5), (-999, -4.5, 6)]

DESCRIPCIONES = {
    1: "INAPTO: La piel del tomate está completamente verde.",
    2: "INAPTO: Hasta el 10% de la superficie con colores amarillos y anaranjados.",
    3: "APTO: Del 10 al 30% de la superficie amarillo, anaranjado a rojo.",
    4: "APTO: Del 30 al 60% de la superficie con color rosado a rojo.",
    5: "APTO: Del 60 al 90% de la superficie con colores rosados a rojo.",
    6: "APTO: Más del 90% de la superficie de color rojo.",
}

UMBRAL_AVISO = 8.0      # % de tomates inaptos (etapas 1-2) -> informar a supervisor
UMBRAL_RECHAZO = 30.0   # % de tomates inaptos (etapas 1-2) -> rechazo de carga
RADIO_TOMATE = 8        # radio aproximado de un tomate en px (calibrar por cámara)

# Zonas de tomate por imagen (solo para pruebas). En producción: un ROI fijo por cámara.
ROIS = {
    "calidad_rojo.jpeg":  [(0,560),(330,190),(560,130),(740,200),(1000,430),(1250,640),(1450,850),(1600,1060),(1600,1200),(0,1200)],
    "calidad_verde.jpeg": [(230,640),(330,540),(560,420),(760,330),(960,200),(990,60),(960,470),(950,800),(880,880),(870,1330),(860,1520),(420,1500),(330,1440),(180,1250),(180,1000),(230,800)],
    "calidad_media.jpeg": [(395,680),(560,565),(750,470),(960,380),(1100,340),(1250,300),(1400,250),(1600,218),(1600,265),(1520,330),(1420,420),(1290,520),(1200,555),(1000,590),(740,630),(560,655)],
}


def etapa_por_hue(hue):
    for lo, hi, st in CORTES:
        if lo <= hue < hi:
            return st
    return 6

def clasificar_tomates(img, valid, hue_img, radio):
    """Separa tomates individuales (distance transform + watershed) y clasifica cada uno por su matiz mediano."""
    mask = valid.astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    dist = cv2.GaussianBlur(dist, (0, 0), 1.5)
    k = int(radio * 2) | 1
    picos = ((dist == cv2.dilate(dist, np.ones((k, k), np.uint8))) & (dist > radio * 0.6)).astype(np.uint8)

    n, marcadores = cv2.connectedComponents(picos)
    marcadores = marcadores + 1                      # 1 = fondo
    marcadores[mask == 0] = 1
    marcadores[(mask > 0) & (picos == 0)] = 0        # 0 = desconocido
    marcadores = marcadores.astype(np.int32)
    cv2.watershed(img, marcadores)

    # regiones candidatas: descarta las muy chicas (ruido)
    regiones = []
    for lab in range(2, n + 1):
        reg = (marcadores == lab) & (mask > 0)
        area = int(reg.sum())
        if area >= radio * radio * 1.2:
            regiones.append((reg, area))
    if not regiones:
        return []

    # descarta manchones enormes (lona, chapa) respecto del tamaño típico de tomate
    med = float(np.median([a for _, a in regiones]))
    return [etapa_por_hue(float(np.median(hue_img[reg]))) for reg, a in regiones if a <= 4 * med]

def predict_tomato_maturity(image_path, roi=None, radio=RADIO_TOMATE):
    if not os.path.exists(image_path):
        return {"error": f"La ruta '{image_path}' no ha sido encontrada."}

    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Formato de imagen inválido."}

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    valid = (s > 35) & (v > 110)
    if roi is not None:
        mask = np.zeros(h.shape, np.uint8)
        cv2.fillPoly(mask, [np.array(roi, np.int32)], 255)
        valid &= (mask > 0)

    if valid.sum() < 100:
        return {"error": "No se detectaron píxeles de tomate."}

    # rojo cruza el 0: llevar 170-180 a -10..0
    hue_img = np.where(h > 150, h.astype(np.int16) - 180, h.astype(np.int16))

    # 1) análisis tomate por tomate
    etapas = np.array(clasificar_tomates(img, valid, hue_img, radio))
    if len(etapas) == 0:
        return {"error": "No se pudo separar ningún tomate (revisar radio)."}

    # 2) análisis agregado
    dist = {st: float(np.mean(etapas == st) * 100) for st in range(1, 7)}
    inapto_pct = dist[1] + dist[2]
    etapa_pred = max(dist, key=dist.get)

    if inapto_pct > UMBRAL_RECHAZO:
        decision = "RECHAZO DE CARGA - informar a supervisor"
    elif inapto_pct > UMBRAL_AVISO:
        decision = "INFORMAR A SUPERVISOR"
    else:
        decision = "CARGA APTA"

    return {
        "analisis": "completo",
        "tomates_detectados": len(etapas),
        "etapa_predominante": f"Etapa {etapa_pred}",
        "descripcion": DESCRIPCIONES[etapa_pred],
        "metricas": {f"etapa {st}": f"{dist[st]:.1f}%" for st in range(1, 7)},
        "inapto_pct": f"{inapto_pct:.1f}%",
        "decision": decision,
    }


def imprimir(img, res):
    print(f"Resultado para imagen: {img}")
    for k, val in res.items():
        if isinstance(val, dict):
            print(f"  {k}:")
            for kk, vv in val.items():
                print(f"    {kk} -> {vv}")
        else:
            print(f"  {k}: {val}")


if __name__ == '__main__':
    print("=" * 50)
    print("Detector de madurez de tomate")
    print("=" * 50)
    if len(sys.argv) < 2:
        print("Uso: python madurez.py <imagen> [lote]")
        images = ['./img/1.png', './img/2a.png', './img/2b.png', './img/3.png',
                  './img/4.png', './img/5.png', './img/6.png']
        for img in images:
            imprimir(img, predict_tomato_maturity(img, radio=20))
    else:
        img = sys.argv[1]
        radio = int(sys.argv[2]) if len(sys.argv) > 2 else RADIO_TOMATE
        roi = ROIS.get(os.path.basename(img))
        imprimir(img, predict_tomato_maturity(img, roi=roi, radio=radio))