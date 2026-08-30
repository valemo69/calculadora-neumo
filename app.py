import streamlit as st
import os

# Configuración del nombre de la pestaña del navegador y la app para iPhone
st.set_page_config(page_title="Cetrángolo NeumoCheck", page_icon="🫁", layout="centered")

# CABECERA INSTITUCIONAL CON LOGO AUTOMÁTICO (Si subes el archivo logo.png)
if os.path.exists("logo.png"):
    st.image("logo.png", width=140)

st.write("🏥 **Hospital de Agudos y Crónicos Dr. Antonio A. Cetrángolo**")
st.title("🫁 Cetrángolo NeumoCheck")
st.caption("Guía de Decisiones de Guardia y Soporte Respiratorio - Sala General (No UTI)")
st.info("⚠️ Recordatorio: No ingrese datos filiatorios del paciente (Nombres, DNI). Solo variables clínicas anónimas.")

# Estructura limpia de 3 Solapas Principales propuestas para optimizar el flujo de trabajo
tab_guia, tab_quirurgico, tab_calculadoras = st.tabs([
    "🛟 Guía VNI / Alto Flujo", 
    "🩺 Riesgo Quirúrgico", 
    "🧮 Calculadoras de Sala"
])

# ==============================================================================
# SOLAPA 1: GUÍA DE MANEJO COMPLETA DE VNI Y ALTO FLUJO PARA EL RESIDENTE
# ==============================================================================
with tab_guia:
    st.header("📋 Protocolo de Soporte No Invasivo en Guardia")
    st.write("Asistente paso a paso para disminuir errores en el piso de internación.")
    
    soporte = st.selectbox(
        "1. Seleccione la terapia actual del paciente:",
        ["[Seleccionar]", "Ventilación No Invasiva (VNI - BiPAP/CPAP)", "Cánula Nasal de Alto Flujo (CNAF)"]
    )
    
    if soporte == "Ventilación No Invasiva (VNI - BiPAP/CPAP)":
        st.subheader("🛠️ Monitoreo de VNI (Evaluar a los 60 minutos del inicio)")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            ipap_act = st.number_input("IPAP programada (cmH2O)", min_value=6, max_value=25, value=12, step=1)
            epap_act = st.number_input("EPAP programada (cmH2O)", min_value=4, max_value=12, value=5, step=1)
            fr_paciente = st.number_input("Frecuencia Respiratoria (vpm)", min_value=10, max_value=50, value=28, key="fr_p_vni")
        with col_v2:
            fio2_act = st.slider("FiO2 actual del equipo (%)", min_value=21, max_value=100, value=35)
            fc_vni = st.number_input("Frecuencia Cardíaca (lpm)", min_value=40, max_value=180, value=90, key="fc_vni_p")
            glasgow = st.radio("Estado Neurológico (Glasgow):", ["15 (Lúcido / Colabora)", "13-14 (Tendencia a somnolencia)", "≤ 12 (Estuporoso / No protege vía aérea)"])
            
        st.write("**📄 Gases en Sangre Actuales:**")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            ph_vni = st.number_input("pH Arterial bajo VNI", min_value=6.80, max_value=7.80, value=7.30, step=0.01)
        with col_g2:
            pco2_vni = st.number_input("pCO2 (mmHg)", min_value=15, max_value=120, value=60, step=1)
        with col_g3:
            po2_vni = st.number_input("pO2 (mmHg)", min_value=30, max_value=200, value=60, step=1)
            
        # Cálculo del Score HACOR automático
        p_fc = 1 if fc_vni >= 121 else 0
        p_ph = 0 if ph_vni >= 7.35 else (1 if ph_vni >= 7.30 else (2 if ph_vni >= 7.25 else (3 if ph_vni >= 7.20 else 4)))
        p_gcs = 0 if "15" in glasgow else (2 if "13-14" in glasgow else 5)
        pafi_vni = (po2_vni / (fio2_act / 100))
        p_pafi = 0 if pafi_vni > 200 else (2 if pafi_vni >= 176 else (3 if pafi_vni >= 151 else (4 if pafi_vni >= 126 else (5 if pafi_vni >= 101 else 6))))
        p_fr = 0 if fr_paciente <= 30 else (1 if fr_paciente <= 35 else (2 if fr_paciente <= 40 else (3 if fr_paciente <= 45 else 4)))
        hacor_score = p_fc + p_ph + p_gcs + p_pafi + p_fr
        
        st.markdown("### 🛑 CONDUCTA MANDATORIA DE GUARDIA:")
        
        # Criterios definitivos de "BASTA"
        if "≤ 12" in glasgow or hacor_score > 5 or fr_paciente > 40:
            st.error(f"""
            ### 🚨 FRACASO DE VNI (HACOR: {hacor_score} puntos)
            **INDICACIÓN:** SUSPENDER la VNI inmediatamente.
            *   El paciente presenta alto riesgo de parada respiratoria o incapacidad de proteger vía aérea.
            *   **Acción:** Inicie secuencia de intubación rápida y gestione de urgencia la cama en **UTI**. ¡No demore la intubación en el piso!
            """)
        # Criterios de "Espero 1 hora y reevalúo"
        elif ph_vni < 7.35 and pco2_vni > 45:
            nueva_ipap = ipap_act + 2
            st.warning(f"""
            ### ⚠️ AJUSTE POR ACIDEMIA HIPERCÁPNICA PERSISTENTE
            **DIAGNÓSTICO:** El paciente tolera la interfaz pero el volumen minuto es insuficiente (sigue atrapando CO2).
            *   **Conducta inmediata:** **SUBIR LA IPAP EN +2 cmH2O** (Pasar de {ipap_act} a **{nueva_ipap} cmH2O**). Esto aumentará el gradiente de presión (Delta P).
            *   **Próximo paso:** **ESPERAR EXACTAMENTE 1 HORA** y repetir gases en sangre. Si el pH no corrige o hay fatiga muscular en la reevaluación, asuma fracaso terapéutico.
            """)
        elif pafi_vni < 200 or po2_vni < 60:
            nueva_epap = epap_act + 2
            st.warning(f"""
            ### ⚠️ AJUSTE POR HIPOXEMIA PERSISTENTE
            **DIAGNÓSTICO:** Falla de oxigenación / Colapso alveolar.
            *   **Conducta inmediata:** **SUBIR LA EPAP EN +1 o +2 cmH2O** (Pasar de {epap_act} a **{nueva_epap} cmH2O**) para reclutamiento alveolar.
            *   **Próximo paso:** Evaluar tolerancia y repetir gases / control clínico en 1 hora.
            """)
        else:
            st.success(f"""
            ### ✅ RESPUESTA EXITOSA A LA VNI (HACOR: {hacor_score} pts)
            **ESTADO:** Gases en rango aceptable, sin signos de fatiga ni asincronía.
            *   **Conducta:** Mantener los parámetros actuales ({ipap_act}/{epap_act} cmH2O).
            """)

        # Recordatorio explícito de transcripción para la Historia Clínica
        st.info(f"""
        📝 **RECORDATORIO PARA EL RESIDENTE / MÉDICO DE GUARDIA:**
        *   **Esta aplicación NO guarda datos en memoria** ni se conecta al sistema del hospital. Al cerrar o refrescar la pantalla, los valores cargados desaparecerán por completo.
        *   **Conducta Obligatoria:** Transcriba AHORA este control en la **Historia Clínica (HC) del paciente**: consigne los parámetros iniciales del equipo, los gases basales, el puntaje obtenido y la conducta que el sistema le acaba de indicar.
        """)

    elif soporte == "Cánula Nasal de Alto Flujo (CNAF)":
        st.subheader("🛠️ Monitoreo de Alto Flujo")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            flujo_act = st.number_input("Flujo actual (L/min)", min_value=10, max_value=70, value=50, step=5)
            sat_act = st.number_input("Saturación de O2 actual (%)", min_value=50, max_value=100, value=92, step=1, key="sat_cnaf_act")
        with col_c2:
            fio2_cnaf_act = st.slider("FiO2 programada en el equipo (%)", min_value=21, max_value=100, value=40, key="fio2_cnaf_slider") / 100
            fr_cnaf_act = st.number_input("Frecuencia Respiratoria (vpm)", min_value=10, max_value=50, value=25, key="fr_cnaf_p")
            
        rox_index = (sat_act / fio2_cnaf_act) / fr_cnaf_act
        st.write(f"**📈 Índice de ROX Calculado:** {rox_index:.2f}")
        
        st.markdown("### 🛑 CONDUCTA MANDATORIA DE GUARDIA:")
        
        if rox_index < 3.85:
            st.error(f"""
            ### 🚨 FRACASO DE CNAF (Índice de ROX: {rox_index:.2f} < 3.85)
            **INDICACIÓN:** Detener la terapia de alto flujo inmediatamente. Alto riesgo de parada respiratoria.
            *   **Conducta:** Evalúe pasar a **VNI de rescate** o gestione de urgencia la cama en **UTI**.
            """)
        elif rox_index < 4.88:
            st.warning(f"""
            ### ⚠️ ZONA GRIS / RIESGO INTERMEDIO (Índice de ROX: {rox_index:.2f})
            **CONDUCTA:** El soporte actual es limítrofe.
            *   **Acción:** Maximice flujo a **60 L/min** y titule FiO2. **RE-EVALÚE EL ÍNDICE DE ROX EN EXACTAMENTE 1 HORA**.
            """)
        else:
            if fr_cnaf_act > 28:
                st.warning(f"""
                ### ⚠️ ROX ESTABLE PERO PACIENTE POLIPNEICO (FR: {fr_cnaf_act})
                **ALERTA:** Trabajo respiratorio elevado. Monitoree de cerca. Considere ciclos de **VNI (BiPAP)** para descansar la bomba muscular.
                """)
            else:
                st.success(f"""
                ### ✅ RESPUESTA ADECUADA A LA CNAF (Índice de ROX: {rox_index:.2f})
                **CONDUCTA:** Paciente estable. Sostener parámetros actuales.
                """)

        st.info(f"""
        📝 **RECORDATORIO PARA EL RESIDENTE / MÉDICO DE GUARDIA:**
        *   **Esta aplicación NO guarda datos en memoria** ni se conecta al sistema del hospital. Al cerrar o refrescar la pantalla, los valores cargados desaparecerán por completo.
        *   **Conducta Obligatoria:** Transcriba AHORA este control en la **Historia Clínica (HC) del paciente**: consigne los parámetros de flujo/FiO2, la frecuencia respiratoria, el Índice de ROX calculado y la conducta a seguir.
        """)

# ==============================================================================
# SOLAPA 2: RIESGO QUIRÚRGICO RESPIRATORIO (ARISCAT + TORRINGTON)
# ==============================================================================
with tab_quirurgico:
    st.header("Evaluación de Riesgo Quirúrgico")
    st.write("Modelos predictivos de complicaciones pulmonares postoperatorias (CPP).")
    
    sub1, sub2 = st.tabs(["ARISCAT (Clínico-Quirúrgico)", "Torrington-Henderson (Neumonológico)"])
    
    with sub1:
        st.subheader("Escala ARISCAT")
        edad_sel = st.radio("Edad del paciente:", ["< 50 años (0 pts)", "51 - 80 años (3 pts)", "> 80 años (16 pts)"], key="ar_e")
        p_edad = 0 if "< 50" in edad_sel else (3 if "51" in edad_sel else 16)
