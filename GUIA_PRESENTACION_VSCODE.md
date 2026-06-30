# Guia para explicar el proyecto en la presentacion

## Duracion sugerida

Entre 8 y 12 minutos.

## 1. Introduccion

Frase sugerida:

> Este proyecto construye una solucion end-to-end de analisis de fraude transaccional. El objetivo es tomar un dataset de transacciones, integrarlo con fuentes auxiliares, procesarlo con un pipeline ETL y presentar resultados en un dashboard interactivo.

Que mostrar en VS Code:

- `README.md`
- `docs/arquitectura.md`

## 2. Problema de negocio

Frase sugerida:

> El problema es identificar patrones de fraude en transacciones. Para eso se analizan variables como monto, categoria del comercio, ubicacion, horario, distancia entre cliente y comercio, y estado geografico.

Que mostrar:

- Una vista del CSV o `data/processed/transactions_clean.csv`.

## 3. Arquitectura del proyecto

Frase sugerida:

> La arquitectura tiene tres fuentes de datos. Primero, el CSV principal. Segundo, MongoDB con perfiles anonimizados. Tercero, una API REST que entrega riesgo por categoria. El ETL integra esas fuentes y genera salidas procesadas para el dashboard.

Que mostrar:

- `docs/arquitectura.md`
- Carpetas `etl/`, `api/`, `dashboards/`, `data/`.

## 4. Explicacion del ETL

Frase sugerida:

> El ETL se separa en modulos para que sea mantenible. `schemas.py` valida columnas, `sources.py` lee las fuentes, `transform.py` limpia y crea variables, y `run_pipeline.py` ejecuta todo el proceso.

Que mostrar:

- `etl/run_pipeline.py`
- `etl/transform.py`

Explicacion simple:

- Valida que el CSV tenga columnas necesarias.
- Convierte fechas y numeros.
- Elimina filas con datos criticos vacios.
- Anonimiza tarjetas.
- Calcula edad del cliente.
- Calcula distancia entre cliente y comercio.
- Agrega categoria de monto.
- Une perfiles desde MongoDB.
- Une riesgo por categoria desde la API.
- Exporta resultados a `data/processed/`.

## 5. Tres fuentes de datos

Frase sugerida:

> La evaluacion pide al menos tres fuentes. En este proyecto se usan: el CSV original, MongoDB como base NoSQL para perfiles de clientes y una API REST de riesgo por categoria. Aunque MongoDB y la API se cargan desde el dataset para que el proyecto sea reproducible, funcionan como fuentes separadas dentro del pipeline.

Que mostrar:

- `etl/bootstrap_sources.py`
- MongoDB: coleccion `fraud_project.customer_profiles`
- `data/nosql/customer_profiles.json` como respaldo reproducible
- `api/metadata_api.py`
- `data/reference/category_risk.json`

## 6. Dashboard

Frase sugerida:

> El dashboard esta hecho en Streamlit y tiene visualizaciones diferenciadas por audiencia. La vista ejecutiva resume KPIs, la vista tecnica permite analizar categorias y la vista operativa ayuda a priorizar estados con mas fraudes.

Que mostrar:

- `dashboards/app.py`
- Navegador con Streamlit abierto.

Comando:

```powershell
streamlit run dashboards/app.py
```

## 7. Pruebas

Frase sugerida:

> Se agregaron pruebas para validar que el proceso cree variables importantes, anonimice correctamente y una los datos de referencia.

Que mostrar:

- `tests/test_transform.py`

Comando:

```powershell
pytest -q
```

Si `pytest` no esta instalado:

```powershell
pip install pytest
pytest -q
```

## 8. Docker

Frase sugerida:

> Docker permite ejecutar la solucion de forma reproducible en otro equipo. El proyecto incluye un Dockerfile y docker-compose para levantar MongoDB, la API y el dashboard como servicios separados.

Que mostrar:

- `docker/Dockerfile`
- `docker-compose.yml`

Comando opcional:

```powershell
docker compose up --build
```

## 9. Git

Frase sugerida:

> La evidencia de Git muestra como se podria trabajar profesionalmente: ramas por funcionalidad, commits descriptivos, merges, issues y pull requests.

Que mostrar:

- `repo/evidencia_git.md`

## 10. Cierre

Frase sugerida:

> Como mejora futura, se podria agregar un modelo predictivo supervisado, monitoreo en tiempo real, despliegue cloud y automatizacion CI/CD. La base actual ya deja una arquitectura modular, reproducible y documentada.

## Preguntas probables y respuestas cortas

**Por que se usa hash para la tarjeta?**

Para proteger datos sensibles. Permite identificar una tarjeta sin guardar el numero real.

**Por que se procesa por chunks?**

Porque el CSV es grande. Leerlo por partes evita consumir demasiada memoria.

**Por que hay MongoDB si ya existe CSV?**

Porque la pauta exige integrar multiples fuentes. MongoDB representa una fuente NoSQL separada con perfiles anonimizados.

**Que pasa si MongoDB no esta levantado?**

El proyecto deja un respaldo JSON en `data/nosql/customer_profiles.json`. Eso permite hacer la demo sin perder reproducibilidad, pero la arquitectura preparada es MongoDB.

**Por que hay API?**

Porque simula una fuente externa de metadatos de riesgo, como un servicio interno de una empresa.

**Que entrega final genera el ETL?**

Genera archivos limpios en `data/processed/`, especialmente `transactions_clean.csv`, resumen por categoria, resumen por estado y KPIs ejecutivos.
