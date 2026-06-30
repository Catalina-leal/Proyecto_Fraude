# Matriz de cumplimiento de la evaluacion

## Pipeline ETL robusto - 20%

- Archivos: `etl/bootstrap_sources.py`, `etl/run_pipeline.py`, `etl/transform.py`, `etl/sources.py`, `etl/schemas.py`.
- Integra tres fuentes: CSV, MongoDB NoSQL y API REST.
- Valida columnas obligatorias y tipos numericos.
- Procesa por chunks para soportar volumen alto.
- Maneja caida de API usando archivo local de respaldo.
- Maneja ausencia temporal de MongoDB usando respaldo JSON reproducible.
- Anonimiza `cc_num` con hash SHA-256.

## Documentacion tecnica - 20%

- `README.md`: instalacion, ejecucion y salidas.
- `docs/arquitectura.md`: diagrama y decisiones tecnicas.
- `docs/api.md`: endpoints y formato de respuesta.
- `docs/manual_usuario.md`: uso funcional del dashboard.
- `docs/guia_despliegue.md`: Docker, variables y validacion.
- `docs/testing.md`: pruebas y control de calidad.

## Dashboard interactivo - 25%

- Archivo: `dashboards/app.py`.
- Herramientas: Streamlit y Plotly.
- Vistas diferenciadas: ejecutiva, tecnica y operativa.
- KPI: transacciones, fraudes, tasa de fraude, monto total.

## Git colaborativo - 15%

- Archivo: `repo/evidencia_git.md`.
- Incluye flujo sugerido de ramas, commits, merges, issues y pull requests.
- Para una defensa real, ejecutar esos pasos en GitHub o GitLab y capturar evidencia.

## Docker - 20%

- Archivos: `docker/Dockerfile`, `docker-compose.yml`.
- Servicios: MongoDB, API FastAPI y dashboard Streamlit.
- Configuracion externa mediante variables de entorno.
- Montaje de carpeta `data` para no reconstruir imagen por cambios de datos.

## Presentacion individual

Puntos recomendados para la exposicion:

1. Mostrar el diagrama de `docs/arquitectura.md`.
2. Ejecutar `etl/bootstrap_sources.py` y `etl/run_pipeline.py`.
3. Mostrar MongoDB como fuente NoSQL, API en `/docs` y dashboard en Streamlit.
4. Explicar decisiones: chunks, anonimizar tarjeta, MongoDB, fallback de API y separacion por audiencias.
5. Mencionar mejoras futuras: modelo predictivo supervisado, monitoreo en tiempo real y CI/CD.
