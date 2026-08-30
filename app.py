import streamlit as st
import os

# Importamos las vistas que creamos en los otros archivos
from vistas.ui_vni import renderizar_seccion_vni, renderizar_seccion_cnaf
from vistas.ui_quirurgico import renderizar_tab_quirurgico

st.set_page_config(page_title="Cetrángolo NeumoCheck", page_icon="🫁", layout="centered")

def mostrar_cabecera():
    # Usamos el nombre exacto de la imagen que tienes en el repo
    if os.path.exists("Logo Cetra.png"):
        st.image("Logo Cetra.png", width=140)
        
    st.write("🏥 **Hospital de Agudos y Crónicos Dr. Antonio A. Cetrángolo**")
    st.title("🫁 Cetrángolo NeumoCheck")
    st.caption("Guía de Decisiones de Guardia y Soporte Respiratorio - Sala General (No UTI)")
    st.info("⚠️ Recordatorio: No ingrese datos filiatorios del paciente (Nombres, DNI). Solo variables clínicas anónimas.")

def renderizar_tab_guia():
    st.header("📋 Protocolo de Soporte No Invasivo en Guardia")
    st.write("Asistente paso a paso para disminuir errores en el piso de internación.")
    
    soporte = st.selectbox("1. Seleccione la terapia actual del paciente:", 
                           ["[Seleccionar]", "Ventilación No Invasiva (VNI - BiPAP/CPAP)", "Cánula Nasal de Alto Flujo (CNAF)"])
    
    if soporte == "Ventilación No Invasiva (VNI - BiPAP/CPAP)":
        renderizar_seccion_vni()
    elif soporte == "Cánula Nasal de Alto Flujo (CNAF)":
        renderizar_seccion_cnaf()

def main():
    mostrar_cabecera()
    
    # Creamos las pestañas principales
    tab_guia, tab_quirurgico, tab_calculadoras = st.tabs([
        "🛟 Guía VNI / Alto Flujo", 
        "🩺 Riesgo Quirúrgico", 
        "🧮 Calculadoras de Sala"
    ])
    
    with tab_guia:
        renderizar_tab_guia()
        
    with tab_quirurgico:
        renderizar_tab_quirurgico()
        
    with tab_calculadoras:
        st.info("🚧 Calculadoras de Sala en desarrollo...")

if __name__ == "__main__":
    main()
