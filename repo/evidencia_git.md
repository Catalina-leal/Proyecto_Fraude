# Evidencia sugerida de Git

Para la defensa, se recomienda crear el repositorio y ejecutar un flujo similar:

```bash
git init
git checkout -b feature/etl-pipeline
git add etl data/reference docs
git commit -m "Add reproducible ETL pipeline"
git checkout -b feature/dashboard
git add dashboards api docker-compose.yml docker
git commit -m "Add dashboard API and Docker deployment"
git checkout main
git merge feature/etl-pipeline
git merge feature/dashboard
```

Buenas practicas a evidenciar:

- Issues para tareas de ETL, dashboard, Docker y documentacion.
- Pull requests con revision de codigo.
- Commits pequenos y descriptivos.
- README actualizado con pasos reproducibles.
