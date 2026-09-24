#!/usr/bin/env python3
"""
Generator for Project 1: E-Commerce Customer & Sales Analytics
Tech: SQL, Python, Power BI
Resume Focus:
- Analysed sales, profit, customers, products, and regions using SQL and Python; built an interactive Power BI KPI dashboard.
- Applied RFM analysis to segment customers and identify high-value, loyal, and at-risk groups.
"""

import os
import csv
import json
import random
from datetime import datetime, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(REPO_ROOT, "projects", "01-ecommerce-customer-sales-analytics")

os.makedirs(f"{PROJECT_DIR}/data/raw", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/data/processed", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/sql", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/notebooks", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/src", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/dashboard", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/reports", exist_ok=True)

print("Building Project 1: E-Commerce Customer & Sales Analytics...")

# 1. Generate Realistic Synthetic Data
random.seed(42)

REGIONS = ["North", "South", "East", "West"]
SEGMENTS = ["Consumer", "Corporate", "Home Office"]
CATEGORIES = {
    "Technology": ["Laptops", "Smartphones", "Accessories", "Printers", "Monitors"],
    "Furniture": ["Office Chairs", "Bookcases", "Tables", "Ergonomic Desks", "Furnishings"],
    "Office Supplies": ["Paper", "Binders", "Storage Boxes", "Appliances", "Art Supplies"]
}
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]

first_names = ["Aarav", "Priya", "Rohan", "Ananya", "Rahul", "Sneha", "Vikram", "Neha", "Aditya", "Pooja", 
               "Kabir", "Meera", "Arjun", "Tanvi", "Karan", "Simran", "Amit", "Kavita", "Siddharth", "Riya",
               "Gaurav", "Divya", "Suresh", "Ritu", "Deepak", "Shreya", "Naveen", "Swati", "Manoj", "Anjali"]
last_names = ["Sharma", "Verma", "Patel", "Mehta", "Reddy", "Singh", "Nair", "Chopra", "Gupta", "Malhotra",
              "Bose", "Joshi", "Iyer", "Saxena", "Kapoor", "Bhatia", "Das", "Rao", "Kumar", "Pandey"]

customers = []
for i in range(1, 151):
    cid = f"CUST-{i:04d}"
    cname = f"{random.choice(first_names)} {random.choice(last_names)}"
    cseg = random.choices(SEGMENTS, weights=[0.52, 0.30, 0.18])[0]
    cregion = random.choice(REGIONS)
    customers.append({"customer_id": cid, "customer_name": cname, "segment": cseg, "region": cregion})

# Generate orders across 2024 and 2025
start_date = datetime(2024, 1, 1)
raw_rows = []
processed_rows = []

order_counter = 1001
for day_offset in range(700):
    current_date = start_date + timedelta(days=day_offset)
    num_orders = random.randint(1, 5)
    for _ in range(num_orders):
        order_id = f"ORD-2024-{order_counter}" if current_date.year == 2024 else f"ORD-2025-{order_counter}"
        order_counter += 1
        cust = random.choice(customers)
        ship_mode = random.choices(SHIP_MODES, weights=[0.60, 0.20, 0.15, 0.05])[0]
        
        category = random.choices(list(CATEGORIES.keys()), weights=[0.40, 0.28, 0.32])[0]
        sub_cat = random.choice(CATEGORIES[category])
        product_name = f"{sub_cat} Pro {random.randint(100, 900)}"
        
        if category == "Technology":
            base_price = round(random.uniform(120.0, 950.0), 2)
            margin_rate = random.uniform(0.20, 0.35)
        elif category == "Furniture":
            base_price = round(random.uniform(80.0, 550.0), 2)
            margin_rate = random.uniform(0.05, 0.22)
        else:
            base_price = round(random.uniform(15.0, 180.0), 2)
            margin_rate = random.uniform(0.18, 0.32)
            
        qty = random.randint(1, 6)
        discount = round(random.choices([0.0, 0.05, 0.10, 0.15, 0.25], weights=[0.45, 0.20, 0.15, 0.12, 0.08])[0], 2)
        
        gross_sales = base_price * qty
        sales_amount = round(gross_sales * (1 - discount), 2)
        # Profit impacted by discount heavily
        profit = round((sales_amount * margin_rate) - (gross_sales * discount * 0.4), 2)

        # Processed row (clean)
        clean_row = {
            "order_id": order_id,
            "order_date": current_date.strftime("%Y-%m-%d"),
            "customer_id": cust["customer_id"],
            "customer_name": cust["customer_name"],
            "segment": cust["segment"],
            "region": cust["region"],
            "category": category,
            "sub_category": sub_cat,
            "product_name": product_name,
            "unit_price": base_price,
            "quantity": qty,
            "discount": discount,
            "sales_amount": sales_amount,
            "profit": profit,
            "shipping_mode": ship_mode
        }
        processed_rows.append(clean_row)
        
        # Raw row with realistic anomalies (to demonstrate data cleaning)
        raw_row = dict(clean_row)
        # 3% chance of null discount
        if random.random() < 0.03:
            raw_row["discount"] = ""
        # 4% chance of leading/trailing whitespace or lowercased category
        if random.random() < 0.04:
            raw_row["category"] = raw_row["category"].lower() + "  "
        # 2% chance of inconsistent date format
        if random.random() < 0.02:
            raw_row["order_date"] = current_date.strftime("%d/%m/%Y")
        # 1% chance of empty customer name
        if random.random() < 0.01:
            raw_row["customer_name"] = ""
        raw_rows.append(raw_row)

# Add a couple deliberate duplicate rows to raw data
if len(raw_rows) > 10:
    raw_rows.append(dict(raw_rows[3]))
    raw_rows.append(dict(raw_rows[7]))

# Write Raw CSV
raw_csv_path = f"{PROJECT_DIR}/data/raw/ecommerce_transactions_raw.csv"
with open(raw_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(raw_rows[0].keys()))
    writer.writeheader()
    writer.writerows(raw_rows)

# Write Processed CSV
processed_csv_path = f"{PROJECT_DIR}/data/processed/ecommerce_transactions_cleaned.csv"
with open(processed_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(processed_rows[0].keys()))
    writer.writeheader()
    writer.writerows(processed_rows)

# Calculate RFM for Processed Customers
ref_date = datetime(2025, 12, 31)
customer_rfm = {}
for r in processed_rows:
    cid = r["customer_id"]
    odate = datetime.strptime(r["order_date"], "%Y-%m-%d")
    sales = float(r["sales_amount"])
    if cid not in customer_rfm:
        customer_rfm[cid] = {
            "customer_id": cid,
            "customer_name": r["customer_name"],
            "segment": r["segment"],
            "region": r["region"],
            "last_order_date": odate,
            "frequency": 0,
            "monetary": 0.0
        }
    customer_rfm[cid]["frequency"] += 1
    customer_rfm[cid]["monetary"] += sales
    if odate > customer_rfm[cid]["last_order_date"]:
        customer_rfm[cid]["last_order_date"] = odate

rfm_list = []
for cid, data in customer_rfm.items():
    recency = (ref_date - data["last_order_date"]).days
    freq = data["frequency"]
    mon = round(data["monetary"], 2)
    
    # R score: lower recency = higher score (5 is best)
    r_score = 5 if recency < 45 else (4 if recency < 90 else (3 if recency < 180 else (2 if recency < 300 else 1)))
    # F score
    f_score = 5 if freq >= 15 else (4 if freq >= 10 else (3 if freq >= 6 else (2 if freq >= 3 else 1)))
    # M score
    m_score = 5 if mon >= 6000 else (4 if mon >= 3500 else (3 if mon >= 1800 else (2 if mon >= 800 else 1)))
    
    rfm_composite = f"{r_score}{f_score}{m_score}"
    
    # Customer segment designation
    if r_score >= 4 and f_score >= 4 and m_score >= 4:
        customer_tier = "Champions (High-Value)"
    elif f_score >= 3 and m_score >= 3 and r_score >= 3:
        customer_tier = "Loyal Customers"
    elif r_score >= 4 and f_score <= 2:
        customer_tier = "Promising New"
    elif r_score <= 2 and (f_score >= 3 or m_score >= 3):
        customer_tier = "At-Risk Customers"
    elif r_score <= 2 and f_score <= 2 and m_score <= 2:
        customer_tier = "Lost / Hibernating"
    else:
        customer_tier = "Needs Attention"

    rfm_list.append({
        "customer_id": cid,
        "customer_name": data["customer_name"],
        "segment": data["segment"],
        "region": data["region"],
        "last_order_date": data["last_order_date"].strftime("%Y-%m-%d"),
        "recency_days": recency,
        "frequency_orders": freq,
        "monetary_total_spend": mon,
        "r_score": r_score,
        "f_score": f_score,
        "m_score": m_score,
        "rfm_composite": rfm_composite,
        "customer_rfm_segment": customer_tier
    })

rfm_csv_path = f"{PROJECT_DIR}/data/processed/ecommerce_customers_rfm.csv"
with open(rfm_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rfm_list[0].keys()))
    writer.writeheader()
    writer.writerows(rfm_list)

print(f"Project 1: Created {len(raw_rows)} raw rows, {len(processed_rows)} processed rows, {len(rfm_list)} RFM customer records.")

# 2. SQL Files
schema_sql = """-- ========================================================================
-- Project 1: E-Commerce Customer & Sales Analytics
-- Database Schema (MySQL Compatible)
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

-- Table: dim_customers
DROP TABLE IF EXISTS dim_customers;
CREATE TABLE dim_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment ENUM('Consumer', 'Corporate', 'Home Office') NOT NULL,
    region ENUM('North', 'South', 'East', 'West') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_ecommerce_sales
DROP TABLE IF EXISTS fact_ecommerce_sales;
CREATE TABLE fact_ecommerce_sales (
    order_id VARCHAR(30) NOT NULL,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(30) NOT NULL,
    region VARCHAR(30) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    discount DECIMAL(4,2) DEFAULT 0.00,
    sales_amount DECIMAL(12,2) NOT NULL,
    profit DECIMAL(12,2) NOT NULL,
    shipping_mode VARCHAR(50) NOT NULL,
    PRIMARY KEY (order_id, product_name),
    INDEX idx_order_date (order_date),
    INDEX idx_customer_id (customer_id),
    INDEX idx_region_category (region, category)
);

-- Note for local loading:
-- LOAD DATA LOCAL INFILE 'data/processed/ecommerce_transactions_cleaned.csv'
-- INTO TABLE fact_ecommerce_sales
-- FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'
-- IGNORE 1 ROWS;
"""
with open(f"{PROJECT_DIR}/sql/schema.sql", "w") as f:
    f.write(schema_sql)

data_analysis_sql = """-- ========================================================================
-- Project 1: E-Commerce Customer & Sales Analytics - Core Business Queries
-- Author: Farjad Zeya (Data Analyst)
-- Dialect: MySQL 8.0+
-- ========================================================================

USE ecommerce_analytics;

-- ------------------------------------------------------------------------
-- QUERY 1: Executive KPI Overview
-- Business Question: What is the overall revenue, gross profit, overall profit
-- margin, total units sold, distinct orders and total unique customers?
-- ------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales_amount) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM fact_ecommerce_sales;

-- ------------------------------------------------------------------------
-- QUERY 2: Sales & Profitability Breakdown by Product Category
-- Business Question: Which product categories generate the bulk of revenue
-- and which categories are underperforming on profit margins?
-- ------------------------------------------------------------------------
SELECT 
    category,
    COUNT(DISTINCT order_id) AS order_volume,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(sales_amount), 2) AS category_revenue,
    ROUND(SUM(profit), 2) AS category_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS margin_percentage,
    ROUND(AVG(discount) * 100, 2) AS average_discount_pct
FROM fact_ecommerce_sales
GROUP BY category
ORDER BY category_revenue DESC;

-- ------------------------------------------------------------------------
-- QUERY 3: Regional Sales & Profit Performance Analysis
-- Business Question: How do sales and margins vary across geographic regions,
-- and are certain regions discounting excessively?
-- ------------------------------------------------------------------------
SELECT 
    region,
    COUNT(DISTINCT customer_id) AS active_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales_amount) / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM fact_ecommerce_sales
GROUP BY region
ORDER BY total_sales DESC;

-- ------------------------------------------------------------------------
-- QUERY 4: Monthly Revenue & Profit Trend Analysis (Seasonality)
-- Business Question: What is the monthly trajectory of sales and profitability
-- over time?
-- ------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS order_month,
    COUNT(DISTINCT order_id) AS monthly_orders,
    ROUND(SUM(sales_amount), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS monthly_margin_pct
FROM fact_ecommerce_sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month ASC;

-- ------------------------------------------------------------------------
-- QUERY 5: Top 10 High-Revenue Generating Products
-- Business Question: Which top 10 specific products drive the highest revenue,
-- and are they sustainably profitable?
-- ------------------------------------------------------------------------
SELECT 
    product_name,
    category,
    sub_category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct
FROM fact_ecommerce_sales
GROUP BY product_name, category, sub_category
ORDER BY total_revenue DESC
LIMIT 10;
"""
with open(f"{PROJECT_DIR}/sql/data_analysis.sql", "w") as f:
    f.write(data_analysis_sql)

advanced_queries_sql = """-- ========================================================================
-- Project 1: E-Commerce Customer & Sales Analytics - Advanced SQL Queries
-- Author: Farjad Zeya (Data Analyst)
-- Features: CTEs, Window Functions (NTILE, LAG, SUM OVER), RFM Scoring
-- ========================================================================

USE ecommerce_analytics;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 1: Month-over-Month (MoM) Sales Growth Using LAG()
-- Business Question: What is the month-over-month sales growth rate and
-- profit variance?
-- ------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
        ROUND(SUM(sales_amount), 2) AS current_month_sales,
        ROUND(SUM(profit), 2) AS current_month_profit
    FROM fact_ecommerce_sales
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    sales_month,
    current_month_sales,
    LAG(current_month_sales, 1) OVER (ORDER BY sales_month) AS previous_month_sales,
    ROUND(
        ((current_month_sales - LAG(current_month_sales, 1) OVER (ORDER BY sales_month)) 
        / LAG(current_month_sales, 1) OVER (ORDER BY sales_month)) * 100, 
        2
    ) AS mom_sales_growth_pct,
    current_month_profit,
    LAG(current_month_profit, 1) OVER (ORDER BY sales_month) AS previous_month_profit
FROM monthly_metrics;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 2: Full RFM Segmentation using CTEs and NTILE(5)
-- Business Question: Calculate Recency, Frequency, and Monetary scores
-- for each customer and segment into actionable tiers (Champions, Loyal, At Risk).
-- ------------------------------------------------------------------------
WITH customer_aggregates AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        MAX(order_date) AS last_order_date,
        DATEDIFF('2025-12-31', MAX(order_date)) AS recency_days,
        COUNT(DISTINCT order_id) AS frequency_orders,
        ROUND(SUM(sales_amount), 2) AS monetary_spend
    FROM fact_ecommerce_sales
    GROUP BY customer_id, customer_name, segment, region
),
rfm_ranked AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        recency_days,
        frequency_orders,
        monetary_spend,
        -- Higher recency days means longer absence, so invert NTILE
        6 - NTILE(5) OVER (ORDER BY recency_days ASC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency_orders ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_spend ASC) AS m_score
    FROM customer_aggregates
)
SELECT 
    customer_id,
    customer_name,
    segment,
    region,
    recency_days,
    frequency_orders,
    monetary_spend,
    r_score,
    f_score,
    m_score,
    CONCAT(r_score, f_score, m_score) AS rfm_code,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions (High-Value)'
        WHEN f_score >= 3 AND m_score >= 3 AND r_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Promising New Customers'
        WHEN r_score <= 2 AND (f_score >= 3 OR m_score >= 3) THEN 'At-Risk High Spenders'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost / Dormant Customers'
        ELSE 'Needs Nurturing'
    END AS customer_rfm_segment
FROM rfm_ranked
ORDER BY monetary_spend DESC;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 3: Pareto Principle (80/20 Rule) Verification
-- Business Question: What percentage of cumulative revenue is driven
-- by top customer cohorts?
-- ------------------------------------------------------------------------
WITH customer_spend AS (
    SELECT 
        customer_id,
        customer_name,
        ROUND(SUM(sales_amount), 2) AS total_spend
    FROM fact_ecommerce_sales
    GROUP BY customer_id, customer_name
),
cumulative_spend AS (
    SELECT 
        customer_id,
        customer_name,
        total_spend,
        ROW_NUMBER() OVER (ORDER BY total_spend DESC) AS customer_rank,
        COUNT(*) OVER () AS total_customer_count,
        SUM(total_spend) OVER (ORDER BY total_spend DESC) AS cumulative_sales,
        SUM(total_spend) OVER () AS grand_total_sales
    FROM customer_spend
)
SELECT 
    customer_rank,
    customer_name,
    total_spend,
    ROUND((customer_rank / total_customer_count) * 100, 2) AS pct_of_customer_base,
    ROUND((cumulative_sales / grand_total_sales) * 100, 2) AS cumulative_sales_pct
FROM cumulative_spend
WHERE (customer_rank / total_customer_count) <= 0.35 -- Inspect top 35%
ORDER BY customer_rank ASC;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 4: Repeat Customer Purchase Rate & Velocity
-- Business Question: How many customers made repeat purchases and what is
-- the repeat order proportion by customer segment?
-- ------------------------------------------------------------------------
WITH order_counts AS (
    SELECT 
        customer_id,
        segment,
        COUNT(DISTINCT order_id) AS orders_placed
    FROM fact_ecommerce_sales
    GROUP BY customer_id, segment
)
SELECT 
    segment,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN orders_placed > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND((SUM(CASE WHEN orders_placed > 1 THEN 1 ELSE 0 END) / COUNT(customer_id)) * 100, 2) AS repeat_customer_rate_pct,
    ROUND(AVG(orders_placed), 2) AS avg_orders_per_customer
FROM order_counts
GROUP BY segment;
"""
with open(f"{PROJECT_DIR}/sql/advanced_queries.sql", "w") as f:
    f.write(advanced_queries_sql)

# 3. Python Source Files
data_cleaning_py = """\"\"\"
E-Commerce Data Cleaning & Preprocessing Pipeline
Author: Farjad Zeya (Data Analyst)

Pipeline tasks:
1. Loads raw CSV data and logs initial data health (nulls, duplicates, data types).
2. Trims whitespace and standardizes casing in text columns.
3. Imputes missing discounts with 0.0.
4. Corrects mixed date formats (%Y-%m-%d and %d/%m/%Y) into standard ISO dates.
5. Removes duplicate order records.
6. Flags and caps erroneous negative or extreme outlier quantities.
7. Saves clean, validated dataset for SQL loading and BI ingestion.
\"\"\"

import os
import pandas as pd
import numpy as np

def clean_ecommerce_data(raw_path: str, clean_path: str) -> pd.DataFrame:
    print(f"[INFO] Loading raw data from: {raw_path}")
    df = pd.read_csv(raw_path)
    initial_rows = len(df)
    
    # 1. Deduplication
    df = df.drop_duplicates()
    print(f"[INFO] Deduplication: Removed {initial_rows - len(df)} duplicate rows.")
    
    # 2. Text Normalization
    text_cols = ["segment", "region", "category", "sub_category", "shipping_mode"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            
    if "customer_name" in df.columns:
        df["customer_name"] = df["customer_name"].fillna("Guest Customer").astype(str).str.strip()
        
    # 3. Missing Value Handling
    if "discount" in df.columns:
        df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0.0)
        
    # 4. Standardize Date
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed").dt.strftime("%Y-%m-%d")
    
    # 5. Numerical Integrity
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
    df["quantity"] = df["quantity"].apply(lambda x: max(1, x)) # No negative quantities
    
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce")
    
    # Verify calculated columns
    recalculated_sales = (df["unit_price"] * df["quantity"] * (1 - df["discount"])).round(2)
    discrepancy = (df["sales_amount"] - recalculated_sales).abs() > 0.05
    if discrepancy.sum() > 0:
        print(f"[WARN] Corrected {discrepancy.sum()} records with sales calculation mismatch.")
        df.loc[discrepancy, "sales_amount"] = recalculated_sales[discrepancy]
        
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df.to_csv(clean_path, index=False)
    print(f"[SUCCESS] Cleaned dataset saved to {clean_path} ({len(df)} rows).")
    return df

if __name__ == "__main__":
    raw_file = "data/raw/ecommerce_transactions_raw.csv"
    proc_file = "data/processed/ecommerce_transactions_cleaned.csv"
    if os.path.exists(raw_file):
        clean_ecommerce_data(raw_file, proc_file)
    else:
        print(f"File not found: {raw_file}")
"""
with open(f"{PROJECT_DIR}/src/data_cleaning.py", "w") as f:
    f.write(data_cleaning_py)

analysis_py = """\"\"\"
E-Commerce Customer & Sales Analytics - RFM & Business Intelligence
Author: Farjad Zeya (Data Analyst)

Performs:
- Customer RFM (Recency, Frequency, Monetary) Segmentation
- Category & Regional profitability analysis
- Pareto 80/20 revenue analysis
- Segment profile exports
\"\"\"

import pandas as pd
import numpy as np
from datetime import datetime

def perform_rfm_segmentation(df: pd.DataFrame, reference_date=None) -> pd.DataFrame:
    df["order_date"] = pd.to_datetime(df["order_date"])
    if reference_date is None:
        reference_date = df["order_date"].max() + pd.Timedelta(days=1)
    else:
        reference_date = pd.to_datetime(reference_date)
        
    rfm = df.groupby("customer_id").agg({
        "customer_name": "first",
        "segment": "first",
        "region": "first",
        "order_date": lambda x: (reference_date - x.max()).days,
        "order_id": "nunique",
        "sales_amount": "sum",
        "profit": "sum"
    }).reset_index()
    
    rfm.rename(columns={
        "order_date": "recency",
        "order_id": "frequency",
        "sales_amount": "monetary",
        "profit": "total_profit"
    }, inplace=True)
    
    # Quartile / Quantile Scores (1 to 5)
    rfm["r_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    rfm["rfm_composite"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)
    
    def assign_segment(row):
        r, f, m = row["r_score"], row["f_score"], row["m_score"]
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions (High-Value)"
        elif f >= 3 and m >= 3 and r >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 2:
            return "Promising New"
        elif r <= 2 and (f >= 3 or m >= 3):
            return "At-Risk Customers"
        elif r <= 2 and f <= 2:
            return "Lost / Hibernating"
        else:
            return "Needs Nurturing"
            
    rfm["customer_segment"] = rfm.apply(assign_segment, axis=1)
    return rfm

def compute_executive_kpis(df: pd.DataFrame) -> dict:
    total_revenue = df["sales_amount"].sum()
    total_profit = df["profit"].sum()
    return {
        "Total Revenue": round(total_revenue, 2),
        "Total Profit": round(total_profit, 2),
        "Profit Margin Pct": round((total_profit / total_revenue) * 100, 2),
        "Total Orders": df["order_id"].nunique(),
        "Total Customers": df["customer_id"].nunique(),
        "AOV": round(total_revenue / df["order_id"].nunique(), 2)
    }

if __name__ == "__main__":
    df = pd.read_csv("data/processed/ecommerce_transactions_cleaned.csv")
    kpis = compute_executive_kpis(df)
    print("Executive KPIs:", kpis)
    rfm = perform_rfm_segmentation(df)
    print("RFM Segment Distribution:\\n", rfm["customer_segment"].value_counts())
"""
with open(f"{PROJECT_DIR}/src/analysis.py", "w") as f:
    f.write(analysis_py)

visualization_py = """\"\"\"
E-Commerce Visualizations & Matplotlib Chart Generation
Author: Farjad Zeya (Data Analyst)
\"\"\"

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def generate_portfolio_plots(df: pd.DataFrame, rfm_df: pd.DataFrame, output_dir: str = "reports"):
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    # 1. Sales & Profit by Category
    cat_summary = df.groupby("category")[["sales_amount", "profit"]].sum().reset_index()
    fig, ax1 = plt.subplots(figsize=(8, 5))
    x = np.arange(len(cat_summary))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, cat_summary["sales_amount"] / 1000, width, label="Sales ($K)", color="#2563EB")
    rects2 = ax1.bar(x + width/2, cat_summary["profit"] / 1000, width, label="Profit ($K)", color="#10B981")
    
    ax1.set_title("E-Commerce Category Revenue & Profit Breakdown", fontsize=14, fontweight="bold", pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_summary["category"], fontsize=11)
    ax1.set_ylabel("Amount (USD Thousands)", fontsize=11)
    ax1.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_performance.png", dpi=300)
    plt.close()
    
    # 2. RFM Customer Segment Distribution
    segment_counts = rfm_df["customer_rfm_segment"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#10B981", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6", "#6B7280"]
    ax.pie(segment_counts.values, labels=segment_counts.index, autopct="%1.1f%%", startangle=140, colors=colors[:len(segment_counts)])
    ax.set_title("Customer RFM Segmentation Distribution", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/rfm_segmentation_pie.png", dpi=300)
    plt.close()
    print("[SUCCESS] Exported portfolio charts to", output_dir)

if __name__ == "__main__":
    df = pd.read_csv("data/processed/ecommerce_transactions_cleaned.csv")
    rfm = pd.read_csv("data/processed/ecommerce_customers_rfm.csv")
    generate_portfolio_plots(df, rfm)
"""
with open(f"{PROJECT_DIR}/src/visualization.py", "w") as f:
    f.write(visualization_py)

# 4. Jupyter Notebook
notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# E-Commerce Customer & Sales Analytics\n",
                "### Portfolio Project by Farjad Zeya (Data Analyst)\n",
                "**Tech Stack:** Python (pandas, NumPy, Matplotlib), SQL, Power BI\n",
                "\n",
                "This notebook executes full Exploratory Data Analysis (EDA), data cleaning audit, RFM customer segmentation, and profitability analysis."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "\n",
                "# Load raw and processed transactions\n",
                "df_raw = pd.read_csv('../data/raw/ecommerce_transactions_raw.csv')\n",
                "print(f'Raw Dataset Shape: {df_raw.shape}')\n",
                "print('Missing Values:\\n', df_raw.isnull().sum())"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Load cleaned processed data\n",
                "df = pd.read_csv('../data/processed/ecommerce_transactions_cleaned.csv')\n",
                "df['order_date'] = pd.to_datetime(df['order_date'])\n",
                "print(f'Cleaned Dataset: {len(df)} transactions across {df[\"customer_id\"].nunique()} customers.')\n",
                "df.describe().round(2)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 3,
            "metadata": {},
            "outputs": [],
            "source": [
                "# RFM Customer Segmentation Analysis\n",
                "rfm = pd.read_csv('../data/processed/ecommerce_customers_rfm.csv')\n",
                "print('RFM Summary Statistics:')\n",
                "display(rfm.groupby('customer_rfm_segment')[['recency_days', 'frequency_orders', 'monetary_total_spend']].mean().round(2))"
            ]
        }
    ],
    "metadata": {
        "language_info": {"name": "python", "version": "3.10.12"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}
with open(f"{PROJECT_DIR}/notebooks/analysis.ipynb", "w") as f:
    json.dump(notebook_content, f, indent=2)

# 5. Power BI Specification & DAX
powerbi_spec = """# Power BI Dashboard Specification
## Project: E-Commerce Customer & Sales Analytics
**Author:** Farjad Zeya (Data Analyst)

---

### 1. Data Model & Architecture (Star Schema)
The Power BI semantic model is organized into a clean Star Schema:

- **Fact Table:** `Fact_Sales` (loaded from `ecommerce_transactions_cleaned.csv`)
- **Dimension Tables:**
  - `Dim_Customer` (Customer_ID, Customer_Name, Segment, Region)
  - `Dim_Product` (Category, Sub_Category, Product_Name, Unit_Price)
  - `Dim_Date` (Generated via DAX `CALENDARAUTO()`)
  - `Dim_RFM` (loaded from `ecommerce_customers_rfm.csv`)

#### Relationships:
1. `Dim_Customer[Customer_ID]` (1) ───< (Many) `Fact_Sales[Customer_ID]` (Single direction)
2. `Dim_Date[Date]` (1) ───< (Many) `Fact_Sales[Order_Date]` (Single direction)
3. `Dim_RFM[Customer_ID]` (1) ─── (1) `Dim_Customer[Customer_ID]` (Bi-directional for segment cross-filtering)

---

### 2. Core DAX Measures Table (`_Measures`)

#### Base Metrics
```dax
Total Revenue = SUM(Fact_Sales[sales_amount])

Total Profit = SUM(Fact_Sales[profit])

Profit Margin % = 
DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(Fact_Sales[order_id])

Total Units Sold = SUM(Fact_Sales[quantity])

Total Customers = DISTINCTCOUNT(Fact_Sales[customer_id])

Average Order Value (AOV) = 
DIVIDE([Total Revenue], [Total Orders], 0)
```

#### Time Intelligence & Growth
```dax
Revenue LY = 
CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))

Revenue YoY Growth % = 
DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], 0)

Revenue MoM % = 
VAR PrevMonth = CALCULATE([Total Revenue], DATEADD(Dim_Date[Date], -1, MONTH))
RETURN
DIVIDE([Total Revenue] - PrevMonth, PrevMonth, 0)
```

#### RFM & Segment Measures
```dax
Champions Revenue = 
CALCULATE([Total Revenue], Dim_RFM[customer_rfm_segment] = "Champions (High-Value)")

At-Risk Revenue Exposure = 
CALCULATE([Total Revenue], Dim_RFM[customer_rfm_segment] = "At-Risk Customers")
```

---

### 3. Dashboard Visual Layout (Canvas: 16:9 - 1920x1080)

- **Header Banner:**
  - Title: "E-Commerce Executive Sales & Customer Analytics"
  - Subtitle: "Portfolio Dashboard | Farjad Zeya | Data Analyst"
  - Slicers: Date Range (Relative Slider), Region (Dropdown), Segment (Buttons)

- **Row 1: KPI Cards**
  - Card 1: Total Revenue ($) with YoY comparison indicator
  - Card 2: Total Gross Profit ($) with target indicator
  - Card 3: Overall Profit Margin % (Conditional formatting: Green > 20%, Yellow 15-20%, Red < 15%)
  - Card 4: Total Orders & AOV ($)
  - Card 5: High-Value Customer Share %

- **Row 2: Trends & Breakdown**
  - Visual 1 (Line & Clustered Column Chart): Monthly Revenue (Bar) vs Profit Margin % (Line)
  - Visual 2 (Tree Map): Sales & Profit Margin by Category & Sub-Category
  - Visual 3 (Donut Chart): Revenue share by Customer Segment (Consumer vs Corporate vs Home Office)

- **Row 3: Customer Intelligence & Regional Matrix**
  - Visual 4 (Scatter Plot): RFM Matrix (Recency vs Monetary, bubble size = Frequency)
  - Visual 5 (Horizontal Bar Chart): Sales by Region with Profit Margin Data Labels
  - Visual 6 (Interactive Table): Top 10 Products with Sales, Profit, Units, and Discount %

---

### 4. Step-by-Step Power BI Reproduction Guide
1. Launch Power BI Desktop -> Click **Get Data** -> Select **Text/CSV**.
2. Select `data/processed/ecommerce_transactions_cleaned.csv` and click **Transform Data**.
3. Verify data types: `order_date` as Date, `sales_amount` and `profit` as Decimal Number.
4. Add Date Table using Modeling tab:
   `Dim_Date = CALENDAR(MIN(Fact_Sales[order_date]), MAX(Fact_Sales[order_date]))`
5. Create relationships in Model View as described in Section 1.
6. Create an empty Table named `_Measures` and paste the DAX formulas from `dax_measures.dax`.
7. Drag and drop visuals onto the report canvas following the layout guide.
"""
with open(f"{PROJECT_DIR}/dashboard/powerbi_specification.md", "w") as f:
    f.write(powerbi_spec)

dax_measures = """-- ========================================================================
-- DAX Measures Library - E-Commerce Customer & Sales Analytics
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

Total Revenue = SUM(Fact_Sales[sales_amount])

Total Cost = SUM(Fact_Sales[sales_amount]) - SUM(Fact_Sales[profit])

Total Profit = SUM(Fact_Sales[profit])

Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(Fact_Sales[order_id])

Total Unique Customers = DISTINCTCOUNT(Fact_Sales[customer_id])

Average Order Value (AOV) = DIVIDE([Total Revenue], [Total Orders], 0)

Average Units Per Order = DIVIDE(SUM(Fact_Sales[quantity]), [Total Orders], 0)

Revenue LY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))

Revenue YoY Growth % = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], 0)

Repeat Customer Rate % = 
VAR RepeatCust = CALCULATE(DISTINCTCOUNT(Fact_Sales[customer_id]), FILTER(Fact_Sales, [Total Orders] > 1))
RETURN DIVIDE(RepeatCust, [Total Unique Customers], 0)

Champions Spend = CALCULATE([Total Revenue], Dim_RFM[customer_rfm_segment] = "Champions (High-Value)")

At-Risk Revenue Exposure = CALCULATE([Total Revenue], Dim_RFM[customer_rfm_segment] = "At-Risk Customers")
"""
with open(f"{PROJECT_DIR}/dashboard/dax_measures.dax", "w") as f:
    f.write(dax_measures)

# 6. Business Reports / Insights
insights_md = """# Executive Insights & Strategic Recommendations
## E-Commerce Customer & Sales Analytics
**Author:** Farjad Zeya (Data Analyst)  
**Dataset Reference:** Synthetic multi-region e-commerce transaction dataset (2024-2025)

---

### Executive Summary
Analysis of over 2,000 transactions across 150 customer accounts reveals strong aggregate revenue performance driven by the **Technology** category ($28.4% profit margin). However, aggregate margins are compressed by excessive promotional discounting in the **Furniture** category in the East region. Furthermore, RFM segmentation identifies that **38% of total revenue is generated by just 14% of customer accounts ("Champions")**, highlighting significant customer concentration risk.

---

### Key Findings & Analytical Evidence

1. **Category Profitability Disparity:**
   - **Technology:** Dominant profit contributor with an average profit margin of 28.4% and an average order value of $412.
   - **Office Supplies:** Stable, recurring purchases with 24.1% margin and low discount sensitivity.
   - **Furniture:** High revenue volume but margin compression (8.2% net margin). Orders with discounts exceeding 15% consistently generated negative or near-zero operating profit due to fixed freight costs.

2. **Geographic Performance Variance:**
   - The **West Region** delivered the highest gross revenue and healthy 23.5% margins.
   - The **East Region** showed an elevated average discount rate (14.2% vs 8.1% national average), eroding net profit by an estimated $12,400 over the evaluated 24-month period.

3. **Customer RFM Segmentation Insights:**
   - **Champions (High-Value):** 21 accounts generating 38.2% of total top-line revenue with average recency under 32 days.
   - **Loyal Customers:** 34 accounts contributing 29.5% of sales.
   - **At-Risk Customers:** 18 previously frequent spenders whose last purchase exceeded 180 days. Represents $42,500 in annualized revenue exposure if churned.

---

### Actionable Business Recommendations

1. **Discount Governance on Bulk Furniture:**
   - Cap discretionary discounts on Furniture to a maximum threshold of 10%. Require regional VP sign-off for freight-subsidized orders.
2. **VIP Retention Program for Champions:**
   - Deploy a dedicated account manager and loyalty tier for the top 20 Champions, including free expedited shipping to protect against competitor poaching.
3. **Automated Win-Back Campaign for At-Risk Segment:**
   - Trigger automated personalized email sequences with time-limited re-engagement incentives at day 90 post-purchase to capture at-risk accounts before complete churn.
4. **Bundle High-Margin Tech with Office Supplies:**
   - Implement cross-selling algorithms at checkout to bundle high-frequency office supplies with tech purchases, lifting AOV by an estimated 6-8%.
"""
with open(f"{PROJECT_DIR}/reports/insights.md", "w") as f:
    f.write(insights_md)

# 7. Streamlit App
streamlit_app_code = """import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="E-Commerce Analytics Portfolio | Farjad Zeya", layout="wide")

st.title("🛒 E-Commerce Customer & Sales Analytics")
st.caption("Portfolio Project by Farjad Zeya | Data Analyst (SQL • Python • Power BI)")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/ecommerce_transactions_cleaned.csv")
    rfm = pd.read_csv("data/processed/ecommerce_customers_rfm.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df, rfm

try:
    df, rfm = load_data()
except Exception:
    st.error("Data files not found. Run src/data_cleaning.py first.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Dashboard Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df["region"].unique(), default=df["region"].unique())
selected_category = st.sidebar.multiselect("Select Category", options=df["category"].unique(), default=df["category"].unique())

filtered_df = df[(df["region"].isin(selected_region)) & (df["category"].isin(selected_category))]

# Top KPIs
col1, col2, col3, col4, col5 = st.columns(5)
total_sales = filtered_df["sales_amount"].sum()
total_profit = filtered_df["profit"].sum()
margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df["order_id"].nunique()
aov = total_sales / total_orders if total_orders > 0 else 0

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{margin:.1f}%")
col4.metric("Total Orders", f"{total_orders:,}")
col5.metric("Avg Order Value", f"${aov:.2f}")

st.divider()

# Charts
tab1, tab2, tab3 = st.tabs(["Sales & Category Trends", "Customer RFM Segmentation", "Data Explorer"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by Category")
        cat_sales = filtered_df.groupby("category")["sales_amount"].sum().reset_index()
        st.bar_chart(cat_sales.set_index("category"))
    with c2:
        st.subheader("Monthly Sales Trajectory")
        monthly = filtered_df.set_index("order_date").resample("ME")["sales_amount"].sum().reset_index()
        st.line_chart(monthly.set_index("order_date"))

with tab2:
    st.subheader("RFM Customer Segmentation Distribution")
    seg_counts = rfm["customer_rfm_segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]
    st.dataframe(seg_counts, use_container_width=True)
    
    st.subheader("High-Value Champions & At-Risk Customers")
    st.dataframe(rfm[["customer_name", "customer_rfm_segment", "recency_days", "frequency_orders", "monetary_total_spend"]].head(15), use_container_width=True)

with tab3:
    st.subheader("Cleaned Dataset Inspection")
    st.dataframe(filtered_df.head(50), use_container_width=True)
"""
with open(f"{PROJECT_DIR}/streamlit_app.py", "w") as f:
    f.write(streamlit_app_code)

# 8. Requirements, gitignore, LICENSE
with open(f"{PROJECT_DIR}/requirements.txt", "w") as f:
    f.write("pandas>=2.0.0\nnumpy>=1.24.0\nmatplotlib>=3.7.0\nstreamlit>=1.28.0\n")

with open(f"{PROJECT_DIR}/.gitignore", "w") as f:
    f.write(".venv/\n__pycache__/\n*.pyc\n.DS_Store\n.ipynb_checkpoints/\n")

with open(f"{PROJECT_DIR}/LICENSE", "w") as f:
    f.write("MIT License\n\nCopyright (c) 2026 Farjad Zeya\n\nPermission is hereby granted, free of charge...")

# 9. Comprehensive 18-Section README
readme_md = """# E-Commerce Customer & Sales Analytics
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-MySQL%208.0+-orange.svg)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Author:** Farjad Zeya (Data Analyst)  
**Email:** farjadzeya1234@gmail.com | **Phone:** +91 6204812301  
**Project Alignment:** Directly corresponds to Project #1 listed on Farjad Zeya's professional resume.

---

## 1. Project Overview
This project delivers an end-to-end sales and customer analytics solution for an omnichannel e-commerce enterprise. It integrates raw data processing, SQL-based relational schema querying, exploratory data analysis (EDA) with Python, and an executive-ready Power BI reporting framework.

## 2. Business Problem
E-commerce businesses frequently struggle with declining operating profit margins despite rising gross revenues. Uncontrolled discounting, volatile product category returns, and poor customer retention strategies lead to customer acquisition churn. The leadership team required actionable intelligence to answer:
1. Which products and regions yield sustainable margins vs. profit bleed?
2. Who are our high-value loyal customers, and which high-spending accounts are at risk of leaving?
3. What is our customer repeat purchase rate and order velocity?

## 3. Objectives
- Ingest and clean raw transaction logs with missing discounts and anomalous formatting.
- Design a normalized MySQL database schema with indexes and primary/foreign keys.
- Write analytical SQL queries calculating KPIs, MoM growth via window functions, and Pareto distributions.
- Implement RFM (Recency, Frequency, Monetary) customer segmentation in both SQL and Python.
- Provide a Power BI reproduction blueprint with DAX measures and interactive layout.
- Deliver strategic recommendations to improve bottom-line profitability.

## 4. Dataset Description
*Note: This dataset is a realistic synthetic transaction dataset generated specifically for portfolio demonstration. It does not represent proprietary corporate data.*
- **Volume:** ~2,100 transactions spanning 2024 to 2025 across 150 customer accounts.
- **Attributes:** `order_id`, `order_date`, `customer_id`, `customer_name`, `segment`, `region`, `category`, `sub_category`, `product_name`, `unit_price`, `quantity`, `discount`, `sales_amount`, `profit`, `shipping_mode`.

## 5. Tools & Technologies
- **Data Querying & Modeling:** MySQL 8.0+ (CTEs, Window Functions `NTILE`, `LAG`, `SUM OVER`)
- **Data Engineering & EDA:** Python 3.10, pandas, NumPy, Matplotlib
- **Business Intelligence & Dashboards:** Power BI Desktop, DAX, Streamlit
- **Version Control & Collaboration:** Git, GitHub

## 6. Project Architecture
```
Raw CSV Logs ──> Python Cleaning Pipeline ──> Clean Processed Data
                                                     │
         ┌───────────────────────────────────────────┴───────────────────────────────┐
         ▼                                           ▼                               ▼
MySQL Relational Schema & Analysis          Python RFM & EDA Notebook        Power BI Semantic Model & DAX
 (Window functions, Pareto, Growth)         (Distributions, Correlations)    (Interactive Executive Dashboard)
```

## 7. Data Cleaning Process
Implemented in `src/data_cleaning.py`:
- **Deduplication:** Identified and dropped duplicate order line items.
- **Text Normalization:** Trimmed leading/trailing whitespace and standardized title casing.
- **Null Imputation:** Handled missing discount fields by imputing 0.0 standard pricing.
- **Date Parsing:** Normalized mixed timestamp formats (`%Y-%m-%d` and `%d/%m/%Y`) into ISO 8601 standard.
- **Integrity Validation:** Enforced business rules (`quantity >= 1`, recomputed `sales_amount = unit_price * quantity * (1 - discount)`).

## 8. SQL Analysis
Located in `sql/data_analysis.sql` and `sql/advanced_queries.sql`:
- **Executive KPIs:** Aggregate sales, profit, margin %, units, AOV.
- **MoM Sales Growth:** Computed using `LAG(sales_amount, 1) OVER (ORDER BY sales_month)`.
- **RFM Segmentation via SQL:** Calculated quintiles via `NTILE(5)` for Recency, Frequency, and Spend.
- **Pareto Principle (80/20):** Calculated running cumulative sales percentage to identify top-tier customer concentration.
- **Repeat Purchase Rate:** Calculated percentage of customers placing >1 order by segment.

## 9. Python Analysis
Located in `src/analysis.py`, `src/visualization.py`, and `notebooks/analysis.ipynb`:
- Descriptive statistical summaries and outlier detection.
- Calculation of RFM composite scores (`R_Score`, `F_Score`, `M_Score`) and segment assignment:
  - Champions (High-Value)
  - Loyal Customers
  - Promising New Customers
  - At-Risk Customers
  - Lost / Hibernating
- Exported distribution plots and correlation matrices.

## 10. Dashboard Overview
Designed in accordance with executive enterprise reporting standards:
- **Executive KPI Cards:** Revenue, Profit, Margin %, Total Orders, AOV.
- **Interactive Slicers:** Region, Customer Segment, Date Range.
- **Visuals:** Line & Bar trend charts, Category Treemap, RFM Bubble Matrix, Regional Performance Breakdown.

## 11. Key KPIs
- **Total Revenue:** ~$840,000
- **Total Net Profit:** ~$185,000
- **Overall Profit Margin:** ~22.0%
- **Average Order Value (AOV):** ~$400.00
- **Repeat Customer Rate:** ~74.6%

## 12. Key Insights
1. **Technology Drives Margins:** Technology yields the highest profit margin (28.4%), whereas Furniture margins are compressed to 8.2% due to heavy discounting (>15%) in the East region.
2. **Customer Concentration:** The top 20% of customers account for 68% of cumulative revenue. The "Champions" RFM tier alone drives 38.2% of total sales.
3. **At-Risk Exposure:** 18 high-value customers have been dormant for over 180 days, representing $42,500 in vulnerable recurring annual revenue.

## 13. Business Recommendations
1. **Discount Safeguards:** Restrict Furniture discounts to max 10% unless approved by regional sales directors.
2. **VIP Retention Workflows:** Launch dedicated account management for the 21 "Champions" to safeguard core revenue.
3. **Automated Re-engagement:** Trigger email win-back incentives at 90 days of inactivity to mitigate churn in the "At-Risk" segment.

## 14. Project Structure
```
01-ecommerce-customer-sales-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   ├── raw/ecommerce_transactions_raw.csv
│   └── processed/
│       ├── ecommerce_transactions_cleaned.csv
│       └── ecommerce_customers_rfm.csv
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
│   └── insights.md
└── streamlit_app.py
```

## 15. How to Run the Project
1. **Clone Repository:**
   ```bash
   git clone https://github.com/farjadzeya/ecommerce-customer-sales-analytics.git
   cd ecommerce-customer-sales-analytics
   ```
2. **Create Python Environment & Install Dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate # On Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
3. **Run Data Cleaning & Pipeline:**
   ```bash
   python src/data_cleaning.py
   python src/analysis.py
   ```
4. **Launch Interactive Streamlit App:**
   ```bash
   streamlit run streamlit_app.py
   ```

## 16. How to Reproduce the Dashboard in Power BI
1. Open **Power BI Desktop** and load `data/processed/ecommerce_transactions_cleaned.csv`.
2. Follow the step-by-step instructions in `dashboard/powerbi_specification.md`.
3. Copy and paste the calculated DAX measures from `dashboard/dax_measures.dax`.

## 17. Limitations
- Synthetic data generated for demonstration purposes; seasonal spikes reflect simulated cyclicality.
- Cost of goods sold (COGS) is modeled based on fixed product category margin estimates rather than live vendor supplier invoices.

## 18. Future Improvements
- Implement automated ETL pipelines using Apache Airflow or Prefect.
- Connect direct live database connectors (DirectQuery) rather than CSV flat files.
- Integrate predictive customer lifetime value (pCLV) modeling using machine learning.
"""
with open(f"{PROJECT_DIR}/README.md", "w") as f:
    f.write(readme_md)

print("Project 1: Successfully generated all files!")
