from __future__ import annotations

import pandas as pd

from etl.transform import clean_chunk, enrich_transactions


def sample_frame():
    return pd.DataFrame(
        {
            "trans_date_trans_time": ["2019-01-01 00:00:18"],
            "cc_num": [123456],
            "merchant": ["fraud_Test"],
            "category": ["misc_net"],
            "amt": [10.5],
            "gender": ["F"],
            "city": ["Santiago"],
            "state": ["RM"],
            "lat": [-33.45],
            "long": [-70.66],
            "city_pop": [5000000],
            "dob": ["1990-01-01"],
            "unix_time": [1325376018],
            "merch_lat": [-33.46],
            "merch_long": [-70.67],
            "is_fraud": [0],
        }
    )


def test_clean_chunk_adds_features():
    cleaned = clean_chunk(sample_frame())
    assert "cc_hash" in cleaned.columns
    assert "merchant_distance_km" in cleaned.columns
    assert cleaned.loc[0, "transaction_hour"] == 0


def test_enrich_transactions_joins_reference_data():
    cleaned = clean_chunk(sample_frame())
    customers = pd.DataFrame({"cc_hash": cleaned["cc_hash"], "city_pop": [5000000]})
    risk = pd.DataFrame({"category": ["misc_net"], "fraud_rate": [0.01], "risk_level": ["medio"]})
    enriched = enrich_transactions(cleaned, customers, risk)
    assert enriched.loc[0, "risk_level"] == "medio"
    assert enriched.loc[0, "fraud_rate"] == 0.01
