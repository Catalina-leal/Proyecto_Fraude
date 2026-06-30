from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

try:
    from .config import settings
    from .sources import load_sources, read_transactions
    from .transform import aggregate_outputs, clean_chunk, enrich_transactions
except ImportError:
    from config import settings
    from sources import load_sources, read_transactions
    from transform import aggregate_outputs, clean_chunk, enrich_transactions


def run(input_path: Path, max_rows: int = 50000) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"No se encontro el dataset: {input_path}")
    if not (settings.nosql_dir / "customer_profiles.json").exists():
        raise FileNotFoundError("No existe la fuente NoSQL. Ejecuta primero etl/bootstrap_sources.py")

    settings.output_dir.mkdir(parents=True, exist_ok=True)
    customers, risk = load_sources()
    processed_parts: list[pd.DataFrame] = []
    rows_seen = 0

    for chunk in read_transactions(input_path, settings.chunk_size):
        if max_rows and rows_seen >= max_rows:
            break
        if max_rows:
            chunk = chunk.head(max_rows - rows_seen)
        cleaned = clean_chunk(chunk)
        processed_parts.append(enrich_transactions(cleaned, customers, risk))
        rows_seen += len(chunk)

    if not processed_parts:
        raise ValueError("No se procesaron filas validas.")

    processed = pd.concat(processed_parts, ignore_index=True)
    by_category, by_state, kpis = aggregate_outputs(processed)

    processed.to_csv(settings.output_dir / "transactions_clean.csv", index=False)
    by_category.to_csv(settings.output_dir / "fraud_summary_by_category.csv", index=False)
    by_state.to_csv(settings.output_dir / "fraud_summary_by_state.csv", index=False)
    (settings.output_dir / "executive_kpis.json").write_text(json.dumps(kpis, indent=2), encoding="utf-8")
    print(json.dumps(kpis, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta el pipeline ETL de fraude.")
    parser.add_argument("--input", type=Path, default=settings.dataset_path)
    parser.add_argument("--max-rows", type=int, default=50000, help="0 procesa todo el archivo.")
    args = parser.parse_args()
    run(args.input, args.max_rows)


if __name__ == "__main__":
    main()
