# Proyecto ETL y Dashboard de Deteccion de Fraude

Proyecto desarrollado para la Evaluacion Parcial N°3 de SCY1101. Integra tres fuentes de datos, ejecuta un pipeline ETL reproducible, usa MongoDB como fuente NoSQL, expone una API REST de metadatos de riesgo y entrega un dashboard interactivo en Streamlit.

## Objetivo

Construir una solucion end-to-end para analizar transacciones financieras y detectar patrones asociados a fraude usando el dataset `train (1).csv`.

## Fuentes integradas

1. CSV transaccional: `data/raw/train.csv` o la ruta definida en `FRAUD_DATASET_PATH`.
2. MongoDB NoSQL: coleccion `fraud_project.customer_profiles`, generada desde el CSV con perfiles anonimizados por tarjeta.
3. API REST: servicio FastAPI en `api/metadata_api.py`, que entrega pesos de riesgo por categoria.

## Estructura

```text
api/          API REST de metadatos
dashboards/   Dashboard Streamlit
data/         Datos raw, NoSQL, referencia y salidas procesadas
docker/       Dockerfiles
docs/         Documentacion tecnica, usuario, despliegue y diagramas
etl/          Pipeline ETL modular
repo/         Evidencias sugeridas de colaboracion Git
tests/        Pruebas automatizadas
```

## Ejecucion local rapida

1. Crear entorno e instalar dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Configurar el dataset:

```bash
copy .env.example .env
```

Editar `.env` y apuntar `FRAUD_DATASET_PATH` al CSV real, por ejemplo:

```text
FRAUD_DATASET_PATH=C:\Users\catal\Downloads\train (1).csv
```

3. Levantar MongoDB local con Docker:

```bash
docker compose up -d mongo
```

4. Crear fuentes auxiliares:

```bash
python etl/bootstrap_sources.py --input "%FRAUD_DATASET_PATH%"
```

Si MongoDB esta corriendo, los perfiles anonimizados se cargan en la coleccion `fraud_project.customer_profiles`. Si MongoDB no esta disponible, el proyecto genera `data/nosql/customer_profiles.json` como respaldo para que la demo siga funcionando.

5. Levantar API de metadatos:

```bash
uvicorn api.metadata_api:app --host 0.0.0.0 --port 8000
```

6. Ejecutar ETL:

```bash
python etl/run_pipeline.py --input "%FRAUD_DATASET_PATH%" --max-rows 50000
```

Usar `--max-rows 0` para procesar todo el archivo.

7. Abrir dashboard:

```bash
streamlit run dashboards/app.py
```

## Docker

```bash
docker compose up --build
```

Servicios:

- MongoDB: localhost:27017
- API: http://localhost:8000/docs
- Dashboard: http://localhost:8501

## Pruebas

```bash
pytest -q
```

## Salidas principales

- `data/processed/transactions_clean.csv`
- `data/processed/fraud_summary_by_category.csv`
- `data/processed/fraud_summary_by_state.csv`
- `data/processed/executive_kpis.json`

## Notas de privacidad

El pipeline anonimiza `cc_num` mediante hash SHA-256 y no persiste el numero de tarjeta en las salidas analiticas. Los nombres, direcciones y numeros de transaccion se omiten en los archivos procesados para reducir exposicion de datos personales.
