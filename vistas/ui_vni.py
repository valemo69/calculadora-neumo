import streamlit as st
from logica.scores_vni import calcular_score_hacor

# Constantes Médicas
ROX_LIMITE_FRACASO = 3.85
ROX_ZONA_GRIS = 4.88
HACOR_LIMITE_FRACASO = 5

def mostrar_recordatorio_hc():
    st.info("""
    📝 **RECORDATORIO PARA EL RESIDENTE / MÉDICO DE GUARDIA:**
    *   **Esta aplicación NO guarda datos en memoria** ni se conecta al sistema del hospital. Al cerrar o refrescar la pantalla, los valores cargados desaparecerán por completo.
    *   **Conducta Obligatoria:** Transcriba AHORA este control en la **Historia Clínica (HC) del paciente**.
    """)

def procesar_resultados_vni(ipap_act, epap_act, fr_paciente, fio2_act, fc_vni, glasgow, ph_vni, pco2_vni, po2_vni):
    pafi_vni = (po2_vni / (fio2_act / 100))
    hacor_score = calcular_score_hacor(fc_vni, ph_vni, glasgow, pafi_vni, fr_paciente)
    
    st.markdown("### 🛑 CONDUCTA MANDATORIA DE GUARDIA:")
    
    if "≤ 12" in glasgow or hacor_score > HACOR_LIMITE_FRACASO or fr_paciente > 40:
        st.error(f"""
        ### 🚨 FRACASO DE VNI (HACOR: {hacor_score} puntos)
        **INDICACIÓN:** SUSPENDER la VNI inmediatamente.
        *   El paciente presenta alto riesgo de parada respiratoria o incapacidad de proteger vía aérea.
        *   **Acción:** Inicie secuencia de intubación rápida y gestione de urgencia la cama en **UTI**. ¡No demore la intubación en el piso!
        """)
    elif ph_vni < 7.35 and pco2_vni > 45:
        nueva_ipap = ipap_act + 2
        st.warning(f"""
        ### ⚠️ AJUSTE POR ACIDEMIA HIPERCÁPNICA PERSISTENTE
        **Conducta inmediata:** **SUBIR LA IPAP EN +2 cmH2O** (Pasar a **{nueva_ipap} cmH2O**). 
        """)
    elif pafi_vni < 200 or po2_vni < 60:
        nueva_epap = epap_act + 2
        st.warning(f"""
        ### ⚠️ AJUSTE POR HIPOXEMIA PERSISTENTE
        **Conducta inmediata:** **SUBIR LA EPAP EN +1 o +2 cmH2O** (Pasar a **{nueva_epap} cmH2O**).
        """)
    else:
        st.success(f"""
        ### ✅ RESPUESTA EXITOSA A LA VNI (HACOR: {hacor_score} pts)
        **ESTADO:** Gases en rango aceptable, sin signos de fatiga ni asincronía.
        """)
        
    mostrar_recordatorio_hc()

def renderizar_seccion_vni():
    st.subheader("🛠️ Monitoreo de VNI (Evaluar a los 60 min)")
    
    with st.form("form_vni"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            ipap_act = st.number_input("IPAP programada (cmH2O)", min_value=6, value=12)
            epap_act = st.number_input("EPAP programada (cmH2O)", min_value=4, value=5)
            fr_paciente = st.number_input("Frecuencia Respiratoria (vpm)", min_value=10, value=28)
        with col_v2:
            fio2_act = st.slider("FiO2 actual del equipo (%)", min_value=21, max_value=100, value=35)
            fc_vni = st.number_input("Frecuencia Cardíaca (lpm)", min_value=40, value=90)
            glasgow = st.radio("Estado Neurológico (Glasgow):", 
                               ["15 (Lúcido)", "13-14 (Tendencia a somnolencia)", "≤ 12 (Estuporoso)"])
        
        st.write("**📄 Gases en Sangre Actuales:**")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            ph_vni = st.number_input("pH Arterial bajo VNI", value=7.30, step=0.01)
        with col_g2:
            pco2_vni = st.number_input("pCO2 (mmHg)", value=60)
        with col_g3:
            po2_vni = st.number_input("pO2 (mmHg)", value=60)
            
        calcular_btn = st.form_submit_button("Calcular Resultados VNI")
        
    if calcular_btn:
        procesar_resultados_vni(ipap_act, epap_act, fr_paciente, fio2_act, fc_vni, glasgow, ph_vni, pco2_vni, po2_vni)

def renderizar_seccion_cnaf():
    st.subheader("🛠️ Monitoreo de Alto Flujo")
    with st.form("form_cnaf"):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            sat_act = st.number_input("Saturación de O2 actual (%)", value=92)
        with col_c2:
            fio2_cnaf_act = st.slider("FiO2 programada (%)", min_value=21, max_value=100, value=40) / 100
            fr_cnaf_act = st.number_input("FR (vpm)", value=25)
        
        calcular_btn = st.form_submit_button("Calcular Resultados CNAF")
        
    if calcular_btn:
        rox_index = (sat_act / fio2_cnaf_act) / fr_cnaf_act
        st.write(f"**📈 Índice de ROX Calculado:** {rox_index:.2f}")
        # Aquí puedes agregar los warnings de ROX como estaban en el código original
