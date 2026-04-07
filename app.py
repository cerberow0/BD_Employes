import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client

# URL del logo proporcionado
LOGO_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBE18TlcXuZbRAr7-Q8k_CnAb31sz3XtAQvA&s"

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Directorio Aguas - Gintelco",
    page_icon="💧",
    layout="centered"
)

# --- CSS PARA FONDO NEGRO TOTAL ---

# --- 2. CSS PROFESIONAL (Actualizado para Sidebar) ---
# --- 2. CSS PROFESIONAL (Actualizado para Sidebar) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Fondo General */
    .stApp, .main, .block-container {
        background-color: #020c1b !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Cabecera hero */
    .header-wrapper {
        background: linear-gradient(135deg, #0a192f 0%, #0d2137 60%, #0a192f 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 24px;
    }
    .header-text h1 { color: #e6f1ff !important; margin: 0; font-size: 1.8rem !important; }
    .header-text p { color: #5f8ac7 !important; margin: 0; text-transform: uppercase; font-size: 0.85rem !important; }

    /* Placeholder cursiva */
    input::placeholder { font-style: italic !important; opacity: 0.7; }
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

    # --- 4. CABECERA ---
    st.markdown(f"""
    <div class="header-wrapper">
        <img src="{LOGO_URL}" width="80" style="border-radius:12px;" />
        <div class="header-text">
            <h1>💧 Directorio</h1>
            <p>Sistema Interno de Consulta Rápida</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 5. BUSCADOR ---
    busqueda = st.text_input(
        "Buscar funcionario",
        placeholder="Ejemplo: Diana o Oscar",
    )

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
                        phone = emp.get('phone', 'N/A')
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"📍 **Area:** {emp.get('sub_process', 'N/A')}")
                        with col2:
                            st.markdown(f"📍 **Sede:** {emp.get('sede', 'N/A')}")
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            st.markdown(f"🖥️ **Máquina:** {emp.get('machine_name', 'N/A')}")
                        with c2:
                            st.markdown(f"🌐 **IP:**<br>`{emp.get('ip_target', 'N/A')}`", unsafe_allow_html=True)
                        with c3:
                            st.markdown(f"📞 **Teléfono:**<br> {phone}", unsafe_allow_html=True)
                        with c4:
                            if phone and phone != 'N/A':
                                clean_phone = ''.join(filter(str.isdigit, str(phone)))
                                whatsapp_url = f"https://wa.me/57{clean_phone}"
                                clean_phone = ''.join(filter(str.isdigit, str(phone)))
                                whatsapp_url = f"https://wa.me/57{clean_phone}"
                                st.markdown(
                                    f'**Whatsapp:**<br>'
                                    f'<a href="{whatsapp_url}" target="_blank">'
                                    f'<img src="https://img.icons8.com/color/20/whatsapp.png"/> Abrir chat</a>', 
                                    unsafe_allow_html=True
                                )
                            else:
                                st.markdown("💬 **Whatsapp:** N/A")
            else:
                st.warning("No se encontraron resultados.")

        except Exception as e:
            st.error(f"Error: {e}")
    
    st.markdown("---")
    st.caption("v1.1 - Nicolas & Gintelo - 2026")