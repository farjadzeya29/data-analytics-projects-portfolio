"""
Marketing Conversion Data Cleaning Pipeline
Author: Farjad Zeya (Data Analyst)
"""

import os
import pandas as pd
import numpy as np

def clean_marketing_data(raw_csv: str, output_csv: str) -> pd.DataFrame:
    print(f"[INFO] Ingesting raw leads dataset from: {raw_csv}")
    df = pd.read_csv(raw_csv)
    initial_len = len(df)
    
    # 1. Deduplicate by lead_id
    df = df.drop_duplicates(subset=["lead_id"])
    print(f"[CLEAN] Deduplicated {initial_len - len(df)} duplicate lead records.")
    
    # 2. Impute null deal values with 0.00
    df["deal_value_usd"] = pd.to_numeric(df["deal_value_usd"], errors="coerce").fillna(0.0).round(2)
    
    # 3. String normalization
    df["marketing_channel"] = df["marketing_channel"].astype(str).str.strip().str.title()
    df["target_segment"] = df["target_segment"].astype(str).str.strip()
    df["funnel_stage"] = df["funnel_stage"].astype(str).str.strip()
    
    # 4. Standardize date
    df["lead_date"] = pd.to_datetime(df["lead_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"[SUCCESS] Exported {len(df)} sanitized leads to {output_csv}")
    return df

if __name__ == "__main__":
    clean_marketing_data("data/raw/marketing_leads_raw.csv", "data/processed/marketing_leads_cleaned.csv")
