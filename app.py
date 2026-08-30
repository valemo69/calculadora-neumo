import streamlit as st

# Configuración del nombre de la pestaña del navegador y la app
st.set_page_config(page_title="Cetrángolo NeumoCheck", page_icon="🫁", layout="centered")

# CABECERA PERSONALIZADA CON EL NUEVO NOMBRE
st.write("🏥 **Hospital de Agudos y Crónicos Dr. Antonio A. Cetrángolo**")
st.title("🫁 Cetrángolo NeumoCheck")
st.caption("Monitoreo Clínico y Soporte Respiratorio No Invasivo en Sala General")
st.info("⚠️ Recordatorio: No ingrese datos filiatorios del paciente (Nombres, DNI, Camas). Solo variables clínicas anónimas.")

# Pestañas de navegación estilo App móvil
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Gases y Oxigenación", 
    "📋 Score CURB-65", 
    "🩺 Riesgo ARISCAT", 
    "🧮 Calc. Clínicas"
])

with tab1:
    st.header("Análisis de Gases en Sangre")
    
    ph = st.number_input("pH Arterial", min_value=6.80, max_value=7.80, value=7.40, step=0.01, key="ph_input")
    pco2 = st.number_input("pCO2 (mmHg)", min_value=10, max_value=100, value=40, step=1, key="pco2_input")
    po2 = st.number_input("pO2 (mmHg)", min_value=30, max_value=200, value=80, step=1, key="po2_input")
    fio2 = st.slider("FiO2 estimada (%)", min_value=21, max_value=100, value=21, step=1, key="fio2_slider")

    pafi = int(po2 / (fio2 / 100))
    
    if ph < 7.35:
        estado_ph = "Acidemia"
        if pco2 > 45:
            mecanismo = "Acidosis Respiratoria (Sugerir evaluar VNI si hay fatiga muscular)"
        else:
            mecanismo = "Acidosis Metabólica / Mixta"
    elif ph > 7.45:
        estado_ph = "Alcalemia"
        if pco2 < 35:
            mecanismo = "Alcalosis Respiratoria (Hiperventilación)"
        else:
            mecanismo = "Alcalosis Metabólica"
    else:
        estado_ph = "Equilibrio Ácido-Base Normal"
        mecanismo = "Valores dentro del rango fisiológico estándar."

    st.subheader("Resultados:")
    st.metric(label="Interpretación Inicial", value=estado_ph, delta=mecanismo, delta_color="inverse")
    
    if pafi < 200:
        st.error(f"⚠️ PAFI: {pafi} mmHg - Hipoxemia Grave / Distrés Respiratorio")
    elif pafi < 300:
        st.warning(f"⚠️ PAFI: {pafi} mmHg - Hipoxemia Moderada")
    else:
        st.success(f"✅ PAFI: {pafi} mmHg - Oxigenación Adecuada")

with tab2:
    st.header("Estratificación CURB-65")
    st.write("Evaluación de Severidad en Neumonía Adquirida en la Comunidad")
    
    c = st.checkbox("¿Confusión nueva?", key="curb_c")
    u = st.checkbox("¿Uremia > 42 mg/dl o Urea > 7 mmol/L?", key="curb_u")
    r = st.checkbox("¿Frecuencia Respiratoria ≥ 30 vpm?", key="curb_r")
    b = st.checkbox("¿Presión Arterial Sistólica < 90 o Diastólica ≤ 60 mmHg?", key="curb_b")
    age = st.checkbox("¿Edad ≥ 65 años?", key="curb_age")
    
    score = sum([c, u, r, b, age])
    
    st.subheader(f"Puntaje Total: {score} / 5")
    
    if score <= 1:
        st.success("Riesgo Bajo (Mortalidad < 3%). Considerar tratamiento ambulatorio controlado.")
    elif score == 2:
        st.warning("Riesgo Moderado (Mortalidad ~9%). Considerar Internación Corta en Sala General / Monitoreo Estrecho.")
    else:
        st.error("Riesgo Alto (Mortalidad > 15%). Requiere Internación en Sala General Completa. Evaluar criterios de UTI.")

with tab3:
    st.header("Riesgo Quirúrgico Respiratorio (ARISCAT)")
    st.write("Predicción de complicaciones pulmonares postoperatorias (CPP)")
    
    edad_sel = st.radio("Edad del paciente:", ["< 50 años (0 pts)", "51 - 80 años (3 pts)", "> 80 años (16 pts)"])
    p_edad = 0 if "< 50" in edad_sel else (3 if "51" in edad_sel else 16)
    
    sat_sel = st.radio("Saturación de O2 preoperatoria:", ["≥ 96% (0 pts)", "91 - 95% (8 pts)", "≤ 90% (24 pts)"])
    p_sat = 0 if "≥ 96%" in sat_sel else (8 if "91" in sat_sel else 24)
    
    inf_resp = st.checkbox("¿Tuvo infección respiratoria en el último mes? (17 pts)")
    p_inf = 17 if inf_resp else 0
    
    anemia = st.checkbox("¿Anemia preoperatoria? Hb ≤ 10 g/dl (11 pts)")
    p_anemia = 11 if anemia else 0
    
    sitio_sel = st.radio("Sitio de la cirugía:", ["Periférica / No abdominal ni torácica (0 pts)", "Abdominal alta (15 pts)", "Intratorácica (24 pts)"])
    p_sitio = 0 if "Periférica" in sitio_sel else (15 if "Abdominal alta" in sitio_sel else 24)
    
    duracion = st.checkbox("¿Duración prevista de la cirugía > 3 hours? (16 pts)")
    p_duracion = 16 if duracion else 0
    
    urgencia = st.checkbox("¿Es una cirugía de urgencia? (8 pts)")
    p_urgencia = 8 if urgencia else 0
    
    ariscat_score = p_edad + p_sat + p_inf + p_anemia + p_sitio + p_duracion + p_urgencia
    
    st.subheader(f"Puntaje ARISCAT Total: {ariscat_score} puntos")
    
    if ariscat_score < 26:
        st.success("Riesgo Bajo de complicaciones pulmonares (< 3%).")
    elif ariscat_score <= 44:
        st.warning("Riesgo Intermedio de complicaciones pulmonares (~13%). Planificar kinesiología respiratoria perioperatoria.")
    else:
        st.error("Riesgo Alto de complicaciones pulmonares (~42%). Requiere optimización estricta y monitoreo postop cercano.")

with tab4:
    st.header("🧮 Calculadoras Médicas y Soporte No Invasivo")
    
    # SECCIÓN 1: ÍNDICE DE ROX (Monitoreo de CNAF)
    st.subheader("1. Índice de ROX (Monitoreo de Alto Flujo)")
    st.caption("Validado para evaluar el riesgo de falla de la CNAF en Neumonías Hipoxémicas.")
    
    rox_sat = st.number_input("Saturación de O2 del paciente (%)", min_value=50, max_value=100, value=94, key="rox_sat")
    rox_fio2 = st.slider("FiO2 actual de la CNAF (%)", min_value=21, max_value=100, value=40, key="rox_fio2") / 100
    rox_fr = st.number_input("Frecuencia Respiratoria (vpm)", min_value=10, max_value=60, value=24, key="rox_fr")
    
    if rox_fio2 > 0 and rox_fr > 0:
        rox_index = (rox_sat / rox_fio2) / rox_fr
        st.write(f"**Índice de ROX calculado:** {rox_index:.2f}")
        
        if rox_index >= 4.88:
            st.success("✅ Bajo riesgo de falla de CNAF. Continuar monitoreo clínico de rutina.")
        elif rox_index >= 3.85:
            st.warning("⚠️ Riesgo intermedio de falla. Monitorear estrechamente en las próximas 2 horas. Evaluar ajustar parámetros.")
        else:
            st.error("🚨 Alto riesgo de falla de CNAF. Alta probabilidad de requerir intubación/UTI. No demorar la reevaluación.")
            
    st.divider()
    
    # SECCIÓN 2: SCORE HACOR (Monitoreo de VNI)
    st.subheader("2. Score HACOR (Monitoreo de VNI / BiPAP)")
    st.caption("Evalúa el éxito o fracaso de la ventilación no invasiva a la hora de haber iniciado el soporte.")
    
    h_fc = st.radio("Frecuencia Cardíaca (lpm):", ["≤ 120 (0 pts)", "≥ 121 (1 pt)"], key="h_fc")
    p_h_fc = 1 if "≥ 121" in h_fc else 0
    
    h_ph = st.radio("pH Arterial actual:", ["≥ 7.35 (0 pts)", "7.30 - 7.34 (1 pt)", "7.25 - 7.29 (2 pts)", "7.20 - 7.24 (3 pts)", "< 7.20 (4 pts)"], key="h_ph")
    p_h_ph = 0 if "≥ 7.35" in h_ph else (1 if "7.30" in h_ph else (2 if "7.25" in h_ph else (3 if "7.20" in h_ph else 4)))
    
    h_gcs = st.radio("Estado Neurológico (Glasgow):", ["15 - Normal (0 pts)", "13 - 14 (2 pts)", "≤ 12 (5 pts)"], key="h_gcs")
    p_h_gcs = 0 if "15" in h_gcs else (2 if "13" in h_gcs else 5)
    
    h_pafi = st.radio("Relación PaO2/FiO2 actual (PAFI):", ["> 200 (0 pts)", "176 - 200 (2 pts)", "151 - 175 (3 pts)", "126 - 150 (4 pts)", "101 - 125 (5 pts)", "≤ 100 (6 pts)"], key="h_pafi")
    p_h_pafi = 0 if "> 200" in h_pafi else (2 if "176" in h_pafi else (3 if "151" in h_pafi else (4 if "126" in h_pafi else (5 if "101" in h_pafi else 6))))
    
    h_fr = st.radio("Frecuencia Respiratoria (vpm):", ["≤ 30 (0 pts)", "31 - 35 (1 pt)", "36 - 40 (2 pts)", "41 - 45 (3 pts)", "≥ 46 (4 pts)"], key="h_fr")
    p_h_fr = 0 if "≤ 30" in h_fr else (1 if "31" in h_fr else (2 if "36" in h_fr else (3 if "41" in h_fr else 4)))
    
    hacor_total = p_h_fc + p_h_ph + p_h_gcs + p_h_pafi + p_h_fr
    st.write(f"**Score HACOR Total:** {hacor_total} puntos")
    
    if hacor_total <= 5:
        st.success("✅ Buen pronóstico con VNI. Continuar con la estrategia actual si los objetivos clínicos acompañan.")
    else:
        st.error("🚨 Alto riesgo de falla de VNI (Mortalidad intrahospitalaria y tasa de intubación elevadas). Considerar fuertemente pase inmediato a UTI.")

    st.divider()
    
    # SECCIÓN 3: Clearance de Creatinina (Cockcroft-Gault)
    st.subheader("3. Aclaramiento de Creatinina (Ajuste antibiótico)")
    
    col1, col2 = st.columns(2)
    with col1:
        cc_edad = st.number_input("Edad (años)", min_value=1, max_value=110, value=65, step=1, key="cc_edad")
        cc_peso = st.number_input("Peso (kg)", min_value=30, max_value=200, value=70, step=1, key="cc_peso")
    with col2:
        cc_creat = st.number_input("Creatinina Sérica (mg/dl)", min_value=0.20, max_value=10.00, value=1.00, step=0.01, key="cc_creat")
        cc_sexo = st.radio("Sexo biológico:", ["Masculino", "Femenino"], key="cc_sexo")
        
    if cc_creat > 0:
        clearance = ((140 - cc_edad) * cc_peso) / (72 * cc_creat)
        if cc_sexo == "Femenino":
            clearance *= 0.85
            
        st.write(f"**Aclaramiento Estimado:** {clearance:.1f} mL/min")
        
        if clearance >= 90:
            st.success("Función renal normal / hiperfiltración.")
        elif clearance >= 60:
            st.info("Deterioro leve de la función renal.")
        elif clearance >= 30:
            st.warning("Deterioro moderado de la función renal (Revisar dosis de antibióticos).")
        else:
            st.error("Deterioro grave de la función renal / Falla renal.")
            
    st.divider()
    
    # SECCIÓN 4: Índice de Paquetes-Año (Pack-Years)
    st.subheader("4. Índice de Paquetes-Año (Carga Tabáquica)")
    
    py_cigarrillos = st.number_input("Cantidad de cigarrillos fumados por día:", min_value=0, max_value=100, value=20, step=1, key="py_cig")
