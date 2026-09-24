import streamlit as st
import pandas as pd

st.set_page_config(page_title="Marketing Conversion Analytics | Farjad Zeya", layout="wide")
st.title("🎯 Marketing Campaign & Customer Conversion Cockpit")
st.caption("Production Portfolio Project by Farjad Zeya | Data Analyst (SQL • Python • Power BI)")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/marketing_leads_cleaned.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

st.sidebar.header("Marketing Controls")
sel_channel = st.sidebar.multiselect("Channel", sorted(df["marketing_channel"].unique()), default=sorted(df["marketing_channel"].unique()))
sel_seg = st.sidebar.multiselect("Segment", sorted(df["target_segment"].unique()), default=sorted(df["target_segment"].unique()))

filtered_df = df[(df["marketing_channel"].isin(sel_channel)) & (df["target_segment"].isin(sel_seg))]

leads = len(filtered_df)
won = filtered_df["is_customer"].sum()
conv_rate = (won / leads * 100) if leads > 0 else 0
revenue = filtered_df["deal_value_usd"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Inbound Leads", f"{leads:,}")
c2.metric("Closed Won Customers", f"{won:,}")
c3.metric("Conversion Rate (%)", f"{conv_rate:.2f}%")
c4.metric("Pipeline Revenue ($)", f"${revenue:,.2f}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Revenue by Channel")
    ch_rev = filtered_df.groupby("marketing_channel")["deal_value_usd"].sum()
    st.bar_chart(ch_rev)

with col2:
    st.subheader("Conversion Rate by Segment")
    seg_conv = filtered_df.groupby("target_segment")["is_customer"].mean() * 100
    st.bar_chart(seg_conv)
