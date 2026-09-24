import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="E-Commerce Analytics Portfolio | Farjad Zeya", layout="wide")

st.title("🛒 E-Commerce Customer & Sales Analytics")
st.caption("Portfolio Project by Farjad Zeya | Data Analyst (SQL • Python • Power BI)")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/ecommerce_transactions_cleaned.csv")
    rfm = pd.read_csv("data/processed/ecommerce_customers_rfm.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df, rfm

try:
    df, rfm = load_data()
except Exception:
    st.error("Data files not found. Run src/data_cleaning.py first.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Dashboard Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df["region"].unique(), default=df["region"].unique())
selected_category = st.sidebar.multiselect("Select Category", options=df["category"].unique(), default=df["category"].unique())

filtered_df = df[(df["region"].isin(selected_region)) & (df["category"].isin(selected_category))]

# Top KPIs
col1, col2, col3, col4, col5 = st.columns(5)
total_sales = filtered_df["sales_amount"].sum()
total_profit = filtered_df["profit"].sum()
margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df["order_id"].nunique()
aov = total_sales / total_orders if total_orders > 0 else 0

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{margin:.1f}%")
col4.metric("Total Orders", f"{total_orders:,}")
col5.metric("Avg Order Value", f"${aov:.2f}")

st.divider()

# Charts
tab1, tab2, tab3 = st.tabs(["Sales & Category Trends", "Customer RFM Segmentation", "Data Explorer"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by Category")
        cat_sales = filtered_df.groupby("category")["sales_amount"].sum().reset_index()
        st.bar_chart(cat_sales.set_index("category"))
    with c2:
        st.subheader("Monthly Sales Trajectory")
        monthly = filtered_df.set_index("order_date").resample("ME")["sales_amount"].sum().reset_index()
        st.line_chart(monthly.set_index("order_date"))

with tab2:
    st.subheader("RFM Customer Segmentation Distribution")
    seg_counts = rfm["customer_rfm_segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]
    st.dataframe(seg_counts, use_container_width=True)
    
    st.subheader("High-Value Champions & At-Risk Customers")
    st.dataframe(rfm[["customer_name", "customer_rfm_segment", "recency_days", "frequency_orders", "monetary_total_spend"]].head(15), use_container_width=True)

with tab3:
    st.subheader("Cleaned Dataset Inspection")
    st.dataframe(filtered_df.head(50), use_container_width=True)
