import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///dw_comercial_financiero.db')

def generar_reportes_estrategicos():
    print("📊 Generando Métricas Estratégicas (Corregidas)...")
    
    # MÉTRICA 1: Riesgo vs Liquidez 
    # Usamos comillas dobles para nombres con espacios
    query_riesgo = """
    SELECT 
        c."Risk Tolerance", 
        AVG(f."Account Balance") as Balance_Promedio,
        SUM(f."Deposits") as Total_Depositos
    FROM fact_transacciones f
    JOIN dim_clientes c ON f.customer_id = c.customer_id
    GROUP BY c."Risk Tolerance"
    """
    
    # MÉTRICA 2: Préstamos por Ocupación
    # Eliminamos el filtro 'Approved' por ahora para ver si hay datos
    query_prestamos = """
    SELECT 
        c.Occupation, 
        COUNT(p.customer_id) as Cantidad_Prestamos,
        AVG(p."Interest Rate") as Tasa_Promedio
    FROM dim_prestamos p
    JOIN dim_clientes c ON p.customer_id = c.customer_id
    GROUP BY c.Occupation
    ORDER BY Cantidad_Prestamos DESC
    LIMIT 5
    """
    
    df_riesgo = pd.read_sql(query_riesgo, engine)
    df_prestamos = pd.read_sql(query_prestamos, engine)
    
    print("\n--- Análisis de Riesgo y Liquidez ---")
    print(df_riesgo)
    print("\n--- Top 5 Ocupaciones con Créditos ---")
    print(df_prestamos)

if __name__ == "__main__":
    generar_reportes_estrategicos()