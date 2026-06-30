from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED = ROOT_DIR / "data/processed"

st.set_page_config(page_title="Fraude transaccional", layout="wide")

summary_path = PROCESSED / "fraud_summary_by_category.csv"
state_path = PROCESSED / "fraud_summary_by_state.csv"
kpi_path = PROCESSED / "executive_kpis.json"
transactions_path = PROCESSED / "transactions_clean.csv"

required = [summary_path, state_path, kpi_path, transactions_path]
if any(not path.exists() for path in required):
    st.warning("Ejecuta primero el pipeline ETL para generar data/processed.")
    st.stop()

category = pd.read_csv(summary_path)
state = pd.read_csv(state_path)
transactions = pd.read_csv(transactions_path, parse_dates=["trans_datetime"])
kpis = json.loads(kpi_path.read_text(encoding="utf-8"))

st.title("Dashboard de deteccion de fraude")

with st.sidebar:
    st.header("Base del dashboard")
    st.metric("Registros usados", f"{len(transactions):,}")
    st.metric("Fraudes", f"{int(transactions['is_fraud'].sum()):,}")
    st.metric("Tasa fraude", f"{transactions['is_fraud'].mean():.2%}")
    st.caption("Todos los KPIs y graficos usan el dataset completo procesado.")

filtered = transactions.copy()

if filtered.empty:
    st.info("No hay datos para los filtros seleccionados.")
    st.stop()

filtered["fraud_label"] = filtered["is_fraud"].map({0: "No fraude", 1: "Fraude"})

filtered_category = (
    filtered.groupby("category", as_index=False)
    .agg(transacciones=("is_fraud", "size"), fraudes=("is_fraud", "sum"), monto_total=("amt", "sum"))
    .assign(tasa_fraude=lambda x: x["fraudes"] / x["transacciones"])
    .sort_values("tasa_fraude", ascending=False)
)

filtered_state = (
    filtered.groupby("state", as_index=False)
    .agg(transacciones=("is_fraud", "size"), fraudes=("is_fraud", "sum"), monto_total=("amt", "sum"))
    .assign(tasa_fraude=lambda x: x["fraudes"] / x["transacciones"])
    .sort_values("fraudes", ascending=False)
)

hourly = (
    filtered.groupby(["transaction_hour", "fraud_label"], as_index=False)
    .agg(transacciones=("is_fraud", "size"), monto_total=("amt", "sum"))
)

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_hour = (
    filtered.groupby(["transaction_day", "transaction_hour"], as_index=False)
    .agg(tasa_fraude=("is_fraud", "mean"), transacciones=("is_fraud", "size"))
)
day_hour["transaction_day"] = pd.Categorical(day_hour["transaction_day"], day_order, ordered=True)

tab_exec, tab_tech, tab_ops, tab_profile = st.tabs(["Ejecutiva", "Tecnica", "Operativa", "Perfil y comportamiento"])

with tab_exec:
    total_transactions = len(filtered)
    frauds = int(filtered["is_fraud"].sum())
    fraud_rate = filtered["is_fraud"].mean()
    total_amount = filtered["amt"].sum()
    avg_amount = filtered["amt"].mean()
    fraud_amount = filtered.loc[filtered["is_fraud"] == 1, "amt"].sum()
    non_fraud_amount = filtered.loc[filtered["is_fraud"] == 0, "amt"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Transacciones", f"{total_transactions:,}")
    c2.metric("Fraudes", f"{frauds:,}")
    c3.metric("Tasa fraude", f"{fraud_rate:.2%}")
    c4.metric("Monto total", f"${total_amount:,.0f}")
    c5.metric("Monto promedio", f"${avg_amount:,.0f}")

    c6, c7 = st.columns(2)
    c6.metric("Monto total fraudes", f"${fraud_amount:,.0f}")
    c7.metric("Monto total no fraude", f"${non_fraud_amount:,.0f}")

    amount_mix = pd.DataFrame(
        {
            "tipo": ["Monto fraudes", "Monto no fraude"],
            "monto": [fraud_amount, non_fraud_amount],
        }
    )
    fig = px.pie(
        amount_mix,
        names="tipo",
        values="monto",
        title="Distribucion porcentual del monto total de transacciones",
        hole=0.38,
        color="tipo",
        color_discrete_map={
            "Monto fraudes": "#EF4444",
            "Monto no fraude": "#10B981",
        },
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="%{label}<br>Monto: $%{value:,.0f}<br>Porcentaje: %{percent}<extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        top = filtered_category.head(10)
        fig = px.bar(
            top,
            x="category",
            y="tasa_fraude",
            color="fraudes",
            title="Top categorias por tasa de fraude",
            labels={"category": "Categoria", "tasa_fraude": "Tasa de fraude", "fraudes": "Fraudes"},
            color_continuous_scale="Reds",
        )
        fig.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        risk_mix = filtered.groupby("risk_level", as_index=False).agg(transacciones=("is_fraud", "size"))
        fig = px.pie(
            risk_mix,
            names="risk_level",
            values="transacciones",
            title="Distribucion de transacciones por nivel de riesgo",
            hole=0.45,
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        hourly,
        x="transaction_hour",
        y="transacciones",
        color="fraud_label",
        markers=True,
        title="Transacciones por hora: fraude vs no fraude",
        labels={"transaction_hour": "Hora", "transacciones": "Transacciones", "fraud_label": "Tipo"},
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_tech:
    left, right = st.columns(2)
    with left:
        fig = px.histogram(
            filtered,
            x="amt",
            color="fraud_label",
            nbins=45,
            barmode="overlay",
            title="Distribucion de montos por tipo de transaccion",
            labels={"amt": "Monto", "fraud_label": "Tipo"},
        )
        fig.update_traces(opacity=0.72)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.box(
            filtered,
            x="risk_level",
            y="amt",
            color="fraud_label",
            title="Montos por nivel de riesgo",
            labels={"risk_level": "Nivel de riesgo", "amt": "Monto", "fraud_label": "Tipo"},
        )
        st.plotly_chart(fig, use_container_width=True)

    heatmap_data = day_hour.pivot(index="transaction_day", columns="transaction_hour", values="tasa_fraude")
    fig = px.imshow(
        heatmap_data,
        aspect="auto",
        color_continuous_scale="Reds",
        title="Mapa de calor: tasa de fraude por dia y hora",
        labels={"x": "Hora", "y": "Dia", "color": "Tasa fraude"},
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(
        filtered_category,
        x="transacciones",
        y="tasa_fraude",
        size="monto_total",
        color="category",
        title="Volumen vs riesgo por categoria",
        labels={"transacciones": "Transacciones", "tasa_fraude": "Tasa de fraude"},
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(filtered_category, use_container_width=True)

with tab_ops:
    left, right = st.columns(2)
    with left:
        top_state = filtered_state.head(15)
        fig = px.bar(
            top_state,
            x="state",
            y="fraudes",
            color="tasa_fraude",
            title="Estados con mas fraudes observados",
            labels={"state": "Estado", "fraudes": "Fraudes", "tasa_fraude": "Tasa fraude"},
            color_continuous_scale="OrRd",
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        amount_bucket = (
            filtered.groupby(["amount_bucket", "fraud_label"], as_index=False)
            .agg(transacciones=("is_fraud", "size"))
            .sort_values("amount_bucket")
        )
        fig = px.bar(
            amount_bucket,
            x="amount_bucket",
            y="transacciones",
            color="fraud_label",
            barmode="group",
            title="Transacciones por rango de monto",
            labels={"amount_bucket": "Rango de monto", "transacciones": "Transacciones", "fraud_label": "Tipo"},
        )
        st.plotly_chart(fig, use_container_width=True)

    high_risk = filtered[filtered["is_fraud"] == 1].sort_values("amt", ascending=False).head(25)
    st.subheader("Transacciones fraudulentas de mayor monto")
    st.dataframe(
        high_risk[
            [
                "trans_datetime",
                "merchant",
                "category",
                "amt",
                "state",
                "transaction_hour",
                "merchant_distance_km",
                "risk_level",
            ]
        ],
        use_container_width=True,
    )

with tab_profile:
    left, right = st.columns(2)
    with left:
        fig = px.histogram(
            filtered.dropna(subset=["customer_age"]),
            x="customer_age",
            color="fraud_label",
            nbins=35,
            barmode="overlay",
            title="Distribucion de edad del cliente",
            labels={"customer_age": "Edad", "fraud_label": "Tipo"},
        )
        fig.update_traces(opacity=0.72)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.histogram(
            filtered,
            x="merchant_distance_km",
            color="fraud_label",
            nbins=45,
            barmode="overlay",
            title="Distancia cliente-comercio",
            labels={"merchant_distance_km": "Distancia km", "fraud_label": "Tipo"},
        )
        fig.update_traces(opacity=0.72)
        st.plotly_chart(fig, use_container_width=True)

    gender = (
        filtered.groupby(["gender", "fraud_label"], as_index=False)
        .agg(transacciones=("is_fraud", "size"), monto_total=("amt", "sum"))
    )
    fig = px.bar(
        gender,
        x="gender",
        y="transacciones",
        color="fraud_label",
        barmode="group",
        title="Transacciones por genero y tipo",
        labels={"gender": "Genero", "transacciones": "Transacciones", "fraud_label": "Tipo"},
    )
    st.plotly_chart(fig, use_container_width=True)
