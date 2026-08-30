import streamlit as st
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
            
        # Guardamos el score en memoria para que no se borre al tipear el nombre
        if calcular_btn_t:
            st.session_state['score_t'] = calcular_torrington(fvc_baja, relacion_baja, edad_mayor, obesidad, tabaquismo, sintomas, cirugia_riesgo)
            
        # Si ya hay un score calculado, mostramos los resultados y el módulo de impresión
        if 'score_t' in st.session_state:
            score_t = st.session_state['score_t']
            riesgo_t, tasa_t, color_t = clasificar_riesgo_torrington(score_t)
            
            st.write("---")
            if color_t == "success":
                st.success(f"### Puntuación Total: **{score_t} puntos** ({riesgo_t})")
            elif color_t == "warning":
                st.warning(f"### Puntuación Total: **{score_t} puntos** ({riesgo_t})")
            else:
                st.error(f"### Puntuación Total: **{score_t} puntos** ({riesgo_t})")

            st.write("---")
            st.subheader("🖨️ Generar Reporte para Historia Clínica")
            st.warning("Los datos ingresados aquí son efímeros: NO se guardan en ninguna base de datos por protección al paciente.")
            
            with st.expander("📝 Completar datos del paciente e indicaciones", expanded=True):
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    nombre = st.text_input("Nombre y Apellido")
                    dni = st.text_input("DNI / N° de Historia Clínica")
                with col_p2:
                    fecha_nac = st.date_input("Fecha de Evaluación", format="DD/MM/YYYY")
                    
                sugerencias_base = [
                    "Kinesiología respiratoria pre y postquirúrgica.",
                    "Aerosolterapia (Broncodilatadores) pautada.",
                    "Cese tabáquico estricto (mínimo 4-8 semanas previas).",
                    "Espirometría incentivada.",
                    "Movilización precoz y analgesia óptima para evitar restricción ventilatoria.",
                    "Profilaxis TVP."
                ]
                
                sugerencias = st.multiselect(
                    "Sugerencias Neumonológicas (puede agregar o quitar):", 
                    sugerencias_base, 
                    default=["Kinesiología respiratoria pre y postquirúrgica.", "Aerosolterapia (Broncodilatadores) pautada.", "Espirometría incentivada."]
                )
                
                otros_comentarios = st.text_area("Observaciones adicionales:")

            st.info("💡 **Presione Ctrl + P** (o Cmd + P en Mac) para imprimir el siguiente reporte y adjuntarlo a la HC.")
            
            # Formato visual de Reporte Médico (HTML y CSS)
            lista_sugerencias_html = "".join([f"<li>{s}</li>" for s in sugerencias])
            
            st.markdown(f"""
            <div style="border: 2px solid #4f8bf9; padding: 20px; border-radius: 10px; background-color: #f0f8ff;">
                <h3 style="text-align: center; margin-top: 0; color: #1e3d59;">Evaluación Neumonológica Prequirúrgica</h3>
                <hr style="border-top: 1px solid #4f8bf9;">
                <p><strong>Paciente:</strong> {nombre if nombre else '_________________________'} &nbsp;&nbsp;&nbsp; <strong>DNI/HC:</strong> {dni if dni else '________________'}</p>
                <p><strong>Fecha:</strong> {fecha_nac}</p>
                <br>
                <p><strong><u>ESCALA DE TORRINGTON-HENDERSON:</u></strong></p>
                <p><strong>Puntuación obtenida:</strong> {score_t} puntos - <strong>{riesgo_t}</strong></p>
                <p><em>Riesgo Estimado: {tasa_t}</em></p>
                <br>
                <p><strong><u>SUGERENCIAS E INDICACIONES:</u></strong></p>
                <ul>
                    {lista_sugerencias_html}
                </ul>
                <p><strong>Observaciones:</strong> {otros_comentarios if otros_comentarios else 'Ninguna.'}</p>
                <br><br><br>
                <p style="text-align: right;"><em>Firma y Sello del Profesional: ___________________________</em></p>
            </div>
            """, unsafe_allow_html=True)
