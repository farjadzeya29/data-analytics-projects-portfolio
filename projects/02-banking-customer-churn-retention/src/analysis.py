"""
Banking Customer Retention Analytical Engine
Author: Farjad Zeya (Data Analyst)

Calculates:
- Baseline Attrition Rate & Capital at Risk
- Product Breadth Paradox (Attrition by Number of Products)
- Digital Engagement Penalty (Active vs Inactive)
- Regional Disparities (Germany vs France vs Spain)
- Retention Risk Score Composite
"""

import os
import pandas as pd
import numpy as np

def analyze_retention_patterns(cleaned_csv: str = "data/processed/banking_churn_cleaned.csv"):
    df = pd.read_csv(cleaned_csv)
    
    total = len(df)
    churned = df["exited"].sum()
    overall_churn_rate = (churned / total) * 100
    total_balance_at_risk = df[df["exited"] == 1]["balance"].sum()
    
    print(f"Overall Churn Rate: {overall_churn_rate:.2f}%")
    print(f"Total Capital Lost: ${total_balance_at_risk:,.2f}")
    
    # Breakdown by Product Count
    prod_table = df.groupby("num_of_products").agg(
        total_accounts=("customer_id", "count"),
        churned_accounts=("exited", "sum"),
        avg_balance=("balance", "mean")
    )
    prod_table["churn_rate_pct"] = (prod_table["churned_accounts"] / prod_table["total_accounts"]) * 100
    print("
--- Churn by Number of Products ---")
    print(prod_table.round(2))
    
    # Breakdown by Digital Activity
    act_table = df.groupby("is_active_member").agg(
        total_accounts=("customer_id", "count"),
        churned_accounts=("exited", "sum")
    )
    act_table["churn_rate_pct"] = (act_table["churned_accounts"] / act_table["total_accounts"]) * 100
    print("
--- Churn by Activity Status ---")
    print(act_table.round(2))
    
    return {
        "overall_churn_rate": round(overall_churn_rate, 2),
        "total_capital_lost": round(total_balance_at_risk, 2),
        "product_breakdown": prod_table.to_dict(orient="index")
    }

if __name__ == "__main__":
    analyze_retention_patterns()
