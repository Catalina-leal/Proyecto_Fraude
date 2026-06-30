FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir pandas numpy fastapi uvicorn streamlit plotly pymongo python-dotenv
COPY . .
ENV FRAUD_DATASET_PATH=/app/data/raw/train.csv
ENV FRAUD_API_URL=http://api:8000
EXPOSE 8501
CMD ["streamlit", "run", "dashboards/app.py", "--server.address=0.0.0.0"]
