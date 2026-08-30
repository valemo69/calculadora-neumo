import streamlit as st

def renderizar_tab_quirurgico():
    st.header("Evaluación de Riesgo Quirúrgico")
    st.write("Modelos predictivos de complicaciones pulmonares postoperatorias (CPP).")
    
    sub1, sub2 = st.tabs(["ARISCAT (Clínico-Quirúrgico)", "Torrington-Henderson (Neumonológico)"])
    
    with sub1:
        st.subheader("Escala ARISCAT")
        edad_sel = st.radio("Edad del paciente:", ["< 50 años (0 pts)", "51 - 80 años (3 pts)", "> 80 años (16 pts)"])
        
        if "< 50" in edad_sel:
            p_edad = 0
        elif "51 - 80" in edad_sel:
            p_edad = 3
        else:
            p_edad = 16
            
        st.info("🚧 Resto de la calculadora ARISCAT en desarrollo...")
        
    with sub2:
        st.subheader("Escala Torrington-Henderson")
        st.info("🚧 Calculadora Torrington en desarrollo...")
