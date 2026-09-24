"""
Banking Churn Visualization Engine
Author: Farjad Zeya (Data Analyst)
"""

import os
import matplotlib.pyplot as plt
import pandas as pd

def export_churn_charts(cleaned_csv: str = "data/processed/banking_churn_cleaned.csv", output_dir: str = "reports"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(cleaned_csv)
    
    # 1. Churn by Product Count
    prod_churn = df.groupby("num_of_products")["exited"].mean() * 100
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#3B82F6", "#10B981", "#EF4444", "#991B1B"]
    ax.bar(prod_churn.index.astype(str), prod_churn.values, color=colors)
    ax.set_title("Customer Churn Rate by Number of Bank Products Held", fontsize=11, fontweight="bold")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_xlabel("Number of Products")
    for i, v in enumerate(prod_churn.values):
        ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold", fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/churn_by_product_count.png", dpi=300)
    plt.close()
    
    # 2. Churn by Geography
    geo_churn = df.groupby("geography")["exited"].mean() * 100
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(geo_churn.index, geo_churn.values, color=["#2563EB", "#DC2626", "#F59E0B"])
    ax.set_title("Customer Churn Rate by Country", fontsize=11, fontweight="bold")
    ax.set_ylabel("Churn Rate (%)")
    for i, v in enumerate(geo_churn.values):
        ax.text(i, v + 1.0, f"{v:.1f}%", ha="center", fontweight="bold", fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/churn_by_geography.png", dpi=300)
    plt.close()
    print(f"[SUCCESS] Exported visuals to {output_dir}/")

if __name__ == "__main__":
    export_churn_charts()
