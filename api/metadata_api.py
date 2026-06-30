from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException


ROOT_DIR = Path(__file__).resolve().parents[1]
RISK_PATH = ROOT_DIR / "data/reference/category_risk.json"

app = FastAPI(title="Fraud Metadata API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/category-risk")
def category_risk():
    if not RISK_PATH.exists():
        raise HTTPException(status_code=404, detail="Ejecuta primero etl/bootstrap_sources.py")
    return json.loads(RISK_PATH.read_text(encoding="utf-8"))
