import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Conexión al repositorio centralizado
engine = create_engine('sqlite:///dw_comercial_financiero.db')

def run_etl_pro():
    print("🚀 Iniciando Pipeline ETL Profesional...")
    
    # 1. EXTRACCIÓN
    df = pd.read_csv('financial_data.csv')
    
    # 2. TRANSFORMACIÓN (Gobernanza y Calidad de Datos)
    print("🛠️ Aplicando Reglas de Calidad y Creando Identificadores...")

    # --- PASO CRÍTICO: Limpieza de columnas monetarias ANTES de modelar ---
    cols_monetarias = ['Account Balance', 'Deposits', 'Withdrawals', 'Investments']
    for col in cols_monetarias:
        # Quitamos símbolos y convertimos a número para permitir cálculos SQL
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('[$,]', '', regex=True), errors='coerce').fillna(0)
    
    # Generamos IDs para integridad referencial (Modelo Estrella)
    df['customer_id'] = df.groupby(['Age', 'Occupation', 'Address']).ngroup()
    df['transaction_id'] = range(1, len(df) + 1)
    
    # 3. DISEÑO DE MODELO DIMENSIONAL (Estrella)
    
    # Dimensión: Clientes (Atributos Maestros - MDM)
    dim_clientes = df[[
        'customer_id', 'Age', 'Occupation', 'Risk Tolerance', 
        'Income Level', 'Address', 'Employment Status'
    ]].drop_duplicates(subset=['customer_id'])
    
    # Dimensión: Productos de Préstamo
    dim_prestamos = df[[
        'customer_id', 'Loan Purpose', 'Loan Term (Months)', 
        'Interest Rate', 'Loan Status'
    ]].copy()
    
    # Tabla de Hechos: Transacciones (Optimización para reportes)
    fact_transacciones = df[[
        'transaction_id', 'customer_id', 'Account Balance', 
        'Deposits', 'Withdrawals', 'Investments', 'Transaction Description'
    ]].copy()

    # 4. CARGA (Consolidación en Repositorio Centralizado)
    print("📥 Consolidando tablas en el Data Warehouse...")
    dim_clientes.to_sql('dim_clientes', engine, if_exists='replace', index=False)
    dim_prestamos.to_sql('dim_prestamos', engine, if_exists='replace', index=False)
    fact_transacciones.to_sql('fact_transacciones', engine, if_exists='replace', index=False)
    
    print("💎 Calidad de datos aplicada: Columnas monetarias convertidas a Float.") 
    print("✅ Proceso Exitoso: Modelo Estrella implementado en SQL.")

if __name__ == "__main__":
    run_etl_pro()