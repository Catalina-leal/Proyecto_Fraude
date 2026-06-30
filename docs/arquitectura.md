# Arquitectura tecnica

```mermaid
flowchart LR
    CSV["CSV transaccional"] --> ETL["Pipeline ETL"]
    MONGO["MongoDB customer_profiles"] --> ETL
    API["FastAPI category-risk"] --> ETL
    ETL --> OUT["Data processed"]
    OUT --> DASH["Streamlit dashboard"]
    OUT --> DOC["Reportes CSV y KPIs JSON"]
```

## Componentes

- `etl/bootstrap_sources.py`: carga MongoDB y crea el JSON de referencia para la API.
- `api/metadata_api.py`: expone `/category-risk` y `/health`.
- `etl/run_pipeline.py`: valida columnas, limpia datos, anonimiza tarjetas, crea variables y genera salidas.
- `dashboards/app.py`: presenta vistas ejecutiva, tecnica y operativa.

## Decisiones tecnicas

- Pandas por su eficiencia suficiente para procesamiento por chunks.
- MongoDB como fuente NoSQL para perfiles anonimizados.
- FastAPI para una API REST clara, documentable y testeable.
- Streamlit y Plotly para dashboards interactivos con baja friccion de despliegue.
