import streamlit as st
import streamlit.components.v1 as components
import base64
from logica.scores_quirurgicos import calcular_ariscat, clasificar_riesgo_ariscat, calcular_torrington, clasificar_riesgo_torrington

def renderizar_tab_quirurgico():
    st.header("Evaluación de Riesgo Quirúrgico")
    st.write("Modelos predictivos de complicaciones pulmonares postoperatorias (CPP).")
    
    sub1, sub2, sub3 = st.tabs(["1️⃣ ARISCAT (Clínico)", "2️⃣ Torrington (Neumonológico)", "3️⃣ 🖨️ Reporte Integrado"])
    
    # ==========================================
    # PESTAÑA 1: ARISCAT
    # ==========================================
    with sub1:
        st.subheader("Escala ARISCAT")
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
            
            if st.form_submit_button("Calcular Score ARISCAT"):
                st.session_state['score_a'] = calcular_ariscat(edad, spo2, infeccion, anemia, incision, duracion, emergencia)
            
        if 'score_a' in st.session_state:
            score_a = st.session_state['score_a']
            riesgo_a, tasa_a, color_a = clasificar_riesgo_ariscat(score_a)
            st.write("---")
            if color_a == "success": st.success(f"### Puntuación: **{score_a} puntos** ({riesgo_a})\n\n{tasa_a}")
            elif color_a == "warning": st.warning(f"### Puntuación: **{score_a} puntos** ({riesgo_a})\n\n{tasa_a}")
            else: st.error(f"### Puntuación: **{score_a} puntos** ({riesgo_a})\n\n{tasa_a}")

    # ==========================================
    # PESTAÑA 2: TORRINGTON
    # ==========================================
    with sub2:
        st.subheader("Escala Torrington-Henderson")
        with st.form("form_torrington"):
            st.write("**Seleccione los factores presentes:**")
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
                
            if st.form_submit_button("Calcular Score Torrington"):
                st.session_state['score_t'] = calcular_torrington(fvc_baja, relacion_baja, edad_mayor, obesidad, tabaquismo, sintomas, cirugia_riesgo)
            
        if 'score_t' in st.session_state:
            score_t = st.session_state['score_t']
            riesgo_t, tasa_t, color_t = clasificar_riesgo_torrington(score_t)
            st.write("---")
            if color_t == "success": st.success(f"### Puntuación: **{score_t} puntos** ({riesgo_t})")
            elif color_t == "warning": st.warning(f"### Puntuación: **{score_t} puntos** ({riesgo_t})")
            else: st.error(f"### Puntuación: **{score_t} puntos** ({riesgo_t})")

    # ==========================================
    # PESTAÑA 3: REPORTE INTEGRADO / PARCIAL
    # ==========================================
    with sub3:
        st.subheader("🖨️ Generación de Reporte Neumonológico")
        st.write("Imprima los scores calculados, o genere una planilla con los datos del paciente para completar a mano.")
        st.warning("Los datos ingresados aquí son efímeros: NO se guardan en ninguna base de datos.")
        
        with st.form("form_datos_paciente"):
            st.write("📝 **Completar datos del paciente e indicaciones**")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                nombre = st.text_input("Nombre y Apellido")
                dni = st.text_input("DNI / N° de Historia Clínica")
            with col_p2:
                fecha_eval = st.date_input("Fecha de Evaluación", format="DD/MM/YYYY")
                
            sugerencias_base = [
                "Kinesiología respiratoria pre y postquirúrgica.",
                "Aerosolterapia (Broncodilatadores) pautada.",
                "Cese tabáquico estricto (mínimo 4-8 semanas previas).",
                "Espirometría incentivada.",
                "Movilización precoz y analgesia óptima para evitar restricción ventilatoria.",
                "Profilaxis TVP."
            ]
            sugerencias = st.multiselect(
                "Sugerencias Neumonológicas:", 
                sugerencias_base, 
                default=["Kinesiología respiratoria pre y postquirúrgica.", "Aerosolterapia (Broncodilatadores) pautada.", "Profilaxis TVP."]
            )
            otros_comentarios = st.text_area("Observaciones adicionales:")
            st.form_submit_button("Aplicar Datos al Reporte")

        # --- CONSTRUCCIÓN DINÁMICA DEL REPORTE ---
        lista_sugerencias_html = "".join([f"<li>{s}</li>" for s in sugerencias])
        
        # Verificamos qué scores fueron calculados para sumarlos al HTML
        html_ariscat = ""
        if 'score_a' in st.session_state:
            score_a = st.session_state['score_a']
            riesgo_a, tasa_a, _ = clasificar_riesgo_ariscat(score_a)
            html_ariscat = f"""
            <p><strong><u>ESCALA CLÍNICA (ARISCAT):</u></strong></p>
            <p><strong>Puntuación:</strong> {score_a} puntos - <strong>{riesgo_a}</strong> <em>({tasa_a})</em></p>
            <br>
            """
            
        html_torrington = ""
        if 'score_t' in st.session_state:
            score_t = st.session_state['score_t']
            riesgo_t, tasa_t, _ = clasificar_riesgo_torrington(score_t)
            html_torrington = f"""
            <p><strong><u>ESCALA ESPIROMÉTRICA (TORRINGTON-HENDERSON):</u></strong></p>
            <p><strong>Puntuación:</strong> {score_t} puntos - <strong>{riesgo_t}</strong> <em>(Riesgo Estimado: {tasa_t})</em></p>
            <br>
            """

        # Armamos la estructura final
        html_reporte = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; border: 2px solid #4f8bf9; padding: 20px; border-radius: 10px; background-color: white; color: black;">
            <h3 style="text-align: center; margin-top: 0; color: #1e3d59;">Evaluación Neumonológica Prequirúrgica</h3>
            <hr style="border-top: 2px solid #4f8bf9;">
            <p><strong>Paciente:</strong> {nombre if nombre else '_________________________'} &nbsp;&nbsp;&nbsp; <strong>DNI/HC:</strong> {dni if dni else '________________'}</p>
            <p><strong>Fecha:</strong> {fecha_eval}</p>
            <br>
            {html_ariscat}
            {html_torrington}
            <p><strong><u>SUGERENCIAS E INDICACIONES:</u></strong></p>
            <ul>{lista_sugerencias_html}</ul>
            <p><strong>Observaciones:</strong> {otros_comentarios if otros_comentarios else 'Ninguna.'}</p>
            <br><br><br>
            <p style="text-align: right;"><em>Firma y Sello del Profesional: ___________________________</em></p>
        </div>
        """
        
        # Mostramos la previsualización en la web
        st.markdown(html_reporte, unsafe_allow_html=True)
        
        # --- MAGIA DE IMPRESIÓN LIMPIA ---
        st.info("💡 **Listo para imprimir:** Haga clic en el botón azul para generar el documento oficial.")
        
        b64_html = base64.b64encode(html_reporte.encode('utf-8')).decode('utf-8')
        javascript_print = f"""
        <script>
        function imprimirLimpio() {{
            const b64 = "{b64_html}";
            const decoded_html = decodeURIComponent(escape(window.atob(b64)));
            const ventana = window.open('', '_blank');
            ventana.document.write('<html><head><title>Reporte Médico</title></head><body>');
            ventana.document.write(decoded_html);
            ventana.document.write('</body></html>');
            ventana.document.close();
            setTimeout(function() {{
                ventana.print();
                ventana.close();
            }}, 250);
        }}
        </script>
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <button onclick="imprimirLimpio()" style="background-color: #4f8bf9; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 400px;">
            🖨️ Imprimir / Guardar PDF
            </button>
        </div>
        """
        components.html(javascript_print, height=80)
