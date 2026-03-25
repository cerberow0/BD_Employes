import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client

# 1. Configuración de la interfaz (Modo Móvil)
st.set_page_config(
    page_title="Directorio Aguas y Aguas",
    page_icon="💧",
    layout="centered"
)

# 2. Carga de credenciales
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Validar que existan las llaves antes de conectar
if not url or not key:
    st.error("⚠️ Error: No se encontraron las credenciales en el archivo .env")
    st.info("Asegúrate de que el archivo .env tenga SUPABASE_URL y SUPABASE_KEY")
else:
    # Conexión a Supabase
    supabase = create_client(url, key)

    # 3. Diseño de la App
    st.title("🔍 Directorio de Funcionarios")
    st.write("Sistema de consulta rápida - PWA")
    
    # Campo de búsqueda
    busqueda = st.text_input("Escribe el nombre a buscar:", placeholder="Ej: Diana o Oscar")

    if busqueda:
        # Ejecutar búsqueda con iLike (ignora mayúsculas/minúsculas)
        # El f"%{busqueda}%" permite encontrar el nombre en cualquier parte de la celda
        try:
            res = supabase.table("Employes").select("*").ilike("name", f"%{busqueda}%").execute()
            
            if res.data:
                st.success(f"Se encontraron {len(res.data)} coincidencias:")
                
                # Mostrar cada funcionario en una tarjeta expandible
                for emp in res.data:
                    with st.expander(f"👤 {emp['name']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**📧 Correo:**\n{emp.get('mail', 'N/A')}")
                            st.markdown(f"**📍 Subproceso:**\n{emp.get('sub_proceso', 'No asignado')}")
                        with col2:
                            st.markdown(f"**🖥️ Máquina:**\n{emp.get('machine_name', 'N/A')}")
                            st.markdown(f"**🌐 IP:**\n{emp.get('ip_target', 'N/A')}")
            else:
                st.warning(f"No hay resultados para '{busqueda}'")
        
        except Exception as e:
            st.error(f"Hubo un error en la consulta: {e}")

    # Pie de página
    st.markdown("---")
    st.caption("v1.0 - Desarrollado para uso interno")