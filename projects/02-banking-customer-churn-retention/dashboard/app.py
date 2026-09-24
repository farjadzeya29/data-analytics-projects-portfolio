import streamlit as st
import pandas as pd

st.set_page_config(page_title="Banking Churn Analytics | Farjad Zeya", layout="wide")
st.title("🏦 Banking Customer Churn & Retention Cockpit")
st.caption("Production Portfolio Project by Farjad Zeya | Data Analyst (SQL • Python • Power BI)")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/banking_churn_cleaned.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Filters
st.sidebar.header("Cohort Filters")
sel_geo = st.sidebar.multiselect("Geography", sorted(df["geography"].unique()), default=sorted(df["geography"].unique()))
sel_prod = st.sidebar.multiselect("Products Held", sorted(df["num_of_products"].unique()), default=sorted(df["num_of_products"].unique()))

filtered_df = df[(df["geography"].isin(sel_geo)) & (df["num_of_products"].isin(sel_prod))]

total_accts = len(filtered_df)
churn_accts = filtered_df["exited"].sum()
churn_rate = (churn_accts / total_accts * 100) if total_accts > 0 else 0
lost_bal = filtered_df[filtered_df["exited"] == 1]["balance"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Accounts", f"{total_accts:,}")
c2.metric("Churned Accounts", f"{churn_accts:,}")
c3.metric("Churn Rate (%)", f"{churn_rate:.2f}%")
c4.metric("Capital at Risk ($)", f"${lost_bal:,.2f}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Churn Rate by Number of Products")
    p_churn = filtered_df.groupby("num_of_products")["exited"].mean() * 100
    st.bar_chart(p_churn)

with col2:
    st.subheader("Churn Rate by Country")
    g_churn = filtered_df.groupby("geography")["exited"].mean() * 100
    st.bar_chart(g_churn)
