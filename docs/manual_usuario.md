# Manual de usuario

## Preparacion

1. Instalar Python 3.11 o superior.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Configurar `.env` usando `.env.example`.
4. Ejecutar `python etl/bootstrap_sources.py --input "ruta/al/train.csv"`.
5. Ejecutar `python etl/run_pipeline.py --input "ruta/al/train.csv" --max-rows 50000`.
6. Abrir el dashboard con `streamlit run dashboards/app.py`.

## Uso del dashboard

- Vista ejecutiva: KPIs generales y categorias de mayor riesgo.
- Vista tecnica: tabla completa y relacion entre volumen, riesgo y monto.
- Vista operativa: estados con mayor numero de fraudes para priorizar monitoreo.

## Interpretacion

La tasa de fraude se calcula como `fraudes / transacciones`. Las categorias con baja frecuencia deben interpretarse con cautela porque una muestra pequena puede elevar artificialmente la tasa.
