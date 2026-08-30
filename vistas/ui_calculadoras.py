import streamlit as st
from logica.calculadoras_sala import calcular_curb65, clasificar_curb65, calcular_clearance_creatinina
from logica.calculadoras_sala import calcular_deficit_sodio, calcular_deficit_agua_libre, calcular_calcio_corregido
from logica.calculadoras_sala import calcular_wells_tep, clasificar_wells_tep, calcular_spesi, clasificar_spesi

def renderizar_tab_calculadoras():
    st.header("🧮 Calculadoras de Sala General")
    st.write("Herramientas rápidas para la toma de decisiones clínicas y ajuste de fármacos.")
    
    sub1, sub2, sub3, sub4 = st.tabs(["🩺 CURB-65", "💧 Clearance", "🧪 Medio Interno", "🩸 TEP (Wells/PESI)"])
    
    # ==========================================
    # PESTAÑA 1: CURB-65
    # ==========================================
    with sub1:
        st.subheader("Score CURB-65 para Neumonía")
        with st.form("form_curb65"):
            col1, col2 = st.columns(2)
            with col1:
                confusion = st.radio("C - Confusión mental reciente:", ["No", "Sí"])
                urea = st.number_input("U - Urea en sangre (mg/dL):", min_value=0, value=30)
                fr = st.number_input("R - Frecuencia Respiratoria (vpm):", min_value=10, value=20)
            with col2:
                pa_sistolica = st.number_input("Sistólica (PAS):", min_value=50, value=120)
                pa_diastolica = st.number_input("Diastólica (PAD):", min_value=30, value=80)
                edad = st.number_input("65 - Edad (años):", min_value=18, value=50)
                
            if st.form_submit_button("Calcular CURB-65"):
                score = calcular_curb65(confusion, urea, fr, pa_sistolica, pa_diastolica, edad)
                riesgo, conducta, color = clasificar_curb65(score)
                st.write("---")
                if color == "success": st.success(f"### Puntos: **{score}** - {riesgo}\n\n**Conducta:** {conducta}")
                elif color == "warning": st.warning(f"### Puntos: **{score}** - {riesgo}\n\n**Conducta:** {conducta}")
                else: st.error(f"### Puntos: **{score}** - {riesgo}\n\n**Conducta:** {conducta}")

    # ==========================================
    # PESTAÑA 2: CLEARANCE DE CREATININA
    # ==========================================
    with sub2:
        st.subheader("Clearance de Creatinina (Cockcroft-Gault)")
        with st.form("form_clearance"):
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                sexo = st.radio("Sexo biológico:", ["Hombre", "Mujer"])
                edad_c = st.number_input("Edad (años):", min_value=18, value=60, key="edad_c")
            with col_c2:
                peso = st.number_input("Peso (kg):", min_value=30.0, value=70.0, step=0.1)
                creatinina = st.number_input("Creatinina sérica (mg/dL):", min_value=0.1, value=1.0, step=0.1)
                
            if st.form_submit_button("Calcular Clearance"):
                crcl = calcular_clearance_creatinina(edad_c, peso, creatinina, sexo)
                st.write("---")
                st.info(f"### TFG estimada: **{crcl:.1f} mL/min**")
                if crcl < 30: st.error("⚠️ **Insuficiencia renal severa.** Ajustar fármacos.")
                elif crcl < 60: st.warning("⚠️ **Insuficiencia renal moderada.** Revisar dosis.")
                else: st.success("✅ Función renal conservada.")

    # ==========================================
    # PESTAÑA 3: MEDIO INTERNO
    # ==========================================
    with sub3:
        st.subheader("Reposición de Electrolitos y Correcciones")
        
        with st.expander("🧂 Déficit de Sodio y Agua Libre", expanded=True):
            with st.form("form_sodio"):
                col_n1, col_n2 = st.columns(2)
                with col_n1:
                    sexo_na = st.radio("Sexo:", ["Hombre", "Mujer"], key="sexo_na")
                    edad_na = st.number_input("Edad:", min_value=18, value=60, key="edad_na")
                    peso_na = st.number_input("Peso (kg):", min_value=30.0, value=70.0, step=0.1, key="peso_na")
                with col_n2:
                    na_actual = st.number_input("Na medido (mEq/L):", min_value=100, max_value=180, value=130)
                    na_deseado = st.number_input("Na objetivo (mEq/L):", min_value=120, max_value=145, value=140)
                    st.caption("No reponer > 8-10 mEq/L en 24h.")
                
                if st.form_submit_button("Calcular Sodio/Agua"):
                    st.write("---")
                    if na_actual < 135:
                        deficit, act = calcular_deficit_sodio(peso_na, sexo_na, edad_na, na_actual, na_deseado)
                        st.warning(f"### 📉 Hiponatremia")
                        st.write(f"- Agua Corporal Total: **{act:.1f} L**")
                        st.write(f"- Déficit de Sodio: **{deficit:.1f} mEq** para llegar a {na_deseado} mEq/L.")
                    elif na_actual > 145:
                        deficit_agua = calcular_deficit_agua_libre(peso_na, sexo_na, edad_na, na_actual)
                        st.error(f"### 📈 Hipernatremia")
                        st.write(f"- Déficit de Agua Libre: **{deficit_agua:.2f} Litros**.")
                    else:
                        st.success("✅ Sodio normal.")
        
        with st.expander("🥛 Calcio Corregido por Albúmina"):
            with st.form("form_calcio"):
                c1, c2 = st.columns(2)
                with c1:
                    calcio_medido = st.number_input("Calcio Total (mg/dL):", min_value=4.0, max_value=15.0, value=8.0, step=0.1)
                with c2:
                    albumina = st.number_input("Albúmina sérica (g/dL):", min_value=1.0, max_value=6.0, value=2.5, step=0.1)
                
                if st.form_submit_button("Calcular Calcio Corregido"):
                    ca_corregido = calcular_calcio_corregido(calcio_medido, albumina)
                    st.info(f"### Calcio Real Corregido: **{ca_corregido:.2f} mg/dL**")

    # ==========================================
    # PESTAÑA 4: TEP (WELLS Y SPESI)
    # ==========================================
    with sub4:
        st.subheader("Tromboembolismo Pulmonar (TEP)")
        st.write("Estratificación para diagnóstico inicial y decisión de internación.")

        with st.expander("🔍 Score de Wells (Probabilidad Diagnóstica)", expanded=True):
            with st.form("form_wells"):
                st.write("**Criterios Clínicos:**")
                col_w1, col_w2 = st.columns(2)
                with col_w1:
                    tvp = st.checkbox("Signos clínicos de TVP (3 pts)")
                    diag_alt = st.checkbox("Diag. alternativo menos probable que TEP (3 pts)")
                    fc_alta = st.checkbox("Frecuencia cardíaca > 100 lpm (1.5 pts)")
                    inmovilizacion = st.checkbox("Inmovilización o cirugía en últimas 4 semanas (1.5 pts)")
                with col_w2:
                    tep_previo = st.checkbox("TEP o TVP previa (1.5 pts)")
                    hemoptisis = st.checkbox("Hemoptisis (1 pt)")
                    cancer = st.checkbox("Cáncer activo (1 pt)")

                if st.form_submit_button("Calcular Score de Wells"):
                    score_w = calcular_wells_tep(tvp, diag_alt, fc_alta, inmovilizacion, tep_previo, hemoptisis, cancer)
                    riesgo_w, conducta_w, color_w = clasificar_wells_tep(score_w)
                    st.write("---")
                    if color_w == "success": st.success(f"### Puntos: **{score_w}** - {riesgo_w}\n\n**Conducta:** {conducta_w}")
                    else: st.error(f"### Puntos: **{score_w}** - {riesgo_w}\n\n**Conducta:** {conducta_w}")

        with st.expander("🏥 Score sPESI (Pronóstico e Internación)"):
            with st.form("form_spesi"):
                st.write("**Predictores de mortalidad a 30 días:**")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    edad_mayor = st.checkbox("Edad > 80 años (1 pt)")
                    cancer_s = st.checkbox("Cáncer activo (1 pt)")
                    epoc_ic = st.checkbox("IC crónica o enf. pulmonar crónica (1 pt)")
                with col_s2:
                    fc_alta_s = st.checkbox("Frecuencia cardíaca ≥ 110 lpm (1 pt)")
                    pas_baja = st.checkbox("Presión sistólica < 100 mmHg (1 pt)")
                    sat_baja = st.checkbox("Saturación O2 < 90% (1 pt)")

                if st.form_submit_button("Calcular sPESI"):
                    score_s = calcular_spesi(edad_mayor, cancer_s, epoc_ic, fc_alta_s, pas_baja, sat_baja)
                    riesgo_s, conducta_s, color_s = clasificar_spesi(score_s)
                    st.write("---")
                    if color_s == "success": st.success(f"### Puntos: **{score_s}** - {riesgo_s}\n\n**Conducta:** {conducta_s}")
                    else: st.error(f"### Puntos: **{score_s}** - {riesgo_s}\n\n**Conducta:** {conducta_s}")
