import streamlit as st

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Protocolo Prehospitalario - 061", page_icon="🚑", layout="centered")

# --- 2. SISTEMA DE SEGURIDAD (CONTRASEÑA) ---
# PUEDES CAMBIAR "061seguro" POR LA CLAVE QUE TÚ QUIERAS
CONTRASEÑA_CORRECTA = "061seguro"

# Comprobamos si el usuario ya ha puesto la clave correcta
if "acceso_concedido" not in st.session_state:
    st.session_state.acceso_concedido = False

# Si no tiene acceso, mostramos la pantalla de bloqueo
if not st.session_state.acceso_concedido:
    st.markdown("<h2 style='text-align: center; color: #2C3E50;'>🔒 Acceso Restringido</h2>", unsafe_allow_html=True)
    st.warning("Esta es un área de desarrollo e investigación clínica. Por favor, introduce la clave de acceso.")
    
    clave_introducida = st.text_input("Contraseña:", type="password")
    
    if st.button("Entrar"):
        if clave_introducida == CONTRASEÑA_CORRECTA:
            st.session_state.acceso_concedido = True
            st.rerun() 
        else:
            st.error("❌ Contraseña incorrecta. Inténtalo de nuevo.")
    
    st.stop()

# =====================================================================
# 🚑 ÁREA PROTEGIDA: TODO LO DE ABAJO SOLO SE VE CON CONTRASEÑA
# =====================================================================

# --- 3. INTERFAZ PRINCIPAL DEL PROTOCOLO ---
st.title("🚑 Protocolo Prehospitalario: Conducta Suicida")
st.markdown("### Guía Rápida de Atención y Evidencia Clínica")

st.success("¡Acceso concedido! Bienvenida a tu espacio de investigación, Susana.")

st.markdown("""
---
#### 🛠️ Estructura del Proyecto:
Esta plataforma integrará tres pilares fundamentales:
1. **Guía Rápida de Protocolos:** Respuestas directas basadas en tus documentos de evidencia.
2. **Observatorio Estadístico:** Análisis de peticiones de asistencia en Andalucía.
3. **Gestión de la Evidencia:** Repositorio de documentos técnicos de interés.
""")

st.info("💡 **Próximo paso:** Una vez verifiques que la contraseña funciona, empezaremos a integrar tus documentos.")
