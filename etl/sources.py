from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

try:
    from .config import settings
except ImportError:
    from config import settings


def hash_card(value: object) -> str:
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


def read_transactions(path: Path, chunksize: int):
    return pd.read_csv(path, chunksize=chunksize)


def read_customer_profiles_from_mongo(fallback_path: Path) -> pd.DataFrame:
    try:
        from pymongo import MongoClient
    except ImportError:
        payload = json.loads(fallback_path.read_text(encoding="utf-8"))
        return pd.DataFrame(payload)

    client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=3000)
    try:
        client.admin.command("ping")
        cursor = client[settings.mongo_db][settings.mongo_collection].find({}, {"_id": 0})
        records = list(cursor)
        if not records:
            raise ValueError("La coleccion MongoDB esta vacia.")
        return pd.DataFrame(records)
    except Exception:
        payload = json.loads(fallback_path.read_text(encoding="utf-8"))
        return pd.DataFrame(payload)
    finally:
        client.close()


def read_category_risk(api_url: str, fallback_path: Path) -> pd.DataFrame:
    try:
        with urllib.request.urlopen(f"{api_url}/category-risk", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        payload = json.loads(fallback_path.read_text(encoding="utf-8"))
    return pd.DataFrame(payload)


def load_sources():
    customers = read_customer_profiles_from_mongo(settings.nosql_dir / "customer_profiles.json")
    risk = read_category_risk(settings.api_url, settings.reference_dir / "category_risk.json")
    return customers, risk
