import streamlit as st

# Configuración de la pantalla para celulares
st.set_page_config(page_title="NeumoCheck", page_icon="🫁", layout="centered")

st.title("🫁 NeumoCheck Pro")
st.write("Asistente de Internación Neumonológica (No UTI)")
st.info("⚠️ Recordatorio: No ingrese datos filiatorios del paciente. Solo variables clínicas anónimas.")

# Pestañas de navegación estilo App móvil
tab1, tab2 = st.tabs(["📊 Gases y Oxigenación", "📋 Score CURB-65"])

with tab1:
    st.header("Análisis de Gases en Sangre")
    
    # Entradas de datos con selectores cómodos para el dedo en el iPhone
    ph = st.number_input("pH Arterial", min_value=6.80, max_value=7.80, value=7.40, step=0.01)
    pco2 = st.number_input("pCO2 (mmHg)", min_value=10, max_value=100, value=40, step=1)
    po2 = st.number_input("pO2 (mmHg)", min_value=30, max_value=200, value=80, step=1)
    fio2 = st.slider("FiO2 estimada (%)", min_value=21, max_value=100, value=21, step=1)

    # Cálculos médicos automatizados
    pafi = int(po2 / (fio2 / 100))
    
    # Lógica de interpretación ácido-base simplificada
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

    # Mostrar Resultados en tarjetas visuales
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
    
    # Checkboxes adaptados para uso rápido en recorrida de sala
    c = st.checkbox("¿Confusión nueva?")
    u = st.checkbox("¿Uremia > 42 mg/dl (o Urea > 7 mmol/L)?")
    r = st.checkbox("¿Frecuencia Respiratoria ≥ 30 vpm?")
    b = st.checkbox("¿Presión Arterial Sistólica < 90 o Diastólica ≤ 60 mmHg?")
    age = st.checkbox("¿Edad ≥ 65 años?")
    
    # Cálculo del score acumulativo
    score = sum([c, u, r, b, age])
    
    st.subheader(f"Puntaje Total: {score} / 5")
    
    # Recomendación clínica basada en el Score tradicional
    if score <= 1:
        st.success("Riesgo Bajo (Mortalidad < 3%). Considerar tratamiento ambulatorio controlado.")
    elif score == 2:
        st.warning("Riesgo Moderado (Mortalidad ~9%). Considerar Internación Corta en Sala General / Monitoreo Estrecho.")
    else:
        st.error("Riesgo Alto (Mortalidad > 15%). Requiere Internación en Sala General Completa. Evaluar criterios de UTI.")
