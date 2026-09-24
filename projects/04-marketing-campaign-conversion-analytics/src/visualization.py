"""
Marketing Visual Analytics
Author: Farjad Zeya (Data Analyst)
"""

import os
import matplotlib.pyplot as plt
import pandas as pd

def generate_marketing_charts(cleaned_csv: str = "data/processed/marketing_leads_cleaned.csv", output_dir: str = "reports"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(cleaned_csv)
    
    # 1. Funnel Stages
    stages = ["Leads", "MQL", "SQL", "Opportunity", "Closed Won"]
    counts = [len(df), df["is_mql"].sum(), df["is_sql"].sum(), df["is_opportunity"].sum(), df["is_customer"].sum()]
    
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(stages, counts, color="#6366F1")
    ax.set_title("Marketing & Sales Conversion Funnel Progression", fontsize=11, fontweight="bold")
    ax.set_xlabel("Volume of Leads")
    for i, v in enumerate(counts):
        ax.text(v + 100, i, f"{v:,}", va="center", fontweight="bold", fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/funnel_progression.png", dpi=300)
    plt.close()
    print(f"[SUCCESS] Exported visuals to {output_dir}/")

if __name__ == "__main__":
    generate_marketing_charts()
