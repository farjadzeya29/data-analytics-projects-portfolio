import streamlit as st
import pandas as pd

st.set_page_config(page_title="Marketing Analytics | Farjad Zeya", layout="wide")
st.title("🎯 Marketing Campaign & Customer Conversion Analytics")
st.caption("Portfolio Project by Farjad Zeya | Data Analyst (SQL • Python • Power BI)")

@st.cache_data
def load_data():
    leads = pd.read_csv("data/processed/marketing_leads_cleaned.csv")
    cmp = pd.read_csv("data/processed/channel_performance_metrics.csv")
    return leads, cmp

try:
    leads, cmp = load_data()
except Exception:
    st.error("Data files not found. Run src/data_cleaning.py first.")
    st.stop()

# Filters
st.sidebar.header("Campaign Filters")
sel_channel = st.sidebar.multiselect("Channel", cmp["channel"].unique(), default=cmp["channel"].unique())
filtered_cmp = cmp[cmp["channel"].isin(sel_channel)]
filtered_leads = leads[leads["channel"].isin(sel_channel)]

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
spend = filtered_cmp["budget_spend_usd"].sum()
revenue = filtered_cmp["total_revenue_usd"].sum()
won = filtered_cmp["closed_won_customers"].sum()
cac = (spend / won) if won > 0 else 0
roas = (revenue / spend) if spend > 0 else 0

c1.metric("Total Spend ($)", f"${spend:,.2f}")
c2.metric("Attributed Revenue", f"${revenue:,.2f}")
c3.metric("Deals Won", f"{won:,}")
c4.metric("Blended CAC", f"${cac:,.2f}")
c5.metric("ROAS Multiplier", f"{roas:.2f}x")

st.divider()

t1, t2 = st.tabs(["Channel Performance & ROI", "Conversion Funnel Breakdown"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue vs Spend by Channel")
        st.bar_chart(filtered_cmp.set_index("channel")[["budget_spend_usd", "total_revenue_usd"]])
    with col2:
        st.subheader("ROAS Multiplier by Channel")
        st.bar_chart(filtered_cmp.set_index("channel")["roas_multiplier"])

with t2:
    st.subheader("Lead Funnel Progression")
    stage_order = ["Lead", "MQL", "SQL", "Opportunity", "Closed-Won", "Closed-Lost"]
    funnel_counts = filtered_leads["funnel_stage"].value_counts().reindex(stage_order).fillna(0)
    st.bar_chart(funnel_counts)
    st.dataframe(filtered_cmp[["campaign_name", "channel", "budget_spend_usd", "closed_won_customers", "cac_usd", "roas_multiplier"]], use_container_width=True)
