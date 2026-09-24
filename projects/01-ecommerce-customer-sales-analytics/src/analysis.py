"""
E-Commerce Customer & Sales Analytics - RFM & Business Intelligence
Author: Farjad Zeya (Data Analyst)

Performs:
- Customer RFM (Recency, Frequency, Monetary) Segmentation
- Category & Regional profitability analysis
- Pareto 80/20 revenue analysis
- Segment profile exports
"""

import pandas as pd
import numpy as np
from datetime import datetime

def perform_rfm_segmentation(df: pd.DataFrame, reference_date=None) -> pd.DataFrame:
    df["order_date"] = pd.to_datetime(df["order_date"])
    if reference_date is None:
        reference_date = df["order_date"].max() + pd.Timedelta(days=1)
    else:
        reference_date = pd.to_datetime(reference_date)
        
    rfm = df.groupby("customer_id").agg({
        "customer_name": "first",
        "segment": "first",
        "region": "first",
        "order_date": lambda x: (reference_date - x.max()).days,
        "order_id": "nunique",
        "sales_amount": "sum",
        "profit": "sum"
    }).reset_index()
    
    rfm.rename(columns={
        "order_date": "recency",
        "order_id": "frequency",
        "sales_amount": "monetary",
        "profit": "total_profit"
    }, inplace=True)
    
    # Quartile / Quantile Scores (1 to 5)
    rfm["r_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    rfm["rfm_composite"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)
    
    def assign_segment(row):
        r, f, m = row["r_score"], row["f_score"], row["m_score"]
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions (High-Value)"
        elif f >= 3 and m >= 3 and r >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 2:
            return "Promising New"
        elif r <= 2 and (f >= 3 or m >= 3):
            return "At-Risk Customers"
        elif r <= 2 and f <= 2:
            return "Lost / Hibernating"
        else:
            return "Needs Nurturing"
            
    rfm["customer_segment"] = rfm.apply(assign_segment, axis=1)
    return rfm

def compute_executive_kpis(df: pd.DataFrame) -> dict:
    total_revenue = df["sales_amount"].sum()
    total_profit = df["profit"].sum()
    return {
        "Total Revenue": round(total_revenue, 2),
        "Total Profit": round(total_profit, 2),
        "Profit Margin Pct": round((total_profit / total_revenue) * 100, 2),
        "Total Orders": df["order_id"].nunique(),
        "Total Customers": df["customer_id"].nunique(),
        "AOV": round(total_revenue / df["order_id"].nunique(), 2)
    }

if __name__ == "__main__":
    df = pd.read_csv("data/processed/ecommerce_transactions_cleaned.csv")
    kpis = compute_executive_kpis(df)
    print("Executive KPIs:", kpis)
    rfm = perform_rfm_segmentation(df)
    print("RFM Segment Distribution:\n", rfm["customer_segment"].value_counts())
