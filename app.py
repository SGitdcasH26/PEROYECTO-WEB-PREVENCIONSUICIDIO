import streamlit as st
import google.generativeai as genai
import PyPDF2
import os

# --- 1. CONFIGURACIÓN Y SEGURIDAD ---
st.set_page_config(page_title="Prevención Suicidio 061", page_icon="🚑")

# Recuperamos la contraseña y la API Key de los Secrets
CONTRASEÑA_CORRECTA = "061seguro" 
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Falta la API Key de Gemini en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- 2. SISTEMA DE LOGIN ---
if "acceso_concedido" not in st.session_state:
    st.session_state.acceso_concedido = False

if not st.session_state.acceso_concedido:
    st.title("🔒 Acceso Restringido")
    clave = st.text_input("Introduce la contraseña para acceder:", type="password")
    if st.button("Entrar"):
        if clave == CONTRASEÑA_CORRECTA:
            st.session_state.acceso_concedido = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

# --- 3. LECTURA DE DOCUMENTOS PDF ---
@st.cache_resource 
def extraer_texto_pdfs():
    texto_total = ""
    archivos_pdf = [f for f in os.listdir('.') if f.endswith('.pdf')]
    for archivo in archivos_pdf:
        try:
            with open(archivo, "rb") as f:
                lector = PyPDF2.PdfReader(f)
                for pagina in lector.pages:
                    texto_total += pagina.extract_text() + "\n"
        except Exception as e:
            st.warning(f"No se pudo leer el archivo {archivo}: {e}")
    return texto_total

contexto_protocolos = extraer_texto_pdfs()

# --- 4. BARRA LATERAL (LISTADO DE PROTOCOLOS) ---
with st.sidebar:
    st.markdown("### 📚 Protocolos y Procedimientos")
    st.markdown("Documentos cargados actualmente:")
    
    # Buscamos todos los archivos PDF en el repositorio
    archivos_pdf = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if archivos_pdf:
        for pdf in archivos_pdf:
            st.markdown(f"- 📄 **{pdf}**")
    else:
        st.write("No se han encontrado archivos PDF.")

# --- 5. INTERFAZ DE CHAT ---
st.markdown("# **Atención a personas con conducta suicida y sus familias**")
st.markdown("##### Cómo contribuir a prevenir el suicidio desde la atención emergente prehospitalaria")
st.markdown('<p style="background-color: #FFFF00; color: black; display: inline; padding: 2px; font-size: 0.9em; font-weight: bold;">Haz tu consulta aquí</p>', unsafe_allow_html=True)
st.write("") 

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

if pregunta := st.chat_input("Escribe tu consulta sobre el protocolo..."):
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando manuales..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
            Eres un asistente experto en protocolos médicos de emergencias (061).
            Utiliza exclusivamente el siguiente texto extraído de los manuales para responder la duda del usuario.
            Si la respuesta no está en el texto, indícalo educadamente.
            
            TEXTO DE PROTOCOLOS:
            {contexto_protocolos}
            
            PREGUNTA:
            {pregunta}
            """
            respuesta = model.generate_content(prompt)
            st.markdown(respuesta.text)
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta.text})
