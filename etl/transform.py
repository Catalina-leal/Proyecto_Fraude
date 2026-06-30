from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from .schemas import NUMERIC_COLUMNS, validate_columns
    from .sources import hash_card
except ImportError:
    from schemas import NUMERIC_COLUMNS, validate_columns
    from sources import hash_card


def haversine_km(lat1, lon1, lat2, lon2):
    radius = 6371.0
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * radius * np.arcsin(np.sqrt(a))


def clean_chunk(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(set(df.columns))
    df = df.copy()
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["trans_datetime"] = pd.to_datetime(df["trans_date_trans_time"], errors="coerce")
    df["dob"] = pd.to_datetime(df["dob"], errors="coerce")
    df = df.dropna(subset=["trans_datetime", "amt", "is_fraud", "lat", "long", "merch_lat", "merch_long"])
    df["cc_hash"] = df["cc_num"].map(hash_card)
    df["transaction_hour"] = df["trans_datetime"].dt.hour
    df["transaction_day"] = df["trans_datetime"].dt.day_name()
    df["customer_age"] = ((df["trans_datetime"] - df["dob"]).dt.days / 365.25).round(1)
    df["merchant_distance_km"] = haversine_km(df["lat"], df["long"], df["merch_lat"], df["merch_long"]).round(2)
    df["amount_bucket"] = pd.cut(
        df["amt"],
        bins=[-0.01, 25, 100, 500, float("inf")],
        labels=["0-25", "25-100", "100-500", "500+"],
    ).astype(str)
    return df


def enrich_transactions(df: pd.DataFrame, customers: pd.DataFrame, risk: pd.DataFrame) -> pd.DataFrame:
    customer_cols = ["cc_hash", "city_pop"]
    if "city_pop" in customers.columns:
        customers = customers.rename(columns={"city_pop": "profile_city_pop"})
        customer_cols = ["cc_hash", "profile_city_pop"]
    enriched = df.merge(customers[customer_cols].drop_duplicates("cc_hash"), on="cc_hash", how="left")
    enriched = enriched.merge(risk[["category", "fraud_rate", "risk_level"]], on="category", how="left")
    enriched["fraud_rate"] = enriched["fraud_rate"].fillna(0)
    enriched["risk_level"] = enriched["risk_level"].fillna("sin_clasificar")
    keep = [
        "trans_datetime",
        "cc_hash",
        "merchant",
        "category",
        "amt",
        "gender",
        "city",
        "state",
        "city_pop",
        "profile_city_pop",
        "transaction_hour",
        "transaction_day",
        "customer_age",
        "merchant_distance_km",
        "amount_bucket",
        "fraud_rate",
        "risk_level",
        "is_fraud",
    ]
    return enriched[keep]


def aggregate_outputs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    by_category = (
        df.groupby("category", as_index=False)
        .agg(transacciones=("is_fraud", "size"), fraudes=("is_fraud", "sum"), monto_total=("amt", "sum"))
        .assign(tasa_fraude=lambda x: x["fraudes"] / x["transacciones"])
        .sort_values("tasa_fraude", ascending=False)
    )
    by_state = (
        df.groupby("state", as_index=False)
        .agg(transacciones=("is_fraud", "size"), fraudes=("is_fraud", "sum"), monto_total=("amt", "sum"))
        .assign(tasa_fraude=lambda x: x["fraudes"] / x["transacciones"])
        .sort_values("fraudes", ascending=False)
    )
    kpis = {
        "transacciones": int(len(df)),
        "fraudes": int(df["is_fraud"].sum()),
        "tasa_fraude": float(df["is_fraud"].mean()) if len(df) else 0.0,
        "monto_total": float(df["amt"].sum()),
        "monto_promedio": float(df["amt"].mean()) if len(df) else 0.0,
    }
    return by_category, by_state, kpis
