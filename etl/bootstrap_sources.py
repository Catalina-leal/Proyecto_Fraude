from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

try:
    from .config import settings
except ImportError:
    from config import settings


def hash_card(value: object) -> str:
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


def row_limit(max_rows: int) -> int | None:
    return max_rows if max_rows > 0 else None


def build_category_risk(input_path: Path, output_path: Path, max_rows: int = 250000) -> None:
    df = pd.read_csv(input_path, usecols=["category", "is_fraud"], nrows=row_limit(max_rows))
    grouped = (
        df.groupby("category", as_index=False)
        .agg(total_transactions=("is_fraud", "size"), fraud_rate=("is_fraud", "mean"))
        .sort_values("fraud_rate", ascending=False)
    )
    grouped["risk_level"] = pd.cut(
        grouped["fraud_rate"],
        bins=[-0.001, 0.005, 0.02, 1.0],
        labels=["bajo", "medio", "alto"],
    ).astype(str)
    payload = grouped.to_dict(orient="records")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_customer_mongo(input_path: Path, fallback_path: Path, max_rows: int = 250000) -> int:
    usecols = ["cc_num", "gender", "city", "state", "city_pop", "dob"]
    df = pd.read_csv(input_path, usecols=usecols, nrows=row_limit(max_rows))
    df["cc_hash"] = df["cc_num"].map(hash_card)
    df = df.drop(columns=["cc_num"]).drop_duplicates("cc_hash")
    records = df.to_dict(orient="records")

    fallback_path.parent.mkdir(parents=True, exist_ok=True)
    fallback_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo no esta instalado. Se genero respaldo JSON para la fuente NoSQL.")
        return len(records)

    client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=3000)
    try:
        client.admin.command("ping")
        collection = client[settings.mongo_db][settings.mongo_collection]
        collection.delete_many({})
        if records:
            collection.insert_many(records)
        collection.create_index("cc_hash")
        print(f"Fuente MongoDB cargada: {settings.mongo_db}.{settings.mongo_collection}")
    except Exception as exc:
        print(f"No se pudo cargar MongoDB ({exc}). Se usara respaldo JSON.")
    finally:
        client.close()
    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea fuentes auxiliares MongoDB/NoSQL y REST de referencia.")
    parser.add_argument("--input", type=Path, default=settings.dataset_path)
    parser.add_argument("--mongo-json", type=Path, default=settings.nosql_dir / "customer_profiles.json")
    parser.add_argument("--risk-json", type=Path, default=settings.reference_dir / "category_risk.json")
    parser.add_argument("--max-rows", type=int, default=250000)
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"No se encontro el dataset: {args.input}")

    build_category_risk(args.input, args.risk_json, args.max_rows)
    profile_count = build_customer_mongo(args.input, args.mongo_json, args.max_rows)
    print(f"Fuente API generada: {args.risk_json}")
    print(f"Fuente NoSQL generada: {profile_count} perfiles en MongoDB o respaldo {args.mongo_json}")


if __name__ == "__main__":
    main()
