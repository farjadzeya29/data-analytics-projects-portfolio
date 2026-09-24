import streamlit as st
import pandas as pd

st.set_page_config(page_title="Banking Churn Analytics | Farjad Zeya", layout="wide")
st.title("🏦 Banking Customer Churn & Retention Analytics")
st.caption("Portfolio Project by Farjad Zeya | Data Analyst (SQL • Python • Power BI)")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/banking_churn_cleaned.csv")

try:
    df = load_data()
except Exception:
    st.error("Data file not found. Run src/data_cleaning.py first.")
    st.stop()

# Sidebar
st.sidebar.header("Filter Segment")
geo_filter = st.sidebar.multiselect("Geography", df["geography"].unique(), default=df["geography"].unique())
tier_filter = st.sidebar.multiselect("Risk Tier", df["retention_risk_tier"].unique(), default=df["retention_risk_tier"].unique())

filtered = df[(df["geography"].isin(geo_filter)) & (df["retention_risk_tier"].isin(tier_filter))]

# KPIs
c1, c2, c3, c4 = st.columns(4)
total_cust = len(filtered)
churned = filtered["churn"].sum()
rate = (churned / total_cust * 100) if total_cust > 0 else 0
balance_lost = filtered[filtered["churn"] == 1]["account_balance"].sum()

c1.metric("Evaluated Customers", f"{total_cust:,}")
c2.metric("Churned Accounts", f"{churned:,}")
c3.metric("Churn Rate", f"{rate:.1f}%")
c4.metric("Capital at Risk ($)", f"${balance_lost:,.2f}")

st.divider()

t1, t2 = st.tabs(["Churn Drivers Analysis", "High-Risk Customer Worklist"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Churn Rate by Number of Products")
        prod_churn = filtered.groupby("num_of_products")["churn"].mean() * 100
        st.bar_chart(prod_churn)
    with col2:
        st.subheader("Churn Rate by Activity Status")
        act_churn = filtered.groupby("is_active_member")["churn"].mean() * 100
        act_churn.index = ["Inactive (0)", "Active (1)"]
        st.bar_chart(act_churn)

with t2:
    st.subheader("High-Risk Accounts for Retention Intervention")
    high_risk_df = filtered[filtered["retention_risk_tier"] == "High Risk"].sort_values("account_balance", ascending=False)
    st.dataframe(high_risk_df[["customer_id", "surname", "geography", "age", "account_balance", "num_of_products", "is_active_member", "churn"]].head(30), use_container_width=True)
