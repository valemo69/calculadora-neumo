# logica/scores_vni.py

def calcular_puntos_ph(ph):
    if ph >= 7.35: return 0
    elif ph >= 7.30: return 1
    elif ph >= 7.25: return 2
    elif ph >= 7.20: return 3
    return 4

def calcular_puntos_gcs(glasgow_str):
    if "15" in glasgow_str: return 0
    elif "13-14" in glasgow_str: return 2
    return 5

def calcular_puntos_pafi(pafi):
    if pafi > 200: return 0
    elif pafi >= 176: return 2
    elif pafi >= 151: return 3
    elif pafi >= 126: return 4
    elif pafi >= 101: return 5
    return 6

def calcular_puntos_fr(fr):
    if fr <= 30: return 0
    elif fr <= 35: return 1
    elif fr <= 40: return 2
    elif fr <= 45: return 3
    return 4

def calcular_score_hacor(fc, ph, glasgow, pafi, fr):
    p_fc = 1 if fc >= 121 else 0
    p_ph = calcular_puntos_ph(ph)
    p_gcs = calcular_puntos_gcs(glasgow)
    p_pafi = calcular_puntos_pafi(pafi)
    p_fr = calcular_puntos_fr(fr)
    return p_fc + p_ph + p_gcs + p_pafi + p_fr
