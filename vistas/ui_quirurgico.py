import streamlit as st
# Fíjate que ahora también importamos Torrington en esta línea:
from logica.scores_quirurgicos import calcular_ariscat, clasificar_riesgo_ariscat, calcular_torrington, clasificar_riesgo_torrington

def renderizar_tab_quirurgico():
    st.header("Evaluación de Riesgo Quirúrgico")
    st.write("Modelos predictivos de complicaciones pulmonares postoperatorias (CPP).")
    
    sub1, sub2 = st.tabs(["ARISCAT (Clínico-Quirúrgico)", "Torrington-Henderson (Neumonológico)"])
    
    with sub1:
        st.subheader("Escala ARISCAT")
        st.write("Calcula el riesgo de complicaciones pulmonares postoperatorias.")
        
        with st.form("form_ariscat"):
            col1, col2 = st.columns(2)
            
            with col1:
                edad = st.radio("1. Edad del paciente:", ["≤ 50 años", "51 - 80 años", "> 80 años"])
                spo2 = st.radio("2. SpO2 preoperatoria (aire ambiente):", ["≥ 96%", "91 - 95%", "≤ 90%"])
                infeccion = st.radio("3. Infección respiratoria (< 1 mes):", ["No", "Sí"])
                anemia = st.radio("4. Anemia preoperatoria (Hb ≤ 10 g/dL):", ["No", "Sí"])
                
            with col2:
                incision = st.radio("5. Sitio de incisión quirúrgica:", ["Periférica / Abdominal baja", "Abdominal alta", "Intratorácica"])
                duracion = st.radio("6. Duración estimada de la cirugía:", ["< 2 horas", "2 - 3 horas", "> 3 horas"])
                emergencia = st.radio("7. Procedimiento de emergencia:", ["No", "Sí"])
            
            calcular_btn = st.form_submit_button("Calcular Score ARISCAT")
            
        if calcular_btn:
            score = calcular_ariscat(edad, spo2, infeccion, anemia, incision, duracion, emergencia)
            riesgo, tasa, color = clasificar_riesgo_ariscat(score)
            
            st.write("---")
            st.markdown(f"### Puntuación Total: **{score} puntos**")
            
            if color == "success":
                st.success(f"**Clasificación: {riesgo}**\n\n{tasa}")
            elif color == "warning":
                st.warning(f"**Clasificación: {riesgo}**\n\n{tasa}")
            else:
                st.error(f"**Clasificación: {riesgo}**\n\n{tasa}")

    with sub2:
        st.subheader("Escala Torrington-Henderson")
        st.write("Estratificación de riesgo basada en clínica y espirometría prequirúrgica.")
        
        with st.form("form_torrington"):
            st.write("**Seleccione los factores presentes (Checklist):**")
            col_t1, col_t2 = st.columns(2)
            
            with col_t1:
                fvc_baja = st.checkbox("FVC < 50% del valor predicho (1 pt)")
                relacion_baja = st.checkbox("FEV1/FVC < 65% (1 pt)")
                edad_mayor = st.checkbox("Edad > 65 años (1 pt)")
                obesidad = st.checkbox("Obesidad (IMC > 27) (1 pt)")
                
            with col_t2:
                tabaquismo = st.checkbox("Tabaquismo activo o historia reciente (1 pt)")
                sintomas = st.checkbox("Síntomas respiratorios (Tos / Expectoración) (1 pt)")
                cirugia_riesgo = st.checkbox("Cirugía intratorácica o abdominal alta (2 pts)")
                
            calcular_btn_t = st.form_submit_button("Calcular Score Torrington")
            
        if calcular_btn_t:
            score_t = calcular_torrington(fvc_baja, relacion_baja, edad_mayor, obesidad, tabaquismo, sintomas, cirugia_riesgo)
            riesgo_t, tasa_t, color_t = clasificar_riesgo_torrington(score_t)
            
            st.write("---")
            st.markdown(f"### Puntuación Total: **{score_t} puntos**")
            
            if color_t == "success":
                st.success(f"**Clasificación: {riesgo_t}**\n\n{tasa_t}")
            elif color_t == "warning":
                st.warning(f"**Clasificación: {riesgo_t}**\n\n{tasa_t}")
            else:
                st.error(f"**Clasificación: {riesgo_t}**\n\n{tasa_t}")
