"""
Banking Customer Churn Data Cleaning Pipeline
Author: Farjad Zeya (Data Analyst)

Pipeline actions:
1. Ingests raw banking records.
2. Removes duplicate customer IDs.
3. Corrects negative age values via absolute value transformation.
4. Imputes missing estimated salaries with median salary.
5. Normalizes text casing across country / geography fields.
"""

import os
import pandas as pd
import numpy as np

def clean_banking_data(raw_csv: str, output_csv: str) -> pd.DataFrame:
    print(f"[INFO] Ingesting raw banking data from: {raw_csv}")
    df = pd.read_csv(raw_csv)
    initial_len = len(df)
    
    # 1. Deduplicate by customer_id
    df = df.drop_duplicates(subset=["customer_id"])
    print(f"[CLEAN] Pruned {initial_len - len(df)} duplicate customer accounts.")
    
    # 2. Fix negative age outliers
    df["age"] = pd.to_numeric(df["age"], errors="coerce").abs()
    
    # 3. Impute missing salary with median
    med_salary = df["estimated_salary"].median()
    df["estimated_salary"] = df["estimated_salary"].fillna(med_salary).round(2)
    
    # 4. Normalize geography text
    df["geography"] = df["geography"].astype(str).str.strip().str.title()
    df["gender"] = df["gender"].astype(str).str.strip().str.title()
    
    # 5. Type casting
    df["credit_score"] = df["credit_score"].astype(int)
    df["tenure"] = df["tenure"].astype(int)
    df["balance"] = df["balance"].round(2)
    df["num_of_products"] = df["num_of_products"].astype(int)
    df["has_cr_card"] = df["has_cr_card"].astype(int)
    df["is_active_member"] = df["is_active_member"].astype(int)
    df["exited"] = df["exited"].astype(int)
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"[SUCCESS] Exported {len(df)} validated accounts to {output_csv}")
    return df

if __name__ == "__main__":
    clean_banking_data("data/raw/banking_churn_raw.csv", "data/processed/banking_churn_cleaned.csv")
