# 🏛️ Documentación Técnica: Data Warehouse Comercial Financiero

Este documento detalla la arquitectura y los procesos aplicados para la transformación de datos sintéticos financieros en un repositorio centralizado optimizado para la toma de decisiones.

## 1. Diseño del Modelo Dimensional (Star Schema)
Se implementó un modelo estrella para optimizar la velocidad de las consultas analíticas y separar las entidades maestras de los hechos transaccionales.



- **Fact_Transacciones**: Contiene las métricas cuantitativas (Account Balance, Deposits, Withdrawals, Investments). Es el núcleo del análisis.
- **Dim_Clientes**: Almacena atributos demográficos (Age, Occupation, Address) y perfiles de riesgo. Actúa como el Master Data Management (MDM).
- **Dim_Prestamos**: Detalles específicos de créditos, tasas y propósitos de financiamiento.

## 2. Proceso ETL (Extracción, Transformación y Carga)
El proceso se construyó en Python utilizando `Pandas` para la lógica de negocio y `SQLAlchemy` para la persistencia.

### Transformaciones Críticas (Calidad de Datos):
- **Normalización Monetaria**: Se eliminaron caracteres especiales (`$`, `,`) y se convirtieron los valores a tipos de datos flotantes (`Float64`) para permitir operaciones matemáticas.
- **Generación de Llaves Subrogadas**: Ante la ausencia de IDs en la fuente original, se generó un `customer_id` único mediante el agrupamiento de atributos demográficos, asegurando la integridad referencial.
- **Tratamiento de Nulos**: Se aplicaron políticas de `fillna(0)` para asegurar que las métricas de balance no afecten el promedio general por registros incompletos.

## 3. Gobernanza y Calidad
- **Consistencia**: Se garantizó que cada transacción esté vinculada a un cliente único en la dimensión de maestros.
- **Optimización**: El modelo permite realizar Joins de alta velocidad para generar reportes como el de "Riesgo vs Liquidez" sin procesar archivos CSV pesados repetidamente.

## 4. Métricas Estratégicas Generadas
A través de SQL analítico, el repositorio permite identificar:
1. **Concentración de Liquidez**: Depósitos totales segmentados por niveles de tolerancia al riesgo.
2. **Penetración de Crédito**: Ranking de ocupaciones con mayor volumen de préstamos y sus tasas de interés promedio.