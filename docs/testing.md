# Testing y control de calidad

## Pruebas automatizadas

Ejecutar:

```bash
pytest -q
```

Cobertura incluida:

- Validacion de transformaciones principales.
- Creacion de hash anonimo de tarjeta.
- Enriquecimiento con datos de referencia.

## Validaciones del ETL

- Verifica columnas obligatorias antes de procesar.
- Convierte numericos con manejo de errores.
- Elimina filas sin campos criticos para analisis.
- Lee por chunks para soportar archivos grandes.
- Evita persistir numeros de tarjeta originales.
