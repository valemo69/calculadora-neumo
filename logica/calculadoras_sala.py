# ==========================================
# SCORE CURB-65 (Neumonía)
# ==========================================
def calcular_curb65(confusion, urea, fr, pa_sistolica, pa_diastolica, edad):
    puntos = 0
    if confusion == "Sí": puntos += 1
    # Punto por Urea > 42 mg/dL (equivalente a BUN > 19 mg/dL o > 7 mmol/L)
    if urea > 42: puntos += 1 
    if fr >= 30: puntos += 1
    if pa_sistolica < 90 or pa_diastolica <= 60: puntos += 1
    if edad >= 65: puntos += 1
    return puntos

def clasificar_curb65(score):
    if score <= 1: 
        return "Bajo Riesgo", "Mortalidad 1.5%. Tratamiento ambulatorio.", "success"
    elif score == 2: 
        return "Riesgo Intermedio", "Mortalidad 9.2%. Considerar internación en sala general.", "warning"
    else: 
        return "Alto Riesgo", "Mortalidad ≥ 22%. Internación urgente, considerar UTI si score ≥ 4.", "error"

# ==========================================
# CLEARANCE DE CREATININA (Cockcroft-Gault)
# ==========================================
def calcular_clearance_creatinina(edad, peso, creatinina, sexo):
    if creatinina <= 0: return 0 # Evitar error matemático
    clearance = ((140 - edad) * peso) / (72 * creatinina)
    if sexo == "Mujer":
        clearance *= 0.85
    return clearance

# ==========================================
# MEDIO INTERNO Y ELECTROLITOS
# ==========================================
def calcular_agua_corporal(peso, sexo, edad):
    if sexo == "Hombre":
        factor = 0.6 if edad < 65 else 0.5
    else:
        factor = 0.5 if edad < 65 else 0.45
    return peso * factor

def calcular_deficit_sodio(peso, sexo, edad, na_actual, na_deseado):
    act = calcular_agua_corporal(peso, sexo, edad)
    deficit_na = act * (na_deseado - na_actual)
    return deficit_na, act

def calcular_deficit_agua_libre(peso, sexo, edad, na_actual):
    # Para Hipernatremia
    act = calcular_agua_corporal(peso, sexo, edad)
    deficit_agua = act * ((na_actual / 140) - 1)
    return deficit_agua

def calcular_calcio_corregido(calcio_ionico, albumina):
    return calcio_ionico + 0.8 * (4.0 - albumina)

# ==========================================
# TROMBOEMBOLISMO PULMONAR (TEP)
# ==========================================
def calcular_wells_tep(tvp, diag_alt, fc_alta, inmovilizacion, tep_previo, hemoptisis, cancer):
    puntos = 0.0
    if tvp: puntos += 3.0
    if diag_alt: puntos += 3.0
    if fc_alta: puntos += 1.5
    if inmovilizacion: puntos += 1.5
    if tep_previo: puntos += 1.5
    if hemoptisis: puntos += 1.0
    if cancer: puntos += 1.0
    return puntos

def clasificar_wells_tep(score):
    if score <= 4.0:
        return "Tromboembolismo Improbable", "Considerar Dímero-D. Si es negativo, se excluye TEP.", "success"
    else:
        return "Tromboembolismo Probable", "Solicitar Angio-TC de tórax (Dímero-D no es útil aquí).", "error"

def calcular_spesi(edad_mayor, cancer, epoc_ic, fc_alta, pas_baja, sat_baja):
    puntos = 0
    if edad_mayor: puntos += 1
    if cancer: puntos += 1
    if epoc_ic: puntos += 1
    if fc_alta: puntos += 1
    if pas_baja: puntos += 1
    if sat_baja: puntos += 1
    return puntos

def clasificar_spesi(score):
    if score == 0:
        return "Riesgo Bajo", "Mortalidad a 30 días: ~1.0%. Considerar tratamiento ambulatorio o alta precoz.", "success"
    else:
        return "Riesgo Alto", "Mortalidad a 30 días: ~10.9%. Requiere internación (considerar UTI/UCO si inestabilidad).", "error"
