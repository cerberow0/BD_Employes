import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client

# URL del logo proporcionado
LOGO_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBE18TlcXuZbRAr7-Q8k_CnAb31sz3XtAQvA&s"

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Directorio Aguas y Aguas",
    page_icon="💧",
    layout="centered"
)

# --- CSS PARA FONDO NEGRO TOTAL ---
st.markdown("""
<style>
    /* Fondo principal negro puro */
    .stApp {
        background-color: #000000 !important;
    }

    /* Forzar que todos los contenedores principales sean negros */
    .main, .block-container, div[data-testid="stVerticalBlock"] {
        background-color: #000000 !important;
    }

    /* Inputs de búsqueda en gris muy oscuro para que se vean */
    div[data-baseweb="input"] {
        background-color: #0d0d0d !important;
        border-radius: 8px;
        border: 1px solid #1f1f1f !important;
    }

    /* Texto blanco en toda la app */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #ffffff !important;
    }

    /* Estilo de los Expanders (Tarjetas de funcionarios) */
    .st-emotion-cache-1f87s0h {
        background-color: #000000 !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 10px;
    }

    /* Línea divisoria sutil */
    hr {
        border-top: 1px solid #1f1f1f !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CARGA DE CREDENCIALES ---
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    st.error("Faltan credenciales en el archivo .env")
else:
    supabase = create_client(url, key)

    # --- 3. CABECERA ---
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(LOGO_URL, width=120)
    with col2:
        st.write("")
        st.title("💧 Directorio")
        st.write("_Sistema Interno de Consulta Rápida_")
    
    st.markdown("---")
    
    # --- 4. BUSCADOR ---
    busqueda = st.text_input("Buscar funcionario por nombre:", placeholder="Ej: Diana o Oscar")

    if busqueda:
        try:
            res = supabase.table("Employes").select("*").ilike("name", f"%{busqueda}%").execute()
            
            if res.data:
                # Ordenar alfabéticamente
                registros = sorted(res.data, key=lambda x: x['name'])
                
                st.markdown(f"**Resultados ({len(registros)}):**")
                
                for emp in registros:
                    with st.expander(f"👤 {emp['name'].title()}"):
                        st.markdown(f"📧 **Correo:** {emp.get('mail', 'N/A')}")
                        st.markdown(f"📍 **Proceso:** {emp.get('sub_process', 'N/A')}")
                        
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.markdown(f"🖥️ **Máquina:** {emp.get('machine_name', 'N/A')}")
                        with c2:
                            st.markdown(f"🌐 **IP:** {emp.get('ip_target', 'N/A')}")
                        with c3:
                            st.markdown(f"📞 **Phone:** {emp.get('phone', 'N/A')}")
            else:
                st.warning("No se encontraron resultados.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.caption("v1.1 - Nicolas - BETA 2026")