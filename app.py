import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuración Inicial ---
st.set_page_config(
    page_title="Data Analyzer MVP",
    page_icon="📊",
    layout="wide"
)

# --- Títulos y Descripción ---
st.title("📊 Analizador Interactivo de Datos")
st.markdown("""
Esta herramienta permite la **ingesta, procesamiento y visualización automática** de bases de datos estructuradas.
Sube un archivo `.csv` o `.xlsx` para comenzar el análisis exploratorio.
""")

st.markdown("---")

# --- Módulo de Ingesta ---
archivo_subido = st.sidebar.file_uploader("📂 Cargar Base de Datos", type=["csv", "xlsx"])

if archivo_subido is not None:
    try:
        # Detección del formato y carga en DataFrame
        if archivo_subido.name.endswith('.csv'):
            df = pd.read_csv(archivo_subido)
        else:
            df = pd.read_excel(archivo_subido)
            
        st.sidebar.success("✅ Archivo cargado correctamente")
        
        # --- Dashboard Principal ---
        
        # 1. KPIs Generales
        st.subheader("1. Resumen Ejecutivo")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Registros", df.shape[0])
        col1.metric("Total Variables", df.shape[1])
        col1.metric("Datos Faltantes", df.isna().sum().sum())
        col1.metric("Duplicados", df.duplicated().sum())

        with st.expander("🔍 Ver Dataframe (Primeras 50 filas)"):
            st.dataframe(df.head(50), use_container_width=True)

        st.markdown("---")

        # 2. Motor de Gráficos
        st.subheader("2. Motor de Visualización")
        
        c_izq, c_der = st.columns([1, 3])
        
        with c_izq:
            st.info("Configuración de Ejes")
            columnas = df.columns.tolist()
            
            tipo_grafico = st.selectbox("Tipo de Gráfico", 
                ["Barras (Bar)", "Dispersión (Scatter)", "Línea (Line)", "Histograma", "Pastel (Pie)"])
            
            eje_x = st.selectbox("Eje X (Categoría/Tiempo)", columnas)
            eje_y = st.selectbox("Eje Y (Valor Numérico)", columnas, index=1 if len(columnas) > 1 else 0)
            
            color = st.selectbox("Agrupar por Color (Opcional)", ["Ninguno"] + columnas)
            col_sel = None if color == "Ninguno" else color

        with c_der:
            # Lógica de Plotly
            if tipo_grafico == "Barras (Bar)":
                fig = px.bar(df, x=eje_x, y=eje_y, color=col_sel, template="plotly_white")
            elif tipo_grafico == "Dispersión (Scatter)":
                fig = px.scatter(df, x=eje_x, y=eje_y, color=col_sel, template="plotly_white")
            elif tipo_grafico == "Línea (Line)":
                fig = px.line(df, x=eje_x, y=eje_y, color=col_sel, template="plotly_white")
            elif tipo_grafico == "Histograma":
                fig = px.histogram(df, x=eje_x, color=col_sel, template="plotly_white")
            elif tipo_grafico == "Pastel (Pie)":
                fig = px.pie(df, names=eje_x, values=eje_y, template="plotly_white")
            
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    # Pantalla de bienvenida cuando no hay datos
    st.info("👈 Utiliza el panel lateral para subir un archivo CSV o Excel.")
    st.warning("Demo: Asegúrate de que tu archivo tenga encabezados en la primera fila.")
