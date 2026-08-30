# logica/scores_quirurgicos.py

def calcular_ariscat(edad, spo2, infeccion, anemia, incision, duracion, emergencia):
    puntos = 0
    
    # 1. Edad
    if edad == "51 - 80 años": puntos += 3
    elif edad == "> 80 años": puntos += 16
    
    # 2. SpO2 preoperatorio (aire ambiente)
    if spo2 == "91 - 95%": puntos += 8
    elif spo2 == "≤ 90%": puntos += 24
    
    # 3. Infección respiratoria en el último mes
    if infeccion == "Sí": puntos += 17
    
    # 4. Anemia preoperatoria (Hb ≤ 10 g/dL)
    if anemia == "Sí": puntos += 11
    
    # 5. Incisión quirúrgica
    if incision == "Abdominal alta": puntos += 15
    elif incision == "Intratorácica": puntos += 24
    
    # 6. Duración de la cirugía
    if duracion == "2 - 3 horas": puntos += 16
    elif duracion == "> 3 horas": puntos += 23
    
    # 7. Procedimiento de emergencia
    if emergencia == "Sí": puntos += 8
    
    return puntos

def clasificar_riesgo_ariscat(score):
    if score < 26:
        return "Bajo Riesgo", "Tasa de CPP estimada: 1.6%", "success"
    elif score < 45:
        return "Riesgo Intermedio", "Tasa de CPP estimada: 13.3%", "warning"
    else:
        return "Alto Riesgo", "Tasa de CPP estimada: 42.1%", "error"

def calcular_torrington(fvc_baja, relacion_baja, edad_mayor, obesidad, tabaquismo, sintomas, cirugia_riesgo):
    puntos = 0
    if fvc_baja: puntos += 1
    if relacion_baja: puntos += 1
    if edad_mayor: puntos += 1
    if obesidad: puntos += 1
    if tabaquismo: puntos += 1
    if sintomas: puntos += 1
    if cirugia_riesgo: puntos += 2
    return puntos

def clasificar_riesgo_torrington(score):
    if score <= 3:
        return "Bajo Riesgo", "Mortalidad: 0.1% | Complicaciones: 5-8%", "success"
    elif score <= 6:
        return "Riesgo Moderado", "Mortalidad: 5.6% | Complicaciones: 23-35%", "warning"
    else:
        return "Alto Riesgo", "Mortalidad: 11.2% | Complicaciones: 45-56%", "error"

