# Documentacion de API

## GET /health

Retorna estado del servicio.

Respuesta:

```json
{"status": "ok"}
```

## GET /category-risk

Retorna riesgo historico por categoria calculado desde el dataset.

Campos:

- `category`: categoria comercial.
- `total_transactions`: numero de transacciones observadas.
- `fraud_rate`: tasa de fraude de la categoria.
- `risk_level`: clasificacion `bajo`, `medio` o `alto`.

Ejemplo:

```json
[
  {
    "category": "shopping_net",
    "total_transactions": 1000,
    "fraud_rate": 0.02,
    "risk_level": "medio"
  }
]
```
