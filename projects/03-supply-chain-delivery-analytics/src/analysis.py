"""
Supply Chain Logistics Analytics & Bottleneck Identification
Author: Farjad Zeya (Data Analyst)
"""

import os
import pandas as pd
import numpy as np

def run_logistics_analysis(cleaned_csv: str = "data/processed/supply_chain_shipments_cleaned.csv"):
    df = pd.read_csv(cleaned_csv)
    
    total = len(df)
    ontime = df["on_time_flag"].sum()
    ontime_pct = (ontime / total) * 100
    avg_delay = df[df["delivery_status"] == "Delayed"]["delivery_delay_days"].mean()
    
    print(f"Network On-Time Delivery (OTD): {ontime_pct:.2f}%")
    print(f"Average Delay Duration: {avg_delay:.2f} days")
    
    # Origin Warehouse Performance
    wh_summary = df.groupby("origin_warehouse").agg(
        total_shipments=("shipment_id", "count"),
        ontime_deliveries=("on_time_flag", "sum"),
        avg_delay=("delivery_delay_days", "mean"),
        total_shipping_cost=("shipping_cost_usd", "sum")
    )
    wh_summary["otd_pct"] = (wh_summary["ontime_deliveries"] / wh_summary["total_shipments"]) * 100
    print("
--- Origin Warehouse Performance ---")
    print(wh_summary.round(2))
    
    # Supplier Tier Scorecard
    sup_summary = df.groupby(["supplier_name", "supplier_tier"]).agg(
        total_shipments=("shipment_id", "count"),
        ontime_deliveries=("on_time_flag", "sum"),
        damaged_count=("damage_flag", "sum")
    )
    sup_summary["otd_pct"] = (sup_summary["ontime_deliveries"] / sup_summary["total_shipments"]) * 100
    sup_summary["damage_rate_pct"] = (sup_summary["damaged_count"] / sup_summary["total_shipments"]) * 100
    print("
--- Supplier Performance Scorecard ---")
    print(sup_summary.round(2))

if __name__ == "__main__":
    run_logistics_analysis()
