import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Data Warehouse Financiero", layout="wide")

DB_NAME = 'dw_comercial_financiero.db'
engine = create_engine(f'sqlite:///{DB_NAME}')

# --- MOTOR DE INGESTA AL VUELO (ETL) ---
@st.cache_resource
def inicializar_data_warehouse():
    if not os.path.exists(DB_NAME):
        if os.path.exists('financial_data.csv'):
            df = pd.read_csv('financial_data.csv')
            
            # Limpieza de Calidad (Gobernanza)
            cols_monetarias = ['Account Balance', 'Deposits', 'Withdrawals', 'Investments']
            for col in cols_monetarias:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('[$,]', '', regex=True), errors='coerce').fillna(0)
            
            # Creación de IDs (Integridad Referencial)
            df['customer_id'] = df.groupby(['Age', 'Occupation', 'Address']).ngroup()
            df['transaction_id'] = range(1, len(df) + 1)
            
            # Carga a Modelo Estrella
            dim_clientes = df[['customer_id', 'Age', 'Occupation', 'Risk Tolerance', 'Income Level', 'Address', 'Employment Status']].drop_duplicates(subset=['customer_id'])
            fact_transacciones = df[['transaction_id', 'customer_id', 'Account Balance', 'Deposits', 'Withdrawals', 'Investments']]
            
            dim_clientes.to_sql('dim_clientes', engine, if_exists='replace', index=False)
            fact_transacciones.to_sql('fact_transacciones', engine, if_exists='replace', index=False)
            return "✅ Data Warehouse construido exitosamente."
    return "⚡ Conectado al Data Warehouse existente."

mensaje = inicializar_data_warehouse()

# --- INTERFAZ DEL DASHBOARD ---
st.title("🏛️ Análisis Comercial: Data Warehouse Financiero")
st.sidebar.success(mensaje)

# Consultas SQL Analíticas
query = """
SELECT f.*, c.Age, c.Occupation, c."Risk Tolerance", c."Income Level"
FROM fact_transacciones f
JOIN dim_clientes c ON f.customer_id = c.customer_id
"""
df_analisis = pd.read_sql(query, engine)

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Balance Total", f"$ {df_analisis['Account Balance'].sum():,.0f}")
c2.metric("Inversión Promedio", f"$ {df_analisis['Investments'].mean():,.2f}")
c3.metric("Nro. Clientes Únicos", len(df_analisis['customer_id'].unique()))

# --- GRÁFICO DE RIESGO OPTIMIZADO ---
st.subheader("Análisis de Riesgo y Comportamiento de Balance")

try:
    # Optimización de estructura para facilitar reportes
    df_plot = df_analisis.sample(n=min(5000, len(df_analisis))) 

    fig = px.box(
        df_plot, 
        x='Risk Tolerance', 
        y='Account Balance', 
        color='Income Level',
        title="Distribución de Balances (Vista Optimizada)",
        points=False, 
        notched=True 
    )
    
    fig.update_layout(height=500, template="plotly_white")
    
    # IMPORTANTE: Usamos un key único para evitar errores de duplicidad
    st.plotly_chart(fig, width='stretch', key="plot_riesgo_principal")

except Exception as e:
    st.error(f"Error de optimización: {e}")

# --- SECCIÓN DE DATOS (OPCIONAL) ---
# --- SECCIÓN DE DATOS (OPCIONAL) ---
with st.expander("Ver muestra de datos del Warehouse"):
    # Cambiamos use_container_width por width='stretch'
    st.dataframe(df_analisis.head(10), width='stretch')