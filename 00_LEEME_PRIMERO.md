# Lee esto primero - Guia para Visual Studio Code

Este proyecto analiza transacciones bancarias para detectar y explicar patrones de fraude. Esta pensado para abrirlo en Visual Studio Code, ejecutar algunos comandos y mostrar el resultado en una presentacion.

## Idea principal del proyecto

El proyecto toma un archivo CSV con transacciones, lo limpia, lo cruza con otras dos fuentes de datos y genera graficos para entender donde aparece mas fraude.

En palabras simples:

1. Entra un archivo grande de transacciones.
2. El ETL valida, limpia y transforma los datos.
3. Se agregan dos fuentes extra: MongoDB y una API de riesgo por categoria.
4. Se generan archivos procesados.
5. El dashboard muestra los resultados con graficos.

## Carpetas explicadas sin tecnicismos

```text
etl/
```

Es el motor del proyecto. Aqui esta el codigo que lee el CSV, limpia los datos, crea variables nuevas y genera resultados.

```text
api/
```

Simula una fuente externa de datos. Entrega informacion de riesgo por categoria, como si otro sistema de la empresa estuviera aportando datos al analisis.

```text
dashboards/
```

Contiene la pantalla visual hecha con Streamlit. Es lo que se muestra al profesor para ver graficos, KPIs y tablas.

```text
data/
```

Guarda datos. Se divide en:

- `data/raw/`: datos originales.
- `data/nosql/`: respaldo JSON de la fuente MongoDB.
- `data/reference/`: datos de referencia para la API.
- `data/processed/`: resultados finales del ETL.

```text
docs/
```

Documentacion tecnica. Sirve para demostrar arquitectura, API, despliegue y pruebas.

```text
tests/
```

Pruebas para comprobar que las transformaciones principales funcionan.

```text
docker/
```

Archivos para desplegar el proyecto en contenedores. En la presentacion basta con explicar que esto permite ejecutar la solucion de forma reproducible.

## Orden recomendado para abrir archivos en VS Code

1. `00_LEEME_PRIMERO.md`
2. `GUIA_PRESENTACION_VSCODE.md`
3. `etl/run_pipeline.py`
4. `etl/transform.py`
5. `dashboards/app.py`
6. `docs/arquitectura.md`

## Comandos principales

Desde la terminal de VS Code, dentro de la carpeta del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Levantar MongoDB:

```powershell
docker compose up -d mongo
```

Crear las fuentes auxiliares:

```powershell
python etl/bootstrap_sources.py --input "C:\Users\catal\Downloads\train (1).csv"
```

Ejecutar el ETL:

```powershell
python etl/run_pipeline.py --input "C:\Users\catal\Downloads\train (1).csv" --max-rows 50000
```

Levantar la API:

```powershell
uvicorn api.metadata_api:app --host 127.0.0.1 --port 8000
```

Abrir el dashboard:

```powershell
streamlit run dashboards/app.py
```

## Que decir si te preguntan por las tres fuentes

La primera fuente es el CSV original de transacciones. La segunda fuente es MongoDB, donde se guardan perfiles anonimizados de clientes. La tercera fuente es una API REST que entrega niveles de riesgo por categoria de comercio. El ETL une estas tres fuentes para producir un dataset enriquecido.

## Que decir si te preguntan por privacidad

El numero de tarjeta `cc_num` no se guarda en los resultados finales. Se transforma en un hash con SHA-256 para poder cruzar datos sin exponer el numero real.

## Que decir si te preguntan por MongoDB

MongoDB es una base NoSQL orientada a documentos. En este proyecto se usa para guardar perfiles anonimizados de clientes, y el ETL consulta esa coleccion para enriquecer las transacciones.

## Que decir si te preguntan por el dashboard

El dashboard tiene tres miradas:

- Ejecutiva: KPIs generales y categorias mas riesgosas.
- Tecnica: tabla y grafico para analizar volumen versus tasa de fraude.
- Operativa: estados con mas fraudes para priorizar acciones.
