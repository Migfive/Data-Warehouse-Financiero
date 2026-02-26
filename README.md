# 🏛️ Data Warehouse Financiero: Arquitectura Estrella & Análisis Comercial

Este proyecto implementa una solución integral de **Ingeniería de Datos** para transformar fuentes de datos financieros crudos en un **Data Warehouse (DW)** centralizado, optimizado para la generación de métricas estratégicas y análisis de riesgo.

## 🎯 Objetivo del Proyecto
Diseñar e implementar un ecosistema de datos que cumpla con los estándares de gobernanza, permitiendo la transición de archivos planos (CSV) a un modelo dimensional robusto para la toma de decisiones comerciales.

---

## 🚀 Funcionalidades Clave

### 1. Pipeline ETL (Python & SQLAlchemy)
Se desarrolló un proceso de **Extracción, Transformación y Carga (ETL)** que garantiza la integridad de los datos:
* **Limpieza de Datos:** Normalización de columnas monetarias eliminando caracteres especiales y estandarizando tipos de datos numéricos.
* **Gobernanza:** Implementación de reglas de negocio para la gestión de Identidad Maestra (MDM) mediante la creación de llaves subrogadas (`customer_id`).
* **Carga Automatizada:** Ingesta en un repositorio SQL (SQLite) con lógica de actualización eficiente.

### 2. Modelo Dimensional (Star Schema)
Para optimizar el rendimiento de las consultas analíticas, los datos se estructuraron en un **Modelo de Estrella**:
* **Tabla de Hechos (`fact_transacciones`):** Centraliza métricas de balance, depósitos, retiros e inversiones.
* **Dimensiones (`dim_clientes`, `dim_prestamos`):** Almacenan atributos demográficos, perfiles de riesgo y estatus crediticio.

### 3. Dashboard de Inteligencia de Negocios
Interfaz interactiva desarrollada en **Streamlit** que consume el DW para visualizar:
* **Métricas de Liquidez:** Análisis de balances promedio por nivel de riesgo.
* **Segmentación Comercial:** Identificación de las ocupaciones con mayor penetración de créditos.

---

## 📊 Resultados e Insights de Negocio
Gracias a la implementación del modelo estrella y consultas SQL analíticas, el sistema permite identificar:
* **Correlación Riesgo-Liquidez:** Los clientes con tolerancia al riesgo "Medium" mantienen, en promedio, balances más altos que los perfiles "High".
* **Penetración de Mercado:** Las ocupaciones de Ingeniería y Educación representan los mayores volúmenes de transaccionalidad, sugiriendo una oportunidad de segmentación para productos premium.

---

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Procesamiento de Datos:** Pandas, NumPy
* **Base de Datos:** SQL (SQLite / SQLAlchemy)
* **Visualización:** Plotly, Streamlit

---

## ⚙️ Cómo ejecutar el proyecto

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Migfive/Data-Warehouse-Financiero.git


## 📈 Previzualización 
![Gráfica](Warehouse.png)


## 📈 link 
https://data-warehouse-financiero-jmdgntpvfjcujzbkhfcfke.streamlit.app/ 