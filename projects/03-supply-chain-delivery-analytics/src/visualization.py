"""
Supply Chain Performance Visual Suite
Author: Farjad Zeya (Data Analyst)
"""

import os
import matplotlib.pyplot as plt
import pandas as pd

def generate_logistics_charts(cleaned_csv: str = "data/processed/supply_chain_shipments_cleaned.csv", output_dir: str = "reports"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(cleaned_csv)
    
    # 1. Warehouse OTD
    wh_otd = df.groupby("origin_warehouse")["on_time_flag"].mean() * 100
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ["#10B981" if v >= 80 else "#EF4444" for v in wh_otd.values]
    ax.barh(wh_otd.index, wh_otd.values, color=colors)
    ax.set_title("On-Time Delivery Rate (%) by Origin Warehouse Hub", fontsize=11, fontweight="bold")
    ax.set_xlabel("OTD (%)")
    for i, v in enumerate(wh_otd.values):
        ax.text(v + 1.0, i, f"{v:.1f}%", va="center", fontweight="bold", fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/warehouse_otd_benchmark.png", dpi=300)
    plt.close()
    print(f"[SUCCESS] Exported visuals to {output_dir}/")

if __name__ == "__main__":
    generate_logistics_charts()
