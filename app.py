import streamlit as st
import google.generativeai as genai

st.title("🔍 Escáner de Modelos de Gemini")
st.markdown("Vamos a ver qué cerebros tienes disponibles en tu cuenta...")

try:
    # Leemos la llave de tu caja fuerte
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Le pedimos a Google la lista de modelos
    modelos = genai.list_models()
    
    st.success("¡Conexión a Google exitosa! Estos son tus modelos:")
    
    for m in modelos:
        if 'generateContent' in m.supported_generation_methods:
            st.info(m.name)
            
except Exception as e:
    st.error(f"Error al conectar: {e}")
