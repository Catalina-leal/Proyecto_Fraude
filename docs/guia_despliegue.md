# Guia de despliegue

## Despliegue con Docker Compose

1. Copiar el CSV a `data/raw/train.csv` o configurar `FRAUD_DATASET_PATH`.
2. Levantar MongoDB:

```bash
docker compose up -d mongo
```

3. Crear fuentes auxiliares:

```bash
python etl/bootstrap_sources.py --input data/raw/train.csv
```

4. Ejecutar ETL:

```bash
python etl/run_pipeline.py --input data/raw/train.csv --max-rows 50000
```

5. Levantar servicios:

```bash
docker compose up --build
```

6. Validar servicios:

- MongoDB: localhost:27017
- API: http://localhost:8000/health
- Documentacion API: http://localhost:8000/docs
- Dashboard: http://localhost:8501

## Variables de entorno

- `FRAUD_DATASET_PATH`: ruta del CSV.
- `FRAUD_API_URL`: URL base de la API.
- `FRAUD_MONGO_URI`: conexion a MongoDB.
- `FRAUD_MONGO_DB`: base de datos MongoDB.
- `FRAUD_MONGO_COLLECTION`: coleccion de perfiles.
- `FRAUD_OUTPUT_DIR`: ruta de salidas procesadas.
- `FRAUD_CHUNK_SIZE`: tamano de chunk para lectura.
