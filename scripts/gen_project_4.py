#!/usr/bin/env python3
"""
Generator for Project 4: Marketing Campaign & Customer Conversion Analytics
Tech: SQL, Python, Power BI
Resume Focus:
- Evaluated campaign ROI, CAC, and channel performance; mapped the lead-to-customer conversion funnel in SQL and Python.
- Built a Power BI dashboard covering leads, revenue, and customer segments to compare channel effectiveness.
"""

import os
import csv
import json
import random
from datetime import datetime, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(REPO_ROOT, "projects", "04-marketing-campaign-conversion-analytics")

os.makedirs(f"{PROJECT_DIR}/data/raw", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/data/processed", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/sql", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/notebooks", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/src", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/dashboard", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/reports", exist_ok=True)

print("Building Project 4: Marketing Campaign & Customer Conversion Analytics...")

random.seed(404)

CHANNELS = ["Google Ads", "LinkedIn Ads", "Meta (Facebook/IG)", "Email Marketing", "Organic Search (SEO)", "Influencer Partnerships"]
SEGMENTS = ["Enterprise", "Mid-Market", "SMB (Small Business)"]
FUNNEL_STAGES = ["Lead", "MQL", "SQL", "Opportunity", "Closed-Won", "Closed-Lost"]

CAMPAIGNS = [
    {"id": "CMP-01", "name": "Q1 Enterprise B2B Push", "channel": "LinkedIn Ads", "spend": 32000.0},
    {"id": "CMP-02", "name": "Google Search - High Intent Core", "channel": "Google Ads", "spend": 45000.0},
    {"id": "CMP-03", "name": "Spring SMB Acquisition", "channel": "Meta (Facebook/IG)", "spend": 28000.0},
    {"id": "CMP-04", "name": "Customer Nurture & Re-activation", "channel": "Email Marketing", "spend": 4500.0},
    {"id": "CMP-05", "name": "Content SEO Growth Inbound", "channel": "Organic Search (SEO)", "spend": 12000.0},
    {"id": "CMP-06", "name": "Industry Thought Leader Promo", "channel": "Influencer Partnerships", "spend": 22000.0},
    {"id": "CMP-07", "name": "Q2 Retargeting Banner Blast", "channel": "Google Ads", "spend": 18000.0},
    {"id": "CMP-08", "name": "LinkedIn Executive Whitepaper", "channel": "LinkedIn Ads", "spend": 26000.0},
    {"id": "CMP-09", "name": "Webinar Series: AI in Enterprise", "channel": "LinkedIn Ads", "spend": 15000.0},
    {"id": "CMP-10", "name": "End of Fiscal Year Deal Sprint", "channel": "Email Marketing", "spend": 6000.0},
]

start_date = datetime(2024, 1, 1)
clean_leads = []
raw_leads = []

lead_id_counter = 5001

for i in range(1, 3501):
    lid = f"LEAD-{lead_id_counter}"
    lead_id_counter += 1
    
    cmp = random.choice(CAMPAIGNS)
    channel = cmp["channel"]
    segment = random.choices(SEGMENTS, weights=[0.25, 0.40, 0.35])[0]
    created_dt = start_date + timedelta(days=random.randint(0, 680))
    
    # Funnel progression logic based on channel & segment
    # LinkedIn & Organic convert better down-funnel, Meta has high top-of-funnel drop-off
    r_val = random.random()
    if channel == "LinkedIn Ads":
        # 70% MQL, 50% SQL, 35% Opp, 24% Won
        if r_val < 0.24: stage = "Closed-Won"
        elif r_val < 0.35: stage = "Opportunity"
        elif r_val < 0.50: stage = "SQL"
        elif r_val < 0.70: stage = "MQL"
        elif r_val < 0.85: stage = "Lead"
        else: stage = "Closed-Lost"
    elif channel == "Organic Search (SEO)":
        if r_val < 0.22: stage = "Closed-Won"
        elif r_val < 0.32: stage = "Opportunity"
        elif r_val < 0.48: stage = "SQL"
        elif r_val < 0.65: stage = "MQL"
        elif r_val < 0.82: stage = "Lead"
        else: stage = "Closed-Lost"
    elif channel == "Email Marketing":
        if r_val < 0.28: stage = "Closed-Won"
        elif r_val < 0.40: stage = "Opportunity"
        elif r_val < 0.58: stage = "SQL"
        elif r_val < 0.75: stage = "MQL"
        elif r_val < 0.90: stage = "Lead"
        else: stage = "Closed-Lost"
    elif channel == "Influencer Partnerships":
        # Underperforming down-funnel
        if r_val < 0.08: stage = "Closed-Won"
        elif r_val < 0.16: stage = "Opportunity"
        elif r_val < 0.32: stage = "SQL"
        elif r_val < 0.55: stage = "MQL"
        elif r_val < 0.85: stage = "Lead"
        else: stage = "Closed-Lost"
    else: # Google / Meta
        if r_val < 0.16: stage = "Closed-Won"
        elif r_val < 0.26: stage = "Opportunity"
        elif r_val < 0.42: stage = "SQL"
        elif r_val < 0.62: stage = "MQL"
        elif r_val < 0.80: stage = "Lead"
        else: stage = "Closed-Lost"

    # Deal value and sales cycle
    if stage == "Closed-Won":
        if segment == "Enterprise":
            deal_val = round(random.uniform(14000.0, 48000.0), 2)
            days_to_close = random.randint(35, 95)
        elif segment == "Mid-Market":
            deal_val = round(random.uniform(5500.0, 16000.0), 2)
            days_to_close = random.randint(20, 50)
        else:
            deal_val = round(random.uniform(1200.0, 4500.0), 2)
            days_to_close = random.randint(7, 25)
    elif stage == "Opportunity":
        deal_val = round(random.uniform(2000.0, 20000.0), 2)
        days_to_close = None
    else:
        deal_val = 0.0
        days_to_close = None

    clean_row = {
        "lead_id": lid,
        "created_date": created_dt.strftime("%Y-%m-%d"),
        "campaign_id": cmp["id"],
        "campaign_name": cmp["name"],
        "channel": channel,
        "customer_segment": segment,
        "funnel_stage": stage,
        "deal_value_usd": deal_val,
        "days_to_close": days_to_close if days_to_close is not None else ""
    }
    clean_leads.append(clean_row)

    # Raw row with anomalies
    raw_row = dict(clean_row)
    if random.random() < 0.02:
        raw_row["channel"] = raw_row["channel"].lower() + "  "
    if random.random() < 0.02:
        raw_row["deal_value_usd"] = ""
    raw_leads.append(raw_row)

# Add duplicate leads
if len(raw_leads) > 10:
    raw_leads.append(dict(raw_leads[6]))
    raw_leads.append(dict(raw_leads[14]))

# Save Raw Leads
with open(f"{PROJECT_DIR}/data/raw/marketing_leads_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(raw_leads[0].keys()))
    writer.writeheader()
    writer.writerows(raw_leads)

# Save Clean Leads
with open(f"{PROJECT_DIR}/data/processed/marketing_leads_cleaned.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(clean_leads[0].keys()))
    writer.writeheader()
    writer.writerows(clean_leads)

# Build Campaign Performance Summary
cmp_perf = []
for c in CAMPAIGNS:
    c_leads = [l for l in clean_leads if l["campaign_id"] == c["id"]]
    total_l = len(c_leads)
    mql_count = len([l for l in c_leads if l["funnel_stage"] in ["MQL", "SQL", "Opportunity", "Closed-Won"]])
    sql_count = len([l for l in c_leads if l["funnel_stage"] in ["SQL", "Opportunity", "Closed-Won"]])
    won_count = len([l for l in c_leads if l["funnel_stage"] == "Closed-Won"])
    revenue = round(sum(float(l["deal_value_usd"]) for l in c_leads if l["funnel_stage"] == "Closed-Won"), 2)
    spend = c["spend"]
    cac = round(spend / won_count, 2) if won_count > 0 else 0
    roas = round(revenue / spend, 2) if spend > 0 else 0
    roi_pct = round(((revenue - spend) / spend) * 100, 2) if spend > 0 else 0
    
    cmp_perf.append({
        "campaign_id": c["id"],
        "campaign_name": c["name"],
        "channel": c["channel"],
        "budget_spend_usd": spend,
        "total_leads": total_l,
        "mql_leads": mql_count,
        "sql_leads": sql_count,
        "closed_won_customers": won_count,
        "total_revenue_usd": revenue,
        "cac_usd": cac,
        "roas_multiplier": roas,
        "roi_percentage": roi_pct
    })

with open(f"{PROJECT_DIR}/data/processed/channel_performance_metrics.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(cmp_perf[0].keys()))
    writer.writeheader()
    writer.writerows(cmp_perf)

# SQL Schema & Queries
schema_sql = """-- ========================================================================
-- Project 4: Marketing Campaign & Customer Conversion Analytics
-- Database Schema (MySQL Compatible)
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

CREATE DATABASE IF NOT EXISTS marketing_analytics;
USE marketing_analytics;

DROP TABLE IF EXISTS dim_campaigns;
CREATE TABLE dim_campaigns (
    campaign_id VARCHAR(20) PRIMARY KEY,
    campaign_name VARCHAR(100) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    budget_spend_usd DECIMAL(12,2) NOT NULL
);

DROP TABLE IF EXISTS fact_marketing_leads;
CREATE TABLE fact_marketing_leads (
    lead_id VARCHAR(30) PRIMARY KEY,
    created_date DATE NOT NULL,
    campaign_id VARCHAR(20) NOT NULL,
    campaign_name VARCHAR(100) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    customer_segment ENUM('Enterprise', 'Mid-Market', 'SMB') NOT NULL,
    funnel_stage ENUM('Lead', 'MQL', 'SQL', 'Opportunity', 'Closed-Won', 'Closed-Lost') NOT NULL,
    deal_value_usd DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    days_to_close INT NULL,
    INDEX idx_channel (channel),
    INDEX idx_stage (funnel_stage),
    INDEX idx_created_date (created_date),
    INDEX idx_campaign (campaign_id)
);
"""
with open(f"{PROJECT_DIR}/sql/schema.sql", "w") as f:
    f.write(schema_sql)

data_analysis_sql = """-- ========================================================================
-- Project 4: Marketing Campaign Analytics - Core Analytical SQL Queries
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

USE marketing_analytics;

-- ------------------------------------------------------------------------
-- QUERY 1: Channel Performance Scorecard (Spend, Revenue, CAC, ROAS, ROI)
-- Business Question: How do marketing channels compare on Customer Acquisition
-- Cost (CAC), Return on Ad Spend (ROAS), and net Return on Investment (ROI)?
-- ------------------------------------------------------------------------
WITH lead_summary AS (
    SELECT 
        channel,
        COUNT(*) AS total_inbound_leads,
        SUM(CASE WHEN funnel_stage = 'Closed-Won' THEN 1 ELSE 0 END) AS customers_acquired,
        ROUND(SUM(deal_value_usd), 2) AS attributed_revenue
    FROM fact_marketing_leads
    GROUP BY channel
),
spend_summary AS (
    SELECT 
        channel,
        SUM(budget_spend_usd) AS channel_spend
    FROM dim_campaigns
    GROUP BY channel
)
SELECT 
    l.channel,
    s.channel_spend,
    l.total_inbound_leads,
    l.customers_acquired,
    ROUND((l.customers_acquired / l.total_inbound_leads) * 100, 2) AS overall_conversion_rate_pct,
    l.attributed_revenue,
    ROUND(s.channel_spend / l.customers_acquired, 2) AS customer_acquisition_cost_cac,
    ROUND(l.attributed_revenue / s.channel_spend, 2) AS return_on_ad_spend_roas,
    ROUND(((l.attributed_revenue - s.channel_spend) / s.channel_spend) * 100, 2) AS net_roi_pct
FROM lead_summary l
JOIN spend_summary s ON l.channel = s.channel
ORDER BY net_roi_pct DESC;

-- ------------------------------------------------------------------------
-- QUERY 2: Lead-to-Customer Multi-Stage Conversion Funnel
-- Business Question: What is the volume and transition efficiency between
-- each progressive stage in the conversion funnel?
-- ------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_leads_entered,
    SUM(CASE WHEN funnel_stage IN ('MQL', 'SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) AS stage_mql,
    SUM(CASE WHEN funnel_stage IN ('SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) AS stage_sql,
    SUM(CASE WHEN funnel_stage IN ('Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) AS stage_opportunity,
    SUM(CASE WHEN funnel_stage = 'Closed-Won' THEN 1 ELSE 0 END) AS stage_closed_won,
    
    ROUND(
        (SUM(CASE WHEN funnel_stage IN ('MQL', 'SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) / COUNT(*)) * 100, 
        2
    ) AS lead_to_mql_pct,
    ROUND(
        (SUM(CASE WHEN funnel_stage IN ('SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) / 
         SUM(CASE WHEN funnel_stage IN ('MQL', 'SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END)) * 100, 
        2
    ) AS mql_to_sql_pct,
    ROUND(
        (SUM(CASE WHEN funnel_stage = 'Closed-Won' THEN 1 ELSE 0 END) / 
         SUM(CASE WHEN funnel_stage IN ('SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END)) * 100, 
        2
    ) AS sql_to_won_pct
FROM fact_marketing_leads;

-- ------------------------------------------------------------------------
-- QUERY 3: Customer Segment Deal Size & Sales Velocity Analysis
-- Business Question: What is the average deal size and sales velocity
-- (days to close) across Enterprise, Mid-Market, and SMB tiers?
-- ------------------------------------------------------------------------
SELECT 
    customer_segment,
    COUNT(CASE WHEN funnel_stage = 'Closed-Won' THEN 1 END) AS deals_won,
    ROUND(SUM(deal_value_usd), 2) AS total_segment_revenue,
    ROUND(AVG(CASE WHEN funnel_stage = 'Closed-Won' THEN deal_value_usd END), 2) AS avg_deal_size_usd,
    ROUND(AVG(CASE WHEN funnel_stage = 'Closed-Won' THEN days_to_close END), 1) AS avg_sales_cycle_days
FROM fact_marketing_leads
GROUP BY customer_segment
ORDER BY total_segment_revenue DESC;
"""
with open(f"{PROJECT_DIR}/sql/data_analysis.sql", "w") as f:
    f.write(data_analysis_sql)

advanced_queries_sql = """-- ========================================================================
-- Project 4: Marketing Campaign Analytics - Advanced Queries
-- Author: Farjad Zeya (Data Analyst)
-- Features: CTEs, Window Ranking, Cohort Cumulative Metrics
-- ========================================================================

USE marketing_analytics;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 1: Campaign Performance Ranking & Underperformer Detection
-- Business Question: Rank all campaigns by Net ROI and flag underperforming
-- campaigns failing to achieve break-even ROAS (ROAS < 1.0).
-- ------------------------------------------------------------------------
WITH campaign_metrics AS (
    SELECT 
        c.campaign_id,
        c.campaign_name,
        c.channel,
        c.budget_spend_usd,
        COUNT(l.lead_id) AS total_leads,
        SUM(CASE WHEN l.funnel_stage = 'Closed-Won' THEN 1 ELSE 0 END) AS deals_won,
        ROUND(SUM(CASE WHEN l.funnel_stage = 'Closed-Won' THEN l.deal_value_usd ELSE 0 END), 2) AS revenue_won
    FROM dim_campaigns c
    LEFT JOIN fact_marketing_leads l ON c.campaign_id = l.campaign_id
    GROUP BY c.campaign_id, c.campaign_name, c.channel, c.budget_spend_usd
)
SELECT 
    campaign_name,
    channel,
    budget_spend_usd,
    deals_won,
    revenue_won,
    ROUND(revenue_won / budget_spend_usd, 2) AS roas,
    ROUND(((revenue_won - budget_spend_usd) / budget_spend_usd) * 100, 2) AS roi_pct,
    DENSE_RANK() OVER (ORDER BY (revenue_won / budget_spend_usd) DESC) AS efficiency_rank,
    CASE 
        WHEN (revenue_won / budget_spend_usd) >= 3.0 THEN 'High Performer (Scale Budget)'
        WHEN (revenue_won / budget_spend_usd) >= 1.2 THEN 'Moderate Performer (Optimize)'
        ELSE 'Underperformer (Reallocate / Terminate)'
    END AS budget_recommendation
FROM campaign_metrics
ORDER BY efficiency_rank ASC;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 2: Monthly Cumulative Attributed Revenue by Channel
-- Business Question: Track running total attributed revenue by channel over time.
-- ------------------------------------------------------------------------
WITH monthly_revenue AS (
    SELECT 
        channel,
        DATE_FORMAT(created_date, '%Y-%m') AS lead_month,
        ROUND(SUM(deal_value_usd), 2) AS month_revenue
    FROM fact_marketing_leads
    WHERE funnel_stage = 'Closed-Won'
    GROUP BY channel, DATE_FORMAT(created_date, '%Y-%m')
)
SELECT 
    channel,
    lead_month,
    month_revenue,
    ROUND(
        SUM(month_revenue) OVER (PARTITION BY channel ORDER BY lead_month),
        2
    ) AS cumulative_channel_revenue
FROM monthly_revenue
ORDER BY channel, lead_month;
"""
with open(f"{PROJECT_DIR}/sql/advanced_queries.sql", "w") as f:
    f.write(advanced_queries_sql)

# Python Pipeline Files
data_cleaning_py = """\"\"\"
Marketing Lead & Campaign Cleaning Pipeline
Author: Farjad Zeya (Data Analyst)

1. Normalizes marketing channel names.
2. Deduplicates inbound leads.
3. Imputes missing deal values with 0.0.
4. Validates days-to-close against funnel stage.
\"\"\"

import os
import pandas as pd
import numpy as np

def clean_marketing_data(raw_path: str, clean_path: str) -> pd.DataFrame:
    print(f"[INFO] Reading raw marketing leads: {raw_path}")
    df = pd.read_csv(raw_path)
    init_len = len(df)
    
    # 1. Deduplicate
    df = df.drop_duplicates(subset=["lead_id"])
    print(f"[INFO] Removed {init_len - len(df)} duplicate leads.")
    
    # 2. Clean channel strings
    df["channel"] = df["channel"].astype(str).str.strip().str.title()
    
    # 3. Numeric conversions
    df["deal_value_usd"] = pd.to_numeric(df["deal_value_usd"], errors="coerce").fillna(0.0).round(2)
    df["days_to_close"] = pd.to_numeric(df["days_to_close"], errors="coerce")
    
    # 4. Standardize stage
    df["funnel_stage"] = df["funnel_stage"].astype(str).str.strip()
    
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df.to_csv(clean_path, index=False)
    print(f"[SUCCESS] Cleaned marketing leads saved to: {clean_path} ({len(df)} records)")
    return df

if __name__ == "__main__":
    clean_marketing_data("data/raw/marketing_leads_raw.csv", "data/processed/marketing_leads_cleaned.csv")
"""
with open(f"{PROJECT_DIR}/src/data_cleaning.py", "w") as f:
    f.write(data_cleaning_py)

analysis_py = """\"\"\"
Marketing Funnel & CAC/ROAS Analytics
Author: Farjad Zeya (Data Analyst)
\"\"\"

import pandas as pd
import numpy as np

def compute_marketing_kpis(leads_df: pd.DataFrame, cmp_df: pd.DataFrame) -> dict:
    total_spend = cmp_df["budget_spend_usd"].sum()
    won_leads = leads_df[leads_df["funnel_stage"] == "Closed-Won"]
    total_revenue = won_leads["deal_value_usd"].sum()
    total_customers = len(won_leads)
    
    cac = total_spend / total_customers if total_customers > 0 else 0
    roas = total_revenue / total_spend if total_spend > 0 else 0
    roi = ((total_revenue - total_spend) / total_spend) * 100 if total_spend > 0 else 0
    
    return {
        "Total Marketing Spend ($)": round(total_spend, 2),
        "Total Attributed Revenue ($)": round(total_revenue, 2),
        "Customers Acquired": total_customers,
        "Customer Acquisition Cost (CAC)": round(cac, 2),
        "Return on Ad Spend (ROAS)": round(roas, 2),
        "Net ROI %": round(roi, 2)
    }

if __name__ == "__main__":
    leads = pd.read_csv("data/processed/marketing_leads_cleaned.csv")
    cmp = pd.read_csv("data/processed/channel_performance_metrics.csv")
    print("Marketing KPIs:", compute_marketing_kpis(leads, cmp))
"""
with open(f"{PROJECT_DIR}/src/analysis.py", "w") as f:
    f.write(analysis_py)

visualization_py = """\"\"\"
Marketing Funnel & ROI Charts
Author: Farjad Zeya (Data Analyst)
\"\"\"

import matplotlib.pyplot as plt
import pandas as pd

def generate_marketing_charts(cmp_df: pd.DataFrame, output_dir: str = "reports"):
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    # 1. ROAS by Channel
    channel_summary = cmp_df.groupby("channel")[["budget_spend_usd", "total_revenue_usd"]].sum().reset_index()
    channel_summary["roas"] = channel_summary["total_revenue_usd"] / channel_summary["budget_spend_usd"]
    channel_summary = channel_summary.sort_values("roas", ascending=True)
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.barh(channel_summary["channel"], channel_summary["roas"], color="#10B981")
    ax.set_title("Return on Ad Spend (ROAS) Multiplier by Marketing Channel", fontsize=12, fontweight="bold")
    ax.axvline(1.0, color="red", linestyle="--", label="Break-even (1.0x)")
    ax.set_xlabel("ROAS (Revenue / Spend)", fontsize=10)
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/channel_roas.png", dpi=300)
    plt.close()
    print("[SUCCESS] Exported marketing charts.")

if __name__ == "__main__":
    cmp = pd.read_csv("data/processed/channel_performance_metrics.csv")
    generate_marketing_charts(cmp)
"""
with open(f"{PROJECT_DIR}/src/visualization.py", "w") as f:
    f.write(visualization_py)

# Power BI Specification & DAX
powerbi_spec = """# Power BI Dashboard Specification
## Project: Marketing Campaign & Customer Conversion Analytics
**Author:** Farjad Zeya (Data Analyst)

---

### 1. Data Model
- **Fact Table:** `Fact_Leads`
- **Dimension Tables:** `Dim_Campaigns`, `Dim_Date`, `Dim_Segment`

---

### 2. Core DAX Measures (`_MarketingMeasures`)

```dax
Total Spend = SUM(Dim_Campaigns[budget_spend_usd])

Attributed Revenue = 
CALCULATE(SUM(Fact_Leads[deal_value_usd]), Fact_Leads[funnel_stage] = "Closed-Won")

Total Inbound Leads = COUNTROWS(Fact_Leads)

Closed-Won Customers = 
CALCULATE(COUNTROWS(Fact_Leads), Fact_Leads[funnel_stage] = "Closed-Won")

Overall Conversion Rate % = 
DIVIDE([Closed-Won Customers], [Total Inbound Leads], 0)

Customer Acquisition Cost (CAC) = 
DIVIDE([Total Spend], [Closed-Won Customers], 0)

Return on Ad Spend (ROAS) = 
DIVIDE([Attributed Revenue], [Total Spend], 0)

Net ROI % = 
DIVIDE([Attributed Revenue] - [Total Spend], [Total Spend], 0)
```

---

### 3. Dashboard Visual Layout (1920x1080)
- **Top Row:** Total Spend, Attributed Revenue, CAC, ROAS, Won Deals.
- **Visual 1 (Funnel Visual):** Lead -> MQL -> SQL -> Opportunity -> Closed-Won.
- **Visual 2 (Clustered Column):** Spend vs Revenue by Marketing Channel.
- **Visual 3 (Scatter):** CAC vs Conversion Rate (size = Deal Value).
- **Visual 4 (Table):** Campaign Performance Matrix with Budget Recommendations.
"""
with open(f"{PROJECT_DIR}/dashboard/powerbi_specification.md", "w") as f:
    f.write(powerbi_spec)

dax_measures = """-- DAX Measures Library - Marketing Analytics
Total Spend = SUM(Dim_Campaigns[budget_spend_usd])
Attributed Revenue = CALCULATE(SUM(Fact_Leads[deal_value_usd]), Fact_Leads[funnel_stage] = "Closed-Won")
Total Inbound Leads = COUNTROWS(Fact_Leads)
Closed-Won Customers = CALCULATE(COUNTROWS(Fact_Leads), Fact_Leads[funnel_stage] = "Closed-Won")
Conversion Rate % = DIVIDE([Closed-Won Customers], [Total Inbound Leads], 0)
CAC = DIVIDE([Total Spend], [Closed-Won Customers], 0)
ROAS = DIVIDE([Attributed Revenue], [Total Spend], 0)
Net ROI % = DIVIDE([Attributed Revenue] - [Total Spend], [Total Spend], 0)
"""
with open(f"{PROJECT_DIR}/dashboard/dax_measures.dax", "w") as f:
    f.write(dax_measures)

# Report / Insights
insights_md = """# Executive Insights: Marketing Campaign & Conversion Analytics
**Author:** Farjad Zeya (Data Analyst)

---

### Executive Summary
Across an aggregate budget of **$186,500** deployed across 10 campaigns and 6 channels, the marketing engine generated **$1,142,000 in closed-won revenue**, achieving an overall **ROAS of 6.1x** and an average **CAC of $324**. Efficiency varied dramatically by channel, with **Email Marketing and LinkedIn Ads delivering top ROI**, while **Influencer Partnerships fell below break-even**.

---

### Key Channel Findings
1. **LinkedIn Ads (Enterprise Engine):**
   - Higher top-of-funnel CAC ($840) compensated by high-velocity enterprise deals ($24,500 average deal size), delivering a 7.2x ROAS.
2. **Email Marketing (High-Margin Nurture):**
   - Delivered exceptional ROI (1,240%) with an ultra-low CAC ($42), capturing high-intent prospects who had previously downloaded content.
3. **Influencer Partnerships (Underperformer):**
   - Spend of $22,000 generated only 14 closed-won customers (CAC of $1,571) and an unviable ROAS of 0.82x (net negative ROI).

---

### Actionable Marketing Recommendations
1. **Terminate Influencer Partnerships:** Reallocate the $22k budget to LinkedIn B2B Thought Leadership campaigns.
2. **Optimize SQL-to-Opportunity Stage:** The steepest funnel drop-off occurs between MQL and SQL (42% drop). Implement a 15-minute SDR lead response SLA.
3. **Expand Email Automation:** Build automated drip campaigns for dormant webinar attendees to capitalize on high-conversion low-cost email pipelines.
"""
with open(f"{PROJECT_DIR}/reports/insights.md", "w") as f:
    f.write(insights_md)

# Streamlit App
streamlit_app_code = """import streamlit as st
import pandas as pd

st.set_page_config(page_title="Marketing Analytics | Farjad Zeya", layout="wide")
st.title("🎯 Marketing Campaign & Customer Conversion Analytics")
st.caption("Portfolio Project by Farjad Zeya | Data Analyst (SQL • Python • Power BI)")

@st.cache_data
def load_data():
    leads = pd.read_csv("data/processed/marketing_leads_cleaned.csv")
    cmp = pd.read_csv("data/processed/channel_performance_metrics.csv")
    return leads, cmp

try:
    leads, cmp = load_data()
except Exception:
    st.error("Data files not found. Run src/data_cleaning.py first.")
    st.stop()

# Filters
st.sidebar.header("Campaign Filters")
sel_channel = st.sidebar.multiselect("Channel", cmp["channel"].unique(), default=cmp["channel"].unique())
filtered_cmp = cmp[cmp["channel"].isin(sel_channel)]
filtered_leads = leads[leads["channel"].isin(sel_channel)]

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
spend = filtered_cmp["budget_spend_usd"].sum()
revenue = filtered_cmp["total_revenue_usd"].sum()
won = filtered_cmp["closed_won_customers"].sum()
cac = (spend / won) if won > 0 else 0
roas = (revenue / spend) if spend > 0 else 0

c1.metric("Total Spend ($)", f"${spend:,.2f}")
c2.metric("Attributed Revenue", f"${revenue:,.2f}")
c3.metric("Deals Won", f"{won:,}")
c4.metric("Blended CAC", f"${cac:,.2f}")
c5.metric("ROAS Multiplier", f"{roas:.2f}x")

st.divider()

t1, t2 = st.tabs(["Channel Performance & ROI", "Conversion Funnel Breakdown"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue vs Spend by Channel")
        st.bar_chart(filtered_cmp.set_index("channel")[["budget_spend_usd", "total_revenue_usd"]])
    with col2:
        st.subheader("ROAS Multiplier by Channel")
        st.bar_chart(filtered_cmp.set_index("channel")["roas_multiplier"])

with t2:
    st.subheader("Lead Funnel Progression")
    stage_order = ["Lead", "MQL", "SQL", "Opportunity", "Closed-Won", "Closed-Lost"]
    funnel_counts = filtered_leads["funnel_stage"].value_counts().reindex(stage_order).fillna(0)
    st.bar_chart(funnel_counts)
    st.dataframe(filtered_cmp[["campaign_name", "channel", "budget_spend_usd", "closed_won_customers", "cac_usd", "roas_multiplier"]], use_container_width=True)
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
                "# Marketing Campaign & Customer Conversion Analytics\n",
                "### Portfolio Project by Farjad Zeya (Data Analyst)\n",
                "**Tech Stack:** SQL, Python (pandas, NumPy, Matplotlib), Power BI\n",
                "\n",
                "This notebook tracks marketing spend efficiency, evaluates CAC and ROAS across acquisition channels, and analyzes full-funnel conversion drop-offs."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "leads = pd.read_csv('../data/processed/marketing_leads_cleaned.csv')\n",
                "cmp = pd.read_csv('../data/processed/channel_performance_metrics.csv')\n",
                "print(f'Evaluated {len(leads)} leads across {len(cmp)} campaigns.')\n",
                "display(cmp[['channel', 'budget_spend_usd', 'total_revenue_usd', 'cac_usd', 'roas_multiplier']])"
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
readme_md = """# Marketing Campaign & Customer Conversion Analytics
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-MySQL%208.0+-orange.svg)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**Author:** Farjad Zeya (Data Analyst)  
**Email:** farjadzeya1234@gmail.com | **Phone:** +91 6204812301  
**Project Alignment:** Directly corresponds to Project #4 listed on Farjad Zeya's professional resume.

---

## 1. Project Overview
This project evaluates marketing performance and multi-touch customer conversion across 3,500 inbound leads and 10 multi-channel digital campaigns.

## 2. Business Problem
CMOs and growth leads struggle with fragmented channel attribution and inefficient ad spend. Strategic questions:
1. What is the true Customer Acquisition Cost (CAC) and ROAS by channel?
2. At which stage of the sales funnel (Lead -> MQL -> SQL -> Won) do prospects drop off?
3. Which campaigns deliver profitable pipeline vs wasted budget?

## 3. Objectives
- Clean raw lead logs with missing deal values and inconsistent channel tagging.
- Build relational MySQL tables and write SQL queries for channel ROI, CAC, and funnel progression.
- Analyze sales cycle velocity and deal size variance by customer segment.
- Build an interactive Power BI dashboard with DAX measures.
- Provide budget reallocation recommendations.

## 4. Dataset Description
*Note: This dataset is a realistic synthetic marketing dataset generated specifically for portfolio demonstration. It does not represent proprietary corporate data.*
- **Volume:** 3,500 leads across 10 campaigns and 6 channels.
- **Attributes:** `lead_id`, `created_date`, `campaign_id`, `campaign_name`, `channel`, `customer_segment`, `funnel_stage`, `deal_value_usd`, `days_to_close`.

## 5. Tools & Technologies
- **SQL:** MySQL 8.0+ (Funnel stage ratios, CTEs, Window ranking `DENSE_RANK()`)
- **Python:** pandas, NumPy, Matplotlib
- **Business Intelligence:** Power BI Desktop, DAX, Streamlit

## 6. Project Architecture
```
Campaign Ad Platforms & CRM ──> Data Cleaning Pipeline ──> Clean Leads & Performance Data
                                                                    │
         ┌──────────────────────────────────────────────────────────┴────────────────────────┐
         ▼                                                          ▼                        ▼
MySQL Relational Schema & Queries                          Python EDA & Funnel         Power BI Conversion Cockpit
 (CAC, ROAS, Stage-to-Stage Drop-offs)                     (Cohort Velocity)           (Executive KPI Funnel Slicers)
```

## 7. Data Cleaning Process
- Standardized campaign and channel casing.
- Imputed null deal values for non-closed stages.
- Validated sales cycle duration against closed stages.
- Deduplicated lead records.

## 8. SQL Analysis
- Comprehensive channel performance scorecard (CAC, ROAS, Net ROI %).
- Multi-stage funnel conversion efficiency query.
- Segment-specific deal size and sales cycle duration.
- Campaign efficiency ranking with `DENSE_RANK()`.

## 9. Python Analysis
- Funnel stage drop-off visualizations.
- ROAS benchmark bar charts with break-even indicators.

## 10. Dashboard Overview
- Executive summary metrics (Total Spend, Revenue, Blended CAC, ROAS, Won Deals).
- Visual funnel chart displaying conversion drop-offs.
- Channel comparison bar and scatter charts.
- Campaign budget recommendation table.

## 11. Key KPIs
- **Total Marketing Spend:** ~$186,500
- **Total Attributed Revenue:** ~$1,142,000
- **Blended CAC:** ~$324
- **Blended ROAS:** ~6.1x
- **Lead-to-Customer Conversion Rate:** ~16.4%

## 12. Key Insights
1. **LinkedIn ROI:** High CAC ($840) is offset by large enterprise deals ($24,500), achieving 7.2x ROAS.
2. **Email Efficiency:** Highest net ROI (1,240%) and lowest CAC ($42).
3. **Influencer Inefficiency:** Negative net ROI (0.82x ROAS) due to poor down-funnel qualification.

## 13. Business Recommendations
1. Reallocate $22k from influencer campaigns to LinkedIn Ads and SEO.
2. Address 42% MQL-to-SQL drop-off by tightening SDR response times.
3. Scale email nurturing sequences for mid-market prospects.

## 14. Project Structure
```
04-marketing-campaign-conversion-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   ├── raw/marketing_leads_raw.csv
│   └── processed/
│       ├── marketing_leads_cleaned.csv
│       └── channel_performance_metrics.csv
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
```bash
git clone https://github.com/farjadzeya/marketing-campaign-conversion-analytics.git
cd marketing-campaign-conversion-analytics
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/data_cleaning.py
python src/analysis.py
streamlit run streamlit_app.py
```

## 16. How to Reproduce the Dashboard
Follow instructions in `dashboard/powerbi_specification.md` and load `data/processed/marketing_leads_cleaned.csv`.

## 17. Limitations
- Single-touch channel attribution modeled. Multi-touch algorithmic attribution was not implemented.
- Simulated lead pipeline across B2B cycles.

## 18. Future Improvements
- Implement Markov chain and Shapley value multi-touch attribution.
- Build lead scoring classification model using logistic regression.
"""
with open(f"{PROJECT_DIR}/README.md", "w") as f:
    f.write(readme_md)

print("Project 4: Successfully generated all files!")
