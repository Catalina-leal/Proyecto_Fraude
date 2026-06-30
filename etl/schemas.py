from __future__ import annotations


REQUIRED_COLUMNS = {
    "trans_date_trans_time",
    "cc_num",
    "merchant",
    "category",
    "amt",
    "gender",
    "city",
    "state",
    "lat",
    "long",
    "city_pop",
    "dob",
    "unix_time",
    "merch_lat",
    "merch_long",
    "is_fraud",
}


NUMERIC_COLUMNS = {
    "amt",
    "lat",
    "long",
    "city_pop",
    "unix_time",
    "merch_lat",
    "merch_long",
    "is_fraud",
}


def validate_columns(columns: set[str]) -> None:
    missing = REQUIRED_COLUMNS.difference(columns)
    if missing:
        raise ValueError(f"Columnas requeridas ausentes: {sorted(missing)}")
