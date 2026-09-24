"""
Marketing Attribution & Funnel Analytics Suite
Author: Farjad Zeya (Data Analyst)
"""

import os
import pandas as pd
import numpy as np

def run_marketing_analysis(cleaned_csv: str = "data/processed/marketing_leads_cleaned.csv"):
    df = pd.read_csv(cleaned_csv)
    
    # Total Funnel Drop-off
    total_leads = len(df)
    mql = df["is_mql"].sum()
    sql = df["is_sql"].sum()
    opp = df["is_opportunity"].sum()
    won = df["is_customer"].sum()
    
    print("--- Funnel Progression ---")
    print(f"Total Leads: {total_leads:,}")
    print(f"MQL: {mql:,} ({(mql/total_leads)*100:.1f}%)")
    print(f"SQL: {sql:,} ({(sql/mql)*100:.1f}% of MQL)")
    print(f"Opportunity: {opp:,} ({(opp/sql)*100:.1f}% of SQL)")
    print(f"Closed Won: {won:,} ({(won/opp)*100:.1f}% of Opp)")

if __name__ == "__main__":
    run_marketing_analysis()
