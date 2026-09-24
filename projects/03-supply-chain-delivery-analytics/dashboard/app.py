import streamlit as st
import pandas as pd

st.set_page_config(page_title="Supply Chain Analytics | Farjad Zeya", layout="wide")
st.title("🚚 Supply Chain & Delivery Performance Analytics")
st.caption("Production Portfolio Project by Farjad Zeya | Data Analyst (SQL • Excel • Power BI)")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/supply_chain_shipments_cleaned.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

st.sidebar.header("Logistics Controls")
sel_wh = st.sidebar.multiselect("Origin Warehouse", sorted(df["origin_warehouse"].unique()), default=sorted(df["origin_warehouse"].unique()))
sel_carrier = st.sidebar.multiselect("Carrier", sorted(df["carrier_name"].unique()), default=sorted(df["carrier_name"].unique()))

filtered_df = df[(df["origin_warehouse"].isin(sel_wh)) & (df["carrier_name"].isin(sel_carrier))]

total_ship = len(filtered_df)
ontime_ship = filtered_df["on_time_flag"].sum()
otd_pct = (ontime_ship / total_ship * 100) if total_ship > 0 else 0
delayed_df = filtered_df[filtered_df["delivery_status"] == "Delayed"]
avg_delay = delayed_df["delivery_delay_days"].mean() if len(delayed_df) > 0 else 0
total_spend = filtered_df["shipping_cost_usd"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Shipments", f"{total_ship:,}")
c2.metric("On-Time Delivery (OTD)", f"{otd_pct:.2f}%")
c3.metric("Avg Delay Duration", f"{avg_delay:.2f} days")
c4.metric("Total Freight Cost", f"${total_spend:,.2f}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("OTD % by Warehouse Hub")
    wh_otd = filtered_df.groupby("origin_warehouse")["on_time_flag"].mean() * 100
    st.bar_chart(wh_otd)

with col2:
    st.subheader("Freight Cost by Carrier")
    car_cost = filtered_df.groupby("carrier_name")["shipping_cost_usd"].sum()
    st.bar_chart(car_cost)
