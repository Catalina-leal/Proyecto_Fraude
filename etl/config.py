from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


ROOT_DIR = Path(__file__).resolve().parents[1]
if load_dotenv is not None:
    load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    dataset_path: Path = Path(os.getenv("FRAUD_DATASET_PATH", ROOT_DIR / "data/raw/train.csv"))
    api_url: str = os.getenv("FRAUD_API_URL", "http://localhost:8000").rstrip("/")
    mongo_uri: str = os.getenv("FRAUD_MONGO_URI", "mongodb://localhost:27017")
    mongo_db: str = os.getenv("FRAUD_MONGO_DB", "fraud_project")
    mongo_collection: str = os.getenv("FRAUD_MONGO_COLLECTION", "customer_profiles")
    output_dir: Path = Path(os.getenv("FRAUD_OUTPUT_DIR", ROOT_DIR / "data/processed"))
    reference_dir: Path = ROOT_DIR / "data/reference"
    nosql_dir: Path = ROOT_DIR / "data/nosql"
    chunk_size: int = int(os.getenv("FRAUD_CHUNK_SIZE", "50000"))


settings = Settings()
