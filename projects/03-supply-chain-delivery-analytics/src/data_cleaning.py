"""
Supply Chain Data Hygiene & Validation Engine
Author: Farjad Zeya (Data Analyst)
"""

import os
import pandas as pd
import numpy as np

def clean_supply_chain_data(raw_csv: str, output_csv: str) -> pd.DataFrame:
    print(f"[INFO] Ingesting raw logistics data from: {raw_csv}")
    df = pd.read_csv(raw_csv)
    initial_len = len(df)
    
    # 1. Deduplicate
    df = df.drop_duplicates(subset=["shipment_id"])
    print(f"[CLEAN] Deduplicated {initial_len - len(df)} duplicate shipments.")
    
    # 2. Fix negative weight anomalies
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce").abs().round(2)
    
    # 3. Text standardization
    df["delivery_status"] = df["delivery_status"].astype(str).str.strip().str.title()
    df["origin_warehouse"] = df["origin_warehouse"].astype(str).str.strip()
    df["carrier_name"] = df["carrier_name"].astype(str).str.strip()
    
    # 4. Standardize dates
    for col in ["order_date", "scheduled_delivery_date", "actual_delivery_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True).dt.strftime("%Y-%m-%d")
        
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"[SUCCESS] Exported {len(df)} validated shipments to {output_csv}")
    return df

if __name__ == "__main__":
    clean_supply_chain_data("data/raw/supply_chain_shipments_raw.csv", "data/processed/supply_chain_shipments_cleaned.csv")
