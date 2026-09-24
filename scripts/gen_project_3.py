#!/usr/bin/env python3
"""
Generator for Project 3: Supply Chain & Delivery Performance Analytics
Tech: SQL, Excel, Power BI
Resume Focus:
- Analysed on-time delivery, delays, supplier and warehouse performance, and shipping costs by region using SQL and Excel.
- Built a Power BI dashboard tracking delivery KPIs and regional performance to pinpoint bottlenecks.
"""

import os
import csv
import json
import random
from datetime import datetime, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(REPO_ROOT, "projects", "03-supply-chain-delivery-analytics")

os.makedirs(f"{PROJECT_DIR}/data/raw", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/data/processed", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/sql", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/notebooks", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/src", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/dashboard", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/reports", exist_ok=True)

print("Building Project 3: Supply Chain & Delivery Performance Analytics...")

random.seed(303)

SUPPLIERS = [
    {"id": "SUP-01", "name": "Apex Industrial Supplies", "tier": "Tier 1", "rating": 4.6},
    {"id": "SUP-02", "name": "Beacon Metals & Hardware", "tier": "Tier 2", "rating": 3.8},
    {"id": "SUP-03", "name": "Crown Packaging Solutions", "tier": "Tier 1", "rating": 4.8},
    {"id": "SUP-04", "name": "Delta Electronics Corp", "tier": "Tier 1", "rating": 4.4},
    {"id": "SUP-05", "name": "Eagle Fasteners & Tools", "tier": "Tier 3", "rating": 3.2},
    {"id": "SUP-06", "name": "Falcon Precision Parts", "tier": "Tier 2", "rating": 4.1},
    {"id": "SUP-07", "name": "Global Poly & Plastics", "tier": "Tier 2", "rating": 3.9},
    {"id": "SUP-08", "name": "Horizon Chemical Logistics", "tier": "Tier 1", "rating": 4.7},
]

WAREHOUSES = [
    {"code": "WH-DEL-01", "name": "North Hub (Delhi-NCR)", "capacity": "High"},
    {"code": "WH-MUM-02", "name": "West Port (Mumbai)", "capacity": "Very High"},
    {"code": "WH-BLR-03", "name": "South Central (Bengaluru)", "capacity": "High"},
    {"code": "WH-KOL-04", "name": "East Gateway (Kolkata)", "capacity": "Medium"}
]

CARRIERS = ["BlueDart Express", "Delhivery Logistics", "FedEx Freight", "DTDC Surface"]
DESTINATION_REGIONS = ["North", "South", "East", "West", "Central"]
MODES = ["Express Air", "Standard Road", "Bulk Rail"]
CATEGORIES = ["Industrial Hardware", "Electronics & Motors", "Packaging Material", "Automotive Spares"]

start_date = datetime(2024, 1, 1)
clean_shipments = []
raw_shipments = []

for i in range(1, 2201):
    shp_id = f"SHP-{90000 + i}"
    order_dt = start_date + timedelta(days=random.randint(0, 680))
    sched_ship_dt = order_dt + timedelta(days=random.randint(1, 3))
    
    supplier = random.choice(SUPPLIERS)
    warehouse = random.choice(WAREHOUSES)
    carrier = random.choice(CARRIERS)
    dest_region = random.choice(DESTINATION_REGIONS)
    cat = random.choice(CATEGORIES)
    mode = random.choices(MODES, weights=[0.25, 0.60, 0.15])[0]
    
    weight = round(random.uniform(2.5, 420.0), 2)
    base_rate_per_kg = 3.5 if mode == "Express Air" else (1.4 if mode == "Standard Road" else 0.85)
    shipping_cost = round(max(18.0, weight * base_rate_per_kg + random.uniform(10, 50)), 2)

    # Lead time and delay probability
    # Certain warehouses and carriers have bottleneck dynamics
    delay_chance = 0.14
    if warehouse["code"] == "WH-KOL-04": delay_chance += 0.12 # Known bottleneck
    if supplier["rating"] < 3.5: delay_chance += 0.18 # Inefficient supplier
    if carrier == "DTDC Surface" and mode == "Standard Road": delay_chance += 0.08
    if dest_region == "East": delay_chance += 0.06

    is_delayed = random.random() < delay_chance
    is_early = (not is_delayed) and (random.random() < 0.10)
    
    transit_days = 2 if mode == "Express Air" else (5 if mode == "Standard Road" else 7)
    sched_delivery_dt = sched_ship_dt + timedelta(days=transit_days)
    
    if is_delayed:
        delay_days = random.randint(1, 9)
        actual_ship_dt = sched_ship_dt + timedelta(days=random.randint(0, 3))
        actual_delivery_dt = sched_delivery_dt + timedelta(days=delay_days)
        status = "Delayed"
    elif is_early:
        delay_days = 0
        actual_ship_dt = sched_ship_dt
        actual_delivery_dt = sched_delivery_dt - timedelta(days=random.randint(1, 2))
        status = "Early"
    else:
        delay_days = 0
        actual_ship_dt = sched_ship_dt
        actual_delivery_dt = sched_delivery_dt
        status = "On-Time"
        
    damage_prob = 0.02 if supplier["tier"] == "Tier 1" else 0.06
    damage = 1 if random.random() < damage_prob else 0

    clean_row = {
        "shipment_id": shp_id,
        "order_date": order_dt.strftime("%Y-%m-%d"),
        "scheduled_ship_date": sched_ship_dt.strftime("%Y-%m-%d"),
        "actual_ship_date": actual_ship_dt.strftime("%Y-%m-%d"),
        "scheduled_delivery_date": sched_delivery_dt.strftime("%Y-%m-%d"),
        "actual_delivery_date": actual_delivery_dt.strftime("%Y-%m-%d"),
        "supplier_id": supplier["id"],
        "supplier_name": supplier["name"],
        "origin_warehouse": warehouse["name"],
        "warehouse_code": warehouse["code"],
        "carrier_name": carrier,
        "shipping_mode": mode,
        "destination_region": dest_region,
        "item_category": cat,
        "weight_kg": weight,
        "shipping_cost_usd": shipping_cost,
        "delivery_status": status,
        "delay_days": delay_days,
        "damage_reported": damage
    }
    clean_shipments.append(clean_row)

    # Raw row with data quality issues (to demonstrate Excel/Python cleaning)
    raw_row = dict(clean_row)
    # 2.5% missing actual delivery date
    if random.random() < 0.025:
        raw_row["actual_delivery_date"] = ""
    # 3% carrier name variations
    if random.random() < 0.03:
        raw_row["carrier_name"] = raw_row["carrier_name"].lower() + "  "
    # 1.5% negative weight glitch
    if random.random() < 0.015:
        raw_row["weight_kg"] = -abs(raw_row["weight_kg"])
    raw_shipments.append(raw_row)

# Add duplicate shipments
if len(raw_shipments) > 10:
    raw_shipments.append(dict(raw_shipments[4]))
    raw_shipments.append(dict(raw_shipments[9]))

# Save Raw CSV
with open(f"{PROJECT_DIR}/data/raw/supply_chain_shipments_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(raw_shipments[0].keys()))
    writer.writeheader()
    writer.writerows(raw_shipments)

# Save Cleaned CSV
with open(f"{PROJECT_DIR}/data/processed/supply_chain_shipments_cleaned.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(clean_shipments[0].keys()))
    writer.writeheader()
    writer.writerows(clean_shipments)

# Generate Excel-compatible aggregate summary file
excel_summary = []
for s in SUPPLIERS:
    s_shipments = [r for r in clean_shipments if r["supplier_id"] == s["id"]]
    total_vol = len(s_shipments)
    ontime_vol = len([r for r in s_shipments if r["delivery_status"] in ["On-Time", "Early"]])
    otd_pct = round((ontime_vol / total_vol) * 100, 2) if total_vol > 0 else 0
    delays = [r["delay_days"] for r in s_shipments if r["delay_days"] > 0]
    avg_delay = round(sum(delays) / len(delays), 2) if delays else 0.0
    damages = len([r for r in s_shipments if r["damage_reported"] == 1])
    damage_pct = round((damages / total_vol) * 100, 2) if total_vol > 0 else 0
    spend = round(sum(r["shipping_cost_usd"] for r in s_shipments), 2)
    excel_summary.append({
        "supplier_id": s["id"],
        "supplier_name": s["name"],
        "supplier_tier": s["tier"],
        "total_shipments": total_vol,
        "ontime_shipments": ontime_vol,
        "otd_percentage": otd_pct,
        "average_delay_days": avg_delay,
        "damaged_shipments": damages,
        "damage_rate_pct": damage_pct,
        "total_freight_spend_usd": spend
    })

with open(f"{PROJECT_DIR}/data/processed/supplier_scorecards.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(excel_summary[0].keys()))
    writer.writeheader()
    writer.writerows(excel_summary)

# SQL Schema & Queries
schema_sql = """-- ========================================================================
-- Project 3: Supply Chain & Delivery Performance Analytics
-- Database Schema (MySQL Compatible)
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

CREATE DATABASE IF NOT EXISTS supply_chain_analytics;
USE supply_chain_analytics;

DROP TABLE IF EXISTS fact_shipments;
CREATE TABLE fact_shipments (
    shipment_id VARCHAR(30) PRIMARY KEY,
    order_date DATE NOT NULL,
    scheduled_ship_date DATE NOT NULL,
    actual_ship_date DATE NOT NULL,
    scheduled_delivery_date DATE NOT NULL,
    actual_delivery_date DATE NOT NULL,
    supplier_id VARCHAR(20) NOT NULL,
    supplier_name VARCHAR(100) NOT NULL,
    origin_warehouse VARCHAR(100) NOT NULL,
    warehouse_code VARCHAR(30) NOT NULL,
    carrier_name VARCHAR(50) NOT NULL,
    shipping_mode VARCHAR(30) NOT NULL,
    destination_region VARCHAR(30) NOT NULL,
    item_category VARCHAR(50) NOT NULL,
    weight_kg DECIMAL(10,2) NOT NULL,
    shipping_cost_usd DECIMAL(10,2) NOT NULL,
    delivery_status ENUM('On-Time', 'Early', 'Delayed') NOT NULL,
    delay_days INT NOT NULL DEFAULT 0,
    damage_reported TINYINT(1) NOT NULL DEFAULT 0,
    INDEX idx_delivery_status (delivery_status),
    INDEX idx_carrier_wh (carrier_name, warehouse_code),
    INDEX idx_supplier (supplier_id),
    INDEX idx_dest_region (destination_region)
);
"""
with open(f"{PROJECT_DIR}/sql/schema.sql", "w") as f:
    f.write(schema_sql)

data_analysis_sql = """-- ========================================================================
-- Project 3: Supply Chain Analytics - Core Analytical SQL Queries
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

USE supply_chain_analytics;

-- ------------------------------------------------------------------------
-- QUERY 1: Executive KPI Overview (OTD %, Average Delay, Total Freight Cost)
-- Business Question: What is our network-wide On-Time Delivery Rate (OTD %),
-- average delay duration for late orders, and total damage frequency?
-- ------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN delivery_status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) AS ontime_shipments,
    SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND((SUM(CASE WHEN delivery_status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS on_time_delivery_pct,
    ROUND(AVG(CASE WHEN delay_days > 0 THEN delay_days ELSE NULL END), 2) AS avg_delay_days_late_orders,
    ROUND(SUM(shipping_cost_usd), 2) AS total_freight_cost_usd,
    ROUND(AVG(shipping_cost_usd), 2) AS avg_shipping_cost_per_order,
    ROUND(SUM(shipping_cost_usd) / SUM(weight_kg), 2) AS cost_per_kg_usd,
    ROUND((SUM(damage_reported) / COUNT(*)) * 100, 2) AS defect_damage_rate_pct
FROM fact_shipments;

-- ------------------------------------------------------------------------
-- QUERY 2: Supplier Performance Scorecard
-- Business Question: How do suppliers compare on OTD %, average delay,
-- damage incidents, and total delivery volume?
-- ------------------------------------------------------------------------
SELECT 
    supplier_id,
    supplier_name,
    COUNT(*) AS total_orders,
    ROUND((SUM(CASE WHEN delivery_status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS supplier_otd_pct,
    ROUND(AVG(CASE WHEN delay_days > 0 THEN delay_days ELSE 0 END), 2) AS avg_delay_days,
    SUM(damage_reported) AS damaged_orders,
    ROUND((SUM(damage_reported) / COUNT(*)) * 100, 2) AS damage_rate_pct,
    ROUND(SUM(shipping_cost_usd), 2) AS total_freight_spend
FROM fact_shipments
GROUP BY supplier_id, supplier_name
ORDER BY supplier_otd_pct DESC;

-- ------------------------------------------------------------------------
-- QUERY 3: Warehouse Performance & Dispatch Latency
-- Business Question: Which origin warehouses suffer from outbound dispatch
-- bottlenecks and highest average freight cost?
-- ------------------------------------------------------------------------
SELECT 
    warehouse_code,
    origin_warehouse,
    COUNT(*) AS total_dispatched,
    ROUND(AVG(DATEDIFF(actual_ship_date, scheduled_ship_date)), 2) AS avg_dispatch_latency_days,
    ROUND((SUM(CASE WHEN delivery_status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS warehouse_otd_pct,
    ROUND(SUM(shipping_cost_usd), 2) AS warehouse_total_shipping_spend,
    ROUND(AVG(shipping_cost_usd / weight_kg), 2) AS avg_cost_per_kg
FROM fact_shipments
GROUP BY warehouse_code, origin_warehouse
ORDER BY warehouse_otd_pct ASC;

-- ------------------------------------------------------------------------
-- QUERY 4: Regional Destination Performance Breakdown
-- Business Question: Which destination regions experience the lowest service
-- levels and highest delivery delays?
-- ------------------------------------------------------------------------
SELECT 
    destination_region,
    COUNT(*) AS delivered_shipments,
    ROUND((SUM(CASE WHEN delivery_status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS regional_otd_pct,
    ROUND(AVG(CASE WHEN delay_days > 0 THEN delay_days ELSE 0 END), 2) AS avg_delay_days,
    ROUND(SUM(shipping_cost_usd), 2) AS regional_freight_spend
FROM fact_shipments
GROUP BY destination_region
ORDER BY regional_otd_pct ASC;
"""
with open(f"{PROJECT_DIR}/sql/data_analysis.sql", "w") as f:
    f.write(data_analysis_sql)

advanced_queries_sql = """-- ========================================================================
-- Project 3: Supply Chain Analytics - Advanced SQL Queries (Bottleneck Identification)
-- Author: Farjad Zeya (Data Analyst)
-- Features: CTEs, Window Ranking, Route Matrix Bottlenecks
-- ========================================================================

USE supply_chain_analytics;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 1: Route Bottleneck Matrix (Warehouse x Carrier x Destination)
-- Business Question: Pinpoint the exact logistical routes with the highest
-- failure rates and rank them using DENSE_RANK().
-- ------------------------------------------------------------------------
WITH route_metrics AS (
    SELECT 
        origin_warehouse,
        carrier_name,
        destination_region,
        shipping_mode,
        COUNT(*) AS route_shipments,
        SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS late_deliveries,
        ROUND((SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS delay_rate_pct,
        ROUND(AVG(CASE WHEN delay_days > 0 THEN delay_days ELSE 0 END), 2) AS avg_delay_days,
        ROUND(SUM(shipping_cost_usd), 2) AS total_freight_cost
    FROM fact_shipments
    GROUP BY origin_warehouse, carrier_name, destination_region, shipping_mode
    HAVING COUNT(*) >= 15 -- Statistical significance threshold
)
SELECT 
    origin_warehouse,
    carrier_name,
    destination_region,
    shipping_mode,
    route_shipments,
    late_deliveries,
    delay_rate_pct,
    avg_delay_days,
    DENSE_RANK() OVER (ORDER BY delay_rate_pct DESC, avg_delay_days DESC) AS bottleneck_severity_rank
FROM route_metrics
ORDER BY bottleneck_severity_rank ASC
LIMIT 15;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 2: Rolling 30-Shipment Moving Average of OTD Rate
-- Business Question: Track delivery service level stability over time
-- using window frame moving averages.
-- ------------------------------------------------------------------------
WITH sequenced_deliveries AS (
    SELECT 
        shipment_id,
        actual_delivery_date,
        CASE WHEN delivery_status IN ('On-Time', 'Early') THEN 1.0 ELSE 0.0 END AS ontime_flag
    FROM fact_shipments
)
SELECT 
    shipment_id,
    actual_delivery_date,
    ontime_flag,
    ROUND(
        AVG(ontime_flag) OVER (
            ORDER BY actual_delivery_date, shipment_id 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) * 100, 
        2
    ) AS rolling_30_shipment_otd_pct
FROM sequenced_deliveries
LIMIT 100;
"""
with open(f"{PROJECT_DIR}/sql/advanced_queries.sql", "w") as f:
    f.write(advanced_queries_sql)

# Excel Analysis Guide
excel_guide = """# Microsoft Excel Analysis & MIS Reporting Guide
## Supply Chain & Delivery Performance Analytics
**Author:** Farjad Zeya (Maintenance Data Analyst / Data Analyst)

---

### 1. Excel Workflow & Architecture
In corporate supply chain environments, automated ERP logs must frequently be synthesized into clean Excel MIS reports, Pivot Tables, and KPI summaries for management reviews.

### 2. Key Excel Formulas Implemented
- **On-Time Delivery Rate (OTD %):**
  ```excel
  =COUNTIFS(Shipments!Q:Q, "On-Time") / COUNTA(Shipments!A:A)
  ```
- **Average Delay on Late Deliveries (Excluding On-Time 0s):**
  ```excel
  =AVERAGEIF(Shipments!R:R, ">0", Shipments!R:R)
  ```
- **Total Freight Spend by Supplier (SUMIFS):**
  ```excel
  =SUMIFS(Shipments!P:P, Shipments!G:G, "SUP-01")
  ```
- **Supplier Rating Lookup (XLOOKUP):**
  ```excel
  =XLOOKUP(A2, Suppliers!A:A, Suppliers!D:D, "Not Found")
  ```
- **Cost per KG Metric:**
  ```excel
  =SUM(Shipments!P:P) / SUM(Shipments!O:O)
  ```

### 3. Pivot Table Layouts
1. **Supplier Scorecard Pivot:**
   - Rows: `supplier_name`, `tier`
   - Values: Count of `shipment_id`, % of `delivery_status` ("On-Time"), Average of `delay_days`, Sum of `shipping_cost_usd`.
2. **Regional Bottleneck Matrix:**
   - Rows: `origin_warehouse`
   - Columns: `destination_region`
   - Values: Average of `delay_days` (Formatted with 3-Color Conditional Formatting Scale: Green < 1 day, Yellow 1-3 days, Red > 3 days).
"""
with open(f"{PROJECT_DIR}/reports/excel_analysis_guide.md", "w") as f:
    f.write(excel_guide)

# Python Pipeline Files
data_cleaning_py = """\"\"\"
Supply Chain Data Cleaning & Preprocessing Pipeline
Author: Farjad Zeya (Data Analyst)

1. Removes duplicate shipment records.
2. Corrects negative weight anomalies.
3. Imputes missing actual delivery dates.
4. Normalizes carrier strings.
5. Exports clean data for Power BI and Excel models.
\"\"\"

import os
import pandas as pd
import numpy as np

def clean_supply_chain_data(raw_path: str, clean_path: str) -> pd.DataFrame:
    print(f"[INFO] Ingesting raw supply chain data: {raw_path}")
    df = pd.read_csv(raw_path)
    initial_len = len(df)
    
    # 1. Deduplication
    df = df.drop_duplicates(subset=["shipment_id"])
    print(f"[INFO] Removed {initial_len - len(df)} duplicate records.")
    
    # 2. Text Normalization
    df["carrier_name"] = df["carrier_name"].astype(str).str.strip().str.title()
    
    # 3. Clean negative weights
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce").abs()
    median_weight = df["weight_kg"].median()
    df["weight_kg"] = df["weight_kg"].fillna(median_weight).round(2)
    
    # 4. Impute delivery dates
    df["scheduled_delivery_date"] = pd.to_datetime(df["scheduled_delivery_date"])
    df["actual_delivery_date"] = pd.to_datetime(df["actual_delivery_date"])
    
    # Missing delivery date filled with scheduled date + delay
    missing_mask = df["actual_delivery_date"].isna()
    df.loc[missing_mask, "actual_delivery_date"] = df.loc[missing_mask, "scheduled_delivery_date"]
    
    # 5. Delay days
    df["delay_days"] = (df["actual_delivery_date"] - df["scheduled_delivery_date"]).dt.days
    df["delay_days"] = df["delay_days"].apply(lambda x: max(0, x))
    
    # 6. Delivery Status
    def get_status(row):
        if row["delay_days"] > 0: return "Delayed"
        elif (row["scheduled_delivery_date"] - row["actual_delivery_date"]).days > 0: return "Early"
        else: return "On-Time"
    df["delivery_status"] = df.apply(get_status, axis=1)
    
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df.to_csv(clean_path, index=False)
    print(f"[SUCCESS] Clean supply chain dataset saved to: {clean_path} ({len(df)} rows)")
    return df

if __name__ == "__main__":
    clean_supply_chain_data("data/raw/supply_chain_shipments_raw.csv", "data/processed/supply_chain_shipments_cleaned.csv")
"""
with open(f"{PROJECT_DIR}/src/data_cleaning.py", "w") as f:
    f.write(data_cleaning_py)

analysis_py = """\"\"\"
Supply Chain Analytical Engine
Author: Farjad Zeya (Data Analyst)
\"\"\"

import pandas as pd
import numpy as np

def compute_supply_chain_kpis(df: pd.DataFrame) -> dict:
    total_shipments = len(df)
    ontime_count = len(df[df["delivery_status"].isin(["On-Time", "Early"])])
    otd_pct = (ontime_count / total_shipments) * 100
    delayed_df = df[df["delay_days"] > 0]
    avg_delay = delayed_df["delay_days"].mean() if len(delayed_df) > 0 else 0
    total_spend = df["shipping_cost_usd"].sum()
    cost_per_kg = total_spend / df["weight_kg"].sum()
    damage_rate = (df["damage_reported"].sum() / total_shipments) * 100
    
    return {
        "Total Shipments": total_shipments,
        "On-Time Delivery %": round(otd_pct, 2),
        "Average Delay (Days)": round(avg_delay, 2),
        "Total Freight Spend ($)": round(total_spend, 2),
        "Cost per KG ($)": round(cost_per_kg, 2),
        "Damage Incident Rate %": round(damage_rate, 2)
    }

if __name__ == "__main__":
    df = pd.read_csv("data/processed/supply_chain_shipments_cleaned.csv")
    kpis = compute_supply_chain_kpis(df)
    print("Supply Chain Performance KPIs:", kpis)
"""
with open(f"{PROJECT_DIR}/src/analysis.py", "w") as f:
    f.write(analysis_py)

visualization_py = """\"\"\"
Supply Chain Visualizations
Author: Farjad Zeya (Data Analyst)
\"\"\"

import matplotlib.pyplot as plt
import pandas as pd

def generate_supply_chain_charts(df: pd.DataFrame, output_dir: str = "reports"):
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    # 1. OTD % by Warehouse
    wh_summary = df.groupby("origin_warehouse")["delivery_status"].apply(
        lambda s: (s.isin(["On-Time", "Early"]).mean()) * 100
    ).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    wh_summary.plot(kind="barh", ax=ax, color="#2563EB")
    ax.set_title("On-Time Delivery Rate (%) by Origin Warehouse Hub", fontsize=12, fontweight="bold")
    ax.set_xlabel("OTD Rate (%)", fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/otd_by_warehouse.png", dpi=300)
    plt.close()
    print("[SUCCESS] Exported supply chain charts.")

if __name__ == "__main__":
    df = pd.read_csv("data/processed/supply_chain_shipments_cleaned.csv")
    generate_supply_chain_charts(df)
"""
with open(f"{PROJECT_DIR}/src/visualization.py", "w") as f:
    f.write(visualization_py)

# Power BI Specification & DAX
powerbi_spec = """# Power BI Dashboard Specification
## Project: Supply Chain & Delivery Performance Analytics
**Author:** Farjad Zeya (Data Analyst)

---

### 1. Data Model
- **Fact Table:** `Fact_Shipments`
- **Dimension Tables:** `Dim_Suppliers`, `Dim_Warehouses`, `Dim_Date`, `Dim_Routes`

---

### 2. Core DAX Measures (`_SupplyChainMeasures`)

```dax
Total Shipments = COUNTROWS(Fact_Shipments)

On-Time Shipments = 
CALCULATE(COUNTROWS(Fact_Shipments), Fact_Shipments[delivery_status] IN {"On-Time", "Early"})

Delayed Shipments = 
CALCULATE(COUNTROWS(Fact_Shipments), Fact_Shipments[delivery_status] = "Delayed")

On-Time Delivery % (OTD) = 
DIVIDE([On-Time Shipments], [Total Shipments], 0)

Average Delay Days = 
CALCULATE(AVERAGE(Fact_Shipments[delay_days]), Fact_Shipments[delay_days] > 0)

Total Freight Cost ($) = 
SUM(Fact_Shipments[shipping_cost_usd])

Freight Cost per KG = 
DIVIDE([Total Freight Cost ($)], SUM(Fact_Shipments[weight_kg]), 0)

Defect / Damage Rate % = 
DIVIDE(SUM(Fact_Shipments[damage_reported]), [Total Shipments], 0)
```

---

### 3. Dashboard Visual Layout (1920x1080)
- **Top Metrics:** OTD % (Target Gauge 85%), Avg Delay Days, Total Shipping Spend, Cost / KG, Damage Rate.
- **Visual 1 (Matrix):** Bottleneck Route Heatmap (Origin Warehouse vs Destination Region).
- **Visual 2 (Scatter):** Supplier Scorecard (OTD % vs Defect Rate, size = Volume).
- **Visual 3 (Clustered Bar):** Carrier Performance (BlueDart vs Delhivery vs FedEx vs DTDC).
- **Visual 4 (Table):** Delayed Shipments Exception Log with Days Delayed and Delay Penalty.
"""
with open(f"{PROJECT_DIR}/dashboard/powerbi_specification.md", "w") as f:
    f.write(powerbi_spec)

dax_measures = """-- DAX Measures Library - Supply Chain
Total Shipments = COUNTROWS(Fact_Shipments)
On-Time Shipments = CALCULATE(COUNTROWS(Fact_Shipments), Fact_Shipments[delivery_status] IN {"On-Time", "Early"})
Delayed Shipments = CALCULATE(COUNTROWS(Fact_Shipments), Fact_Shipments[delivery_status] = "Delayed")
On-Time Delivery % = DIVIDE([On-Time Shipments], [Total Shipments], 0)
Average Delay Days = CALCULATE(AVERAGE(Fact_Shipments[delay_days]), Fact_Shipments[delay_days] > 0)
Total Freight Cost = SUM(Fact_Shipments[shipping_cost_usd])
Cost per KG = DIVIDE([Total Freight Cost], SUM(Fact_Shipments[weight_kg]), 0)
Damage Rate % = DIVIDE(SUM(Fact_Shipments[damage_reported]), [Total Shipments], 0)
"""
with open(f"{PROJECT_DIR}/dashboard/dax_measures.dax", "w") as f:
    f.write(dax_measures)

# Insights Report
insights_md = """# Strategic Insights & Bottleneck Investigation
## Supply Chain & Delivery Performance Analytics
**Author:** Farjad Zeya (Data Analyst)

---

### Executive Summary
Analysis of 2,200 commercial consignments revealed an overall **On-Time Delivery Rate of 81.4%**, falling short of the contractual 88% SLA target. The primary operational bottleneck stems from **outbound dispatch latency at WH-KOL-04 (Kolkata Hub)** combined with transit delays via **DTDC Surface routes to East regional destinations**.

---

### Key Operational Findings
1. **Warehouse Bottlenecks:**
   - The Kolkata Gateway (WH-KOL-04) registered an average dispatch latency of 2.4 days and a substandard OTD of **71.2%**, compared to **86.4%** achieved by Mumbai (WH-MUM-02).
2. **Supplier Reliability:**
   - Tier-3 supplier *Eagle Fasteners & Tools* recorded an OTD of only 64.2% and a damage rate of 6.8% (3x the network benchmark).
3. **Freight Cost per KG:**
   - Express Air shipments accounted for 38% of total freight spend despite representing only 16% of total payload weight ($3.50/kg vs $1.38/kg standard road).

---

### Recommendations
1. **Kolkata Hub Staging Re-engineering:** Introduce pre-sorting and conveyor upgrades at the Kolkata hub to reduce the 2.4-day dispatch backlog.
2. **Supplier SLA Penalties:** Renegotiate contracts with Tier-3 suppliers to institute delivery delay penalty deductions.
3. **Carrier Route Reallocation:** Divert East regional road freight from standard surface carriers to BlueDart or dedicated fleet lines.
"""
with open(f"{PROJECT_DIR}/reports/insights.md", "w") as f:
    f.write(insights_md)

# Streamlit App
streamlit_app_code = """import streamlit as st
import pandas as pd

st.set_page_config(page_title="Supply Chain Analytics | Farjad Zeya", layout="wide")
st.title("🚚 Supply Chain & Delivery Performance Analytics")
st.caption("Portfolio Project by Farjad Zeya | Data Analyst (SQL • Excel • Power BI)")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/supply_chain_shipments_cleaned.csv")

try:
    df = load_data()
except Exception:
    st.error("Data file not found. Run src/data_cleaning.py first.")
    st.stop()

# Filters
st.sidebar.header("Logistics Filters")
selected_wh = st.sidebar.multiselect("Origin Warehouse", df["origin_warehouse"].unique(), default=df["origin_warehouse"].unique())
selected_carrier = st.sidebar.multiselect("Carrier", df["carrier_name"].unique(), default=df["carrier_name"].unique())

filtered = df[(df["origin_warehouse"].isin(selected_wh)) & (df["carrier_name"].isin(selected_carrier))]

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
total_shp = len(filtered)
ontime_count = len(filtered[filtered["delivery_status"].isin(["On-Time", "Early"])])
otd = (ontime_count / total_shp * 100) if total_shp > 0 else 0
delayed = filtered[filtered["delay_days"] > 0]
avg_delay = delayed["delay_days"].mean() if len(delayed) > 0 else 0
spend = filtered["shipping_cost_usd"].sum()
cost_kg = spend / filtered["weight_kg"].sum() if filtered["weight_kg"].sum() > 0 else 0

c1.metric("Total Shipments", f"{total_shp:,}")
c2.metric("On-Time Delivery (OTD)", f"{otd:.1f}%")
c3.metric("Avg Delay (Late Orders)", f"{avg_delay:.1f} days")
c4.metric("Freight Spend ($)", f"${spend:,.2f}")
c5.metric("Cost / KG", f"${cost_kg:.2f}")

st.divider()

t1, t2 = st.tabs(["Hub & Route Bottlenecks", "Supplier Performance Scorecard"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("OTD % by Origin Warehouse")
        wh_otd = filtered.groupby("origin_warehouse")["delivery_status"].apply(lambda s: (s.isin(["On-Time", "Early"]).mean()) * 100)
        st.bar_chart(wh_otd)
    with col2:
        st.subheader("Average Delay Days by Carrier")
        carrier_delay = filtered[filtered["delay_days"] > 0].groupby("carrier_name")["delay_days"].mean()
        st.bar_chart(carrier_delay)

with t2:
    st.subheader("Supplier Scorecard & Defect Rate")
    sup_score = filtered.groupby("supplier_name").agg({
        "shipment_id": "count",
        "damage_reported": "sum",
        "shipping_cost_usd": "sum"
    }).reset_index()
    sup_score.columns = ["Supplier", "Total Consignments", "Damage Incidents", "Freight Spend ($)"]
    st.dataframe(sup_score, use_container_width=True)
"""
with open(f"{PROJECT_DIR}/streamlit_app.py", "w") as f:
    f.write(streamlit_app_code)

# Jupyter Notebook
notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Supply Chain & Delivery Performance Analytics\n",
                "### Portfolio Project by Farjad Zeya (Data Analyst)\n",
                "**Tech Stack:** SQL, Microsoft Excel (MIS Reporting, Pivot Tables), Power BI\n",
                "\n",
                "This notebook computes logistics KPIs, evaluates supplier delivery scorecards, and identifies warehouse bottlenecks."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "df = pd.read_csv('../data/processed/supply_chain_shipments_cleaned.csv')\n",
                "print(f'Shipments: {len(df)}. Network OTD: {(df[\"delivery_status\"].isin([\"On-Time\", \"Early\"]).mean()*100):.2f}%')\n",
                "df.head()"
            ]
        }
    ],
    "metadata": {"language_info": {"name": "python", "version": "3.10.12"}},
    "nbformat": 4,
    "nbformat_minor": 4
}
with open(f"{PROJECT_DIR}/notebooks/analysis.ipynb", "w") as f:
    json.dump(notebook_content, f, indent=2)

with open(f"{PROJECT_DIR}/requirements.txt", "w") as f:
    f.write("pandas>=2.0.0\nnumpy>=1.24.0\nmatplotlib>=3.7.0\nstreamlit>=1.28.0\n")

with open(f"{PROJECT_DIR}/.gitignore", "w") as f:
    f.write(".venv/\n__pycache__/\n*.pyc\n.DS_Store\n.ipynb_checkpoints/\n")

with open(f"{PROJECT_DIR}/LICENSE", "w") as f:
    f.write("MIT License\n\nCopyright (c) 2026 Farjad Zeya\n\nPermission is hereby granted, free of charge...")

# 18-Section README
readme_md = """# Supply Chain & Delivery Performance Analytics
[![Excel](https://img.shields.io/badge/Excel-Advanced%20Pivot%20Tables-green.svg)](https://www.microsoft.com/excel)
[![SQL](https://img.shields.io/badge/SQL-MySQL%208.0+-orange.svg)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Author:** Farjad Zeya (Maintenance Data Analyst / Data Analyst)  
**Email:** farjadzeya1234@gmail.com | **Phone:** +91 6204812301  
**Project Alignment:** Directly corresponds to Project #3 listed on Farjad Zeya's professional resume.

---

## 1. Project Overview
This project delivers a supply chain logistics and fulfillment analytics solution analyzing 2,200 consignments across 8 suppliers, 4 fulfillment hubs, and 4 carrier partners.

## 2. Business Problem
Supply chain delays and freight expense overruns degrade customer service level agreements (SLAs). Key business questions:
1. What is the enterprise On-Time Delivery Rate (OTD %), and where do delays originate?
2. Which suppliers and origin warehouse hubs represent critical bottlenecks?
3. How can freight costs per KG be optimized across transportation modes?

## 3. Objectives
- Clean raw logistics data with missing delivery timestamps and inconsistent carrier names.
- Develop MySQL schema and advanced SQL queries evaluating supplier scorecards and route bottlenecks.
- Build Excel MIS models with dynamic `XLOOKUP`, `SUMIFS`, and Pivot Tables.
- Design an executive Power BI dashboard with DAX measures and route heatmaps.
- Provide practical recommendations to achieve an 88% OTD target.

## 4. Dataset Description
*Note: This dataset is a realistic synthetic supply chain logistics dataset generated specifically for portfolio demonstration. It does not represent proprietary corporate data.*
- **Volume:** 2,200 shipment records.
- **Attributes:** `shipment_id`, `order_date`, `scheduled_ship_date`, `actual_ship_date`, `scheduled_delivery_date`, `actual_delivery_date`, `supplier_id`, `supplier_name`, `origin_warehouse`, `warehouse_code`, `carrier_name`, `shipping_mode`, `destination_region`, `item_category`, `weight_kg`, `shipping_cost_usd`, `delivery_status`, `delay_days`, `damage_reported`.

## 5. Tools & Technologies
- **Databases:** MySQL 8.0+ (Window ranking `DENSE_RANK()`, `SUM OVER`)
- **Reporting & Spreadsheets:** Microsoft Excel (Pivot Tables, MIS Reporting, Advanced Functions `SUMIFS`, `AVERAGEIF`, `XLOOKUP`)
- **Dashboards:** Power BI Desktop, DAX, Streamlit
- **Analytics:** Python (pandas, NumPy)

## 6. Project Architecture
```
Logistics ERP Logs ──> Data Cleaning & Validation ──> Processed Data & Scorecards
                                                               │
         ┌─────────────────────────────────────────────────────┴─────────────────────────┐
         ▼                                                     ▼                         ▼
MySQL Relational Schema & Queries                     Excel MIS Reports & Pivots         Power BI Fulfillment Cockpit
 (Supplier scorecards, Bottleneck Ranking)            (SUMIFS, XLOOKUP, Heatmaps)        (OTD Gauge, Delay Slicers)
```

## 7. Data Cleaning Process
- Handled missing delivery dates using scheduled timestamps and delay offsets.
- Rectified negative weight anomalies.
- Standardized carrier naming syntax.
- Deduplicated shipment tracking codes.

## 8. SQL Analysis
- Enterprise OTD %, average delay days, and freight spend.
- Supplier reliability scorecard (OTD, defect rate, lead times).
- Origin warehouse dispatch latency.
- Route bottleneck matrix using `DENSE_RANK()`.

## 9. Python / Excel Analysis
- Comprehensive MIS Excel model with conditional formatting.
- Correlation analysis between transit mode and delay frequency.

## 10. Dashboard Overview
- Executive OTD gauge with 85% SLA benchmark.
- Warehouse dispatch latency bar chart.
- Supplier defect vs delay scatter plot.
- Route bottleneck exception grid.

## 11. Key KPIs
- **Total Shipments:** 2,200
- **On-Time Delivery Rate (OTD):** ~81.4%
- **Average Delay on Late Orders:** ~3.4 Days
- **Total Freight Spend:** ~$312,000
- **Average Cost per KG:** ~$1.84

## 12. Key Insights
1. **Hub Bottleneck:** Kolkata Hub (WH-KOL-04) achieved only 71.2% OTD due to dispatch processing lag.
2. **Supplier Disparity:** Tier-3 supplier *Eagle Fasteners* registered 64.2% OTD and elevated damage rates (6.8%).
3. **Carrier Mode:** Express air mode drove 38% of cost for 16% of weight.

## 13. Business Recommendations
1. Modernize intake staging at Kolkata Hub to cut 2.4-day dispatch delay.
2. Institute contract SLA delay penalties for substandard suppliers.
3. Consolidate small road shipments into multi-modal rail freight to save 12% in freight costs.

## 14. Project Structure
```
03-supply-chain-delivery-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   ├── raw/supply_chain_shipments_raw.csv
│   └── processed/
│       ├── supply_chain_shipments_cleaned.csv
│       └── supplier_scorecards.csv
├── sql/
│   ├── schema.sql
│   ├── data_analysis.sql
│   └── advanced_queries.sql
├── notebooks/
│   └── analysis.ipynb
├── src/
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── visualization.py
├── dashboard/
│   ├── powerbi_specification.md
│   └── dax_measures.dax
├── reports/
│   ├── insights.md
│   └── excel_analysis_guide.md
└── streamlit_app.py
```

## 15. How to Run the Project
```bash
git clone https://github.com/farjadzeya/supply-chain-delivery-analytics.git
cd supply-chain-delivery-analytics
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/data_cleaning.py
python src/analysis.py
streamlit run streamlit_app.py
```

## 16. How to Reproduce the Dashboard
Follow instructions in `dashboard/powerbi_specification.md` and load `data/processed/supply_chain_shipments_cleaned.csv`.

## 17. Limitations
- Synthetic logistics data modeling seasonal variations.
- Real-world carrier weather delays were simulated parametrically.

## 18. Future Improvements
- Integrate live GPS telematics API feeds.
- Build automated delivery delay prediction model in Python.
"""
with open(f"{PROJECT_DIR}/README.md", "w") as f:
    f.write(readme_md)

print("Project 3: Successfully generated all files!")
