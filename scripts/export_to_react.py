#!/usr/bin/env python3
"""
Compiles all data from projects 1, 2, 3, 4 into a clean TypeScript module in /src/data/portfolioData.ts.
Avoids f-string escaping pitfalls by serializing structured Python dictionaries to JSON.
"""

import os
import json
import csv

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DATA_DIR = os.path.join(REPO_ROOT, "src", "data")
os.makedirs(SRC_DATA_DIR, exist_ok=True)

def read_csv_sample(path, max_rows=50):
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
            rows.append(row)
    return rows

def read_file_safe(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Load files for Project 1
p1_clean_csv = read_csv_sample(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/data/processed/ecommerce_transactions_cleaned.csv"), 150)
p1_rfm_csv = read_csv_sample(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/data/processed/ecommerce_customers_rfm.csv"), 50)
p1_schema = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/sql/schema.sql"))
p1_analysis_sql = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/sql/data_analysis.sql"))
p1_adv_sql = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/sql/advanced_queries.sql"))
p1_dax = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/dashboard/dax_measures.dax"))
p1_insights = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/reports/insights.md"))
p1_readme = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/README.md"))
p1_py_clean = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/src/data_cleaning.py"))
p1_py_analysis = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/src/analysis.py"))
p1_streamlit = read_file_safe(os.path.join(REPO_ROOT, "projects/01-ecommerce-customer-sales-analytics/streamlit_app.py"))

# Load files for Project 2
p2_clean_csv = read_csv_sample(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/data/processed/banking_churn_cleaned.csv"), 150)
p2_schema = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/sql/schema.sql"))
p2_analysis_sql = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/sql/data_analysis.sql"))
p2_adv_sql = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/sql/advanced_queries.sql"))
p2_dax = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/dashboard/dax_measures.dax"))
p2_insights = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/reports/insights.md"))
p2_readme = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/README.md"))
p2_py_clean = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/src/data_cleaning.py"))
p2_py_analysis = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/src/analysis.py"))
p2_streamlit = read_file_safe(os.path.join(REPO_ROOT, "projects/02-banking-customer-churn-retention/streamlit_app.py"))

# Load files for Project 3
p3_clean_csv = read_csv_sample(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/data/processed/supply_chain_shipments_cleaned.csv"), 150)
p3_scorecards_csv = read_csv_sample(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/data/processed/supplier_scorecards.csv"), 20)
p3_schema = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/sql/schema.sql"))
p3_analysis_sql = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/sql/data_analysis.sql"))
p3_adv_sql = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/sql/advanced_queries.sql"))
p3_dax = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/dashboard/dax_measures.dax"))
p3_insights = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/reports/insights.md"))
p3_readme = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/README.md"))
p3_py_clean = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/src/data_cleaning.py"))
p3_py_analysis = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/src/analysis.py"))
p3_excel = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/reports/excel_analysis_guide.md"))
p3_streamlit = read_file_safe(os.path.join(REPO_ROOT, "projects/03-supply-chain-delivery-analytics/streamlit_app.py"))

# Load files for Project 4
p4_clean_csv = read_csv_sample(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/data/processed/marketing_leads_cleaned.csv"), 150)
p4_channels_csv = read_csv_sample(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/data/processed/channel_performance_metrics.csv"), 20)
p4_schema = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/sql/schema.sql"))
p4_analysis_sql = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/sql/data_analysis.sql"))
p4_adv_sql = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/sql/advanced_queries.sql"))
p4_dax = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/dashboard/dax_measures.dax"))
p4_insights = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/reports/insights.md"))
p4_readme = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/README.md"))
p4_py_clean = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/src/data_cleaning.py"))
p4_py_analysis = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/src/analysis.py"))
p4_streamlit = read_file_safe(os.path.join(REPO_ROOT, "projects/04-marketing-campaign-conversion-analytics/streamlit_app.py"))

root_readme = read_file_safe(os.path.join(REPO_ROOT, "PORTFOLIO_README.md"))

farjad_profile = {
  "name": "Farjad Zeya",
  "title": "Data Analyst",
  "email": "farjadzeya1234@gmail.com",
  "phone": "+91 6204812301",
  "location": "Delhi NCR, India",
  "education": "B.Tech in Computer Science Engineering, Jamia Hamdard (2026)",
  "summary": "Results-oriented Data Analyst with hands-on experience across the full data workflow — cleaning, EDA, visualisation, and stakeholder reporting. Currently working at CK Infrastructure Ltd, maintaining diesel consumption databases and delivering Excel/Pivot Table MIS reports to management.",
  "skills": [
    { "category": "Data Analysis & EDA", "items": ["Python (pandas, NumPy, Matplotlib)", "SQL", "Microsoft Excel", "Pivot Tables", "VLOOKUP/XLOOKUP", "Descriptive Statistics", "Trend Analysis", "RFM Analysis", "Churn & Funnel Analysis"] },
    { "category": "Databases & Querying", "items": ["MySQL", "SELECT", "JOINs", "Aggregations", "Filtering", "Subqueries", "CTEs", "Window Functions (NTILE, LAG, LEAD, DENSE_RANK)"] },
    { "category": "Reporting & Dashboards", "items": ["Power BI Dashboards", "DAX Calculated Measures", "Excel Pivot Tables & Charts", "MIS Reporting", "KPI Dashboards", "Data Visualisation"] },
    { "category": "Data Quality & Engineering", "items": ["Data Cleaning", "Data Validation", "Data Preprocessing", "Data Integrity", "Feature Engineering"] },
    { "category": "Tools & Platforms", "items": ["Jupyter Notebook", "Git", "GitHub", "VS Code", "Power BI", "Streamlit"] }
  ],
  "experience": [
    {
      "role": "Maintenance Data Analyst",
      "company": "CK Infrastructure Ltd",
      "duration": "Aug 2026 – Present",
      "location": "New Delhi",
      "bullets": [
        "MIS Reporting: Build Excel Pivot Table dashboards and charts presenting monthly diesel consumption trends, error summaries, and fleet data to management — enabling data-driven maintenance decisions.",
        "Data Validation: Validate initial and final meter readings for all vehicles and machinery to detect discrepancies, ensuring accurate fuel consumption and mileage reporting across the fleet.",
        "Consumption Analysis: Compute monthly average diesel consumption per machine, track usage patterns, and flag deviations from expected benchmarks to support cost-control initiatives.",
        "Data Integrity: Maintain structured machinery records and datasets, enforcing accuracy, completeness, and timely updates across all maintenance logs."
      ]
    },
    {
      "role": "Data Analyst Intern",
      "company": "Cochain LLC",
      "duration": "May 2025 – Aug 2025",
      "location": "Remote",
      "bullets": [
        "EDA & Insights: Performed exploratory data analysis (EDA) using Python (pandas, NumPy) to identify patterns, trends, correlations, and anomalies across structured business datasets.",
        "Data Cleaning & Preprocessing: Collected, cleaned, and validated raw datasets; applied feature engineering and data preprocessing to prepare data pipelines for ML model training.",
        "Model Evaluation: Evaluated classification and regression model performance using Accuracy, Precision, Recall, and F1-Score; presented findings and analytical recommendations to stakeholders.",
        "Stakeholder Communication: Documented analysis workflows and delivered insight reports, translating data findings into clear, actionable business recommendations."
      ]
    },
    {
      "role": "Software Developer Intern",
      "company": "CDAC — Patna",
      "duration": "Jan 2024 – Feb 2024",
      "location": "Patna",
      "bullets": [
        "SQL Database Design: Designed, queried, and maintained SQL databases for structured data storage, retrieval, and integration across application modules.",
        "API Development: Built RESTful APIs connecting server-side logic with database operations; documented workflows and collaborated via Git."
      ]
    }
  ]
}

projects_data = [
  {
    "id": "ecommerce-analytics",
    "number": 1,
    "title": "E-Commerce Customer & Sales Analytics",
    "shortTitle": "E-Commerce Analytics",
    "tagline": "Omnichannel sales, profitability margins, and RFM customer segmentation model",
    "tech": ["SQL", "Python", "Power BI", "pandas", "RFM Segmentation"],
    "resumeBullet1": "Analysed sales, profit, customers, products, and regions using SQL and Python; built an interactive Power BI KPI dashboard.",
    "resumeBullet2": "Applied RFM analysis to segment customers and identify high-value, loyal, and at-risk groups.",
    "kpis": [
      { "label": "Total Revenue", "value": "$842,500", "delta": "+18.4% YoY", "sub": "Gross sales volume" },
      { "label": "Total Net Profit", "value": "$185,350", "delta": "+14.2% YoY", "sub": "Operating contribution" },
      { "label": "Profit Margin", "value": "22.0%", "delta": "+1.8 pts", "sub": "Technology leads at 28.4%" },
      { "label": "Average Order Value", "value": "$387.80", "delta": "+5.1%", "sub": "2,173 completed orders" },
      { "label": "Repeat Purchase Rate", "value": "74.6%", "delta": "Strong Loyalty", "sub": "150 customer base" }
    ],
    "categoryData": [
      { "name": "Technology", "value": 412500, "secondary": 117150 },
      { "name": "Office Supplies", "value": 248900, "secondary": 60000 },
      { "name": "Furniture", "value": 181100, "secondary": 14850 }
    ],
    "timeData": [
      { "date": "Jan 24", "value": 28400, "secondary": 6200 },
      { "date": "Apr 24", "value": 34100, "secondary": 7800 },
      { "date": "Jul 24", "value": 31500, "secondary": 6900 },
      { "date": "Oct 24", "value": 39800, "secondary": 9100 },
      { "date": "Jan 25", "value": 36200, "secondary": 8100 },
      { "date": "Apr 25", "value": 42500, "secondary": 9700 },
      { "date": "Jul 25", "value": 41000, "secondary": 8900 },
      { "date": "Oct 25", "value": 49200, "secondary": 11200 },
      { "date": "Dec 25", "value": 54300, "secondary": 12400 }
    ],
    "segmentData": [
      { "name": "Champions (High-Value)", "value": 38.2, "color": "#10B981" },
      { "name": "Loyal Customers", "value": 29.5, "color": "#3B82F6" },
      { "name": "Promising New", "value": 14.1, "color": "#F59E0B" },
      { "name": "At-Risk Customers", "value": 12.4, "color": "#EF4444" },
      { "name": "Lost / Hibernating", "value": 5.8, "color": "#6B7280" }
    ],
    "sampleRecords": p1_clean_csv,
    "secondaryRecords": p1_rfm_csv,
    "sqlFiles": [
      { "name": "schema.sql", "description": "MySQL DDL table schemas, indexes, and constraints", "content": p1_schema },
      { "name": "data_analysis.sql", "description": "Core business queries for KPIs, categories, regions, and trends", "content": p1_analysis_sql },
      { "name": "advanced_queries.sql", "description": "Window functions (NTILE, LAG), Pareto 80/20, and RFM scoring CTEs", "content": p1_adv_sql }
    ],
    "pythonFiles": [
      { "name": "data_cleaning.py", "description": "Pandas deduplication, date parsing, null imputation, and data audit", "content": p1_py_clean },
      { "name": "analysis.py", "description": "RFM quintile scoring and executive KPI calculation logic", "content": p1_py_analysis }
    ],
    "daxMeasures": p1_dax,
    "insightsMd": p1_insights,
    "readmeMd": p1_readme,
    "streamlitCode": p1_streamlit,
    "cleaningSummary": {
      "rawRows": 2175,
      "cleanedRows": 2173,
      "issuesFound": ["2 Duplicate transaction entries", "65 Missing discount values (null)", "43 Mixed date formats (DD/MM/YYYY vs YYYY-MM-DD)", "87 Casing discrepancies in categories ('furniture ' vs 'Furniture')"],
      "actionsTaken": ["Deduplicated records on order_id + product", "Imputed 0.0 for missing discounts", "Normalized dates to ISO 8601 YYYY-MM-DD", "Stripped whitespace and applied title-casing"]
    }
  },
  {
    "id": "banking-churn",
    "number": 2,
    "title": "Banking Customer Churn & Retention Analysis",
    "shortTitle": "Banking Churn & Retention",
    "tagline": "Empirical churn driver discovery, tenure cohorts, and capital-at-risk mitigation",
    "tech": ["SQL", "Python", "Power BI", "Statistics", "Retention Modeling"],
    "resumeBullet1": "Measured churn rate and segmented customers by tenure, activity, and balance to uncover key churn drivers.",
    "resumeBullet2": "Built a Power BI retention dashboard highlighting at-risk segments to support retention strategy.",
    "kpis": [
      { "label": "Overall Churn Rate", "value": "20.4%", "delta": "Industry Avg: 18%", "sub": "510 / 2,500 customers" },
      { "label": "Total Capital at Risk", "value": "$48.2M", "delta": "High Exposure", "sub": "Cumulative churned balances" },
      { "label": "Active Member Churn", "value": "14.2%", "delta": "-15.6% vs Inactive", "sub": "Digital engagement anchor" },
      { "label": "Inactive Member Churn", "value": "29.8%", "delta": "Critical Alert", "sub": "2.1x higher attrition probability" },
      { "label": "High Risk Customers", "value": "312", "delta": "Priority List", "sub": "$31.5M balance exposure" }
    ],
    "categoryData": [
      { "name": "1 Product", "value": 27.6, "secondary": 1250 },
      { "name": "2 Products (Optimal)", "value": 8.1, "secondary": 1100 },
      { "name": "3 Products (Warning)", "value": 78.4, "secondary": 125 },
      { "name": "4 Products (Critical)", "value": 92.3, "secondary": 25 }
    ],
    "timeData": [
      { "date": "0-1 Yr (Onboarding)", "value": 24.8, "secondary": 410 },
      { "date": "2-4 Yrs (Early)", "value": 21.2, "secondary": 780 },
      { "date": "5-7 Yrs (Established)", "value": 18.5, "secondary": 820 },
      { "date": "8+ Yrs (Mature)", "value": 17.1, "secondary": 490 }
    ],
    "segmentData": [
      { "name": "Germany (32.4% Churn)", "value": 32.4, "color": "#EF4444" },
      { "name": "France (16.2% Churn)", "value": 16.2, "color": "#3B82F6" },
      { "name": "Spain (16.8% Churn)", "value": 16.8, "color": "#10B981" }
    ],
    "sampleRecords": p2_clean_csv,
    "sqlFiles": [
      { "name": "schema.sql", "description": "MySQL DDL table schemas, indices on activity and products", "content": p2_schema },
      { "name": "data_analysis.sql", "description": "Churn rate breakdown across tenure, activity, products, and geography", "content": p2_analysis_sql },
      { "name": "advanced_queries.sql", "description": "Multi-factor risk scoring CTE, NTILE credit quintiles, and cumulative balance window functions", "content": p2_adv_sql }
    ],
    "pythonFiles": [
      { "name": "data_cleaning.py", "description": "Imputation of credit score by geo median, negative age fixing, risk tier creation", "content": p2_py_clean },
      { "name": "analysis.py", "description": "Driver cross-tabulation, correlation calculations, and risk score thresholds", "content": p2_py_analysis }
    ],
    "daxMeasures": p2_dax,
    "insightsMd": p2_insights,
    "readmeMd": p2_readme,
    "streamlitCode": p2_streamlit,
    "cleaningSummary": {
      "rawRows": 2502,
      "cleanedRows": 2500,
      "issuesFound": ["2 Duplicate customer IDs", "62 Missing credit scores", "38 Negative age anomalies (-42, -55)", "74 Formatting variations in country names (' france ')"],
      "actionsTaken": ["Deduplicated on customer_id", "Imputed median credit score by geography", "Cleaned age using absolute transformation", "Standardized and trimmed country strings"]
    }
  },
  {
    "id": "supply-chain-analytics",
    "number": 3,
    "title": "Supply Chain & Delivery Performance Analytics",
    "shortTitle": "Supply Chain Analytics",
    "tagline": "Fulfillment SLA tracking, warehouse dispatch bottlenecks, and freight cost optimization",
    "tech": ["SQL", "Microsoft Excel", "Power BI", "MIS Reporting", "Pivot Tables"],
    "resumeBullet1": "Analysed on-time delivery, delays, supplier and warehouse performance, and shipping costs by region using SQL and Excel.",
    "resumeBullet2": "Built a Power BI dashboard tracking delivery KPIs and regional performance to pinpoint bottlenecks.",
    "kpis": [
      { "label": "On-Time Delivery (OTD)", "value": "81.4%", "delta": "SLA Target: 88%", "sub": "1,791 / 2,200 consignments" },
      { "label": "Average Delay (Late)", "value": "3.4 Days", "delta": "-0.6 days MoM", "sub": "Across 409 delayed orders" },
      { "label": "Total Freight Spend", "value": "$312,400", "delta": "+8.2% vs budget", "sub": "2,200 shipments" },
      { "label": "Freight Cost / KG", "value": "$1.84", "delta": "Road: $1.38 | Air: $3.50", "sub": "Average unit transport cost" },
      { "label": "Damage / Defect Rate", "value": "3.1%", "delta": "Below 4% SLA", "sub": "Tier 1: 2.0% | Tier 3: 6.8%" }
    ],
    "categoryData": [
      { "name": "North Hub (Delhi)", "value": 84.8, "secondary": 1.1 },
      { "name": "West Port (Mumbai)", "value": 86.4, "secondary": 0.8 },
      { "name": "South Central (Bengaluru)", "value": 82.2, "secondary": 1.3 },
      { "name": "East Gateway (Kolkata)", "value": 71.2, "secondary": 2.4 }
    ],
    "timeData": [
      { "date": "Q1 2024", "value": 83.2, "secondary": 3.1 },
      { "date": "Q2 2024", "value": 80.5, "secondary": 3.6 },
      { "date": "Q3 2024", "value": 82.1, "secondary": 3.3 },
      { "date": "Q4 2024", "value": 79.4, "secondary": 3.8 },
      { "date": "Q1 2025", "value": 82.8, "secondary": 3.2 },
      { "date": "Q2 2025", "value": 81.0, "secondary": 3.5 },
      { "date": "Q3 2025", "value": 83.5, "secondary": 3.0 },
      { "date": "Q4 2025", "value": 81.4, "secondary": 3.4 }
    ],
    "segmentData": [
      { "name": "BlueDart Express", "value": 87.2, "color": "#10B981" },
      { "name": "Delhivery Logistics", "value": 83.5, "color": "#3B82F6" },
      { "name": "FedEx Freight", "value": 81.0, "color": "#F59E0B" },
      { "name": "DTDC Surface", "value": 73.8, "color": "#EF4444" }
    ],
    "sampleRecords": p3_clean_csv,
    "secondaryRecords": p3_scorecards_csv,
    "sqlFiles": [
      { "name": "schema.sql", "description": "MySQL DDL table schemas, indices on status, carrier, and warehouse", "content": p3_schema },
      { "name": "data_analysis.sql", "description": "OTD %, warehouse latency, supplier scorecards, and regional freight costs", "content": p3_analysis_sql },
      { "name": "advanced_queries.sql", "description": "Route bottleneck matrix with DENSE_RANK() and 30-shipment moving average window frame", "content": p3_adv_sql }
    ],
    "pythonFiles": [
      { "name": "data_cleaning.py", "description": "Imputation of delivery dates, correction of negative weights, carrier standardization", "content": p3_py_clean },
      { "name": "analysis.py", "description": "Supply chain KPI engine and lead time statistical summaries", "content": p3_py_analysis }
    ],
    "daxMeasures": p3_dax,
    "insightsMd": p3_insights,
    "readmeMd": p3_readme,
    "excelGuide": p3_excel,
    "streamlitCode": p3_streamlit,
    "cleaningSummary": {
      "rawRows": 2202,
      "cleanedRows": 2200,
      "issuesFound": ["2 Duplicate shipment consignment IDs", "55 Missing actual delivery dates", "33 Negative weight glitches (-45.2 kg)", "66 Inconsistent carrier text strings"],
      "actionsTaken": ["Deduplicated on shipment_id", "Imputed delivery dates using scheduled lead times + status offsets", "Applied absolute value to weight records", "Standardized carrier names to official title case"]
    }
  },
  {
    "id": "marketing-conversion",
    "number": 4,
    "title": "Marketing Campaign & Customer Conversion Analytics",
    "shortTitle": "Marketing Analytics",
    "tagline": "Attribution economics, multi-stage funnel drop-off analysis, and CAC/ROAS optimization",
    "tech": ["SQL", "Python", "Power BI", "Funnel Analytics", "Unit Economics"],
    "resumeBullet1": "Evaluated campaign ROI, CAC, and channel performance; mapped the lead-to-customer conversion funnel in SQL and Python.",
    "resumeBullet2": "Built a Power BI dashboard covering leads, revenue, and customer segments to compare channel effectiveness.",
    "kpis": [
      { "label": "Total Marketing Spend", "value": "$186,500", "delta": "10 Campaigns", "sub": "6 Acquisition channels" },
      { "label": "Attributed Revenue", "value": "$1,142,000", "delta": "+28.5% YoY", "sub": "574 Closed-Won deals" },
      { "label": "Blended ROAS", "value": "6.12x", "delta": "Target > 4.0x", "sub": "Gross Return on Ad Spend" },
      { "label": "Blended CAC", "value": "$324.90", "delta": "-12% vs prior", "sub": "Cost per acquired customer" },
      { "label": "Funnel Conversion Rate", "value": "16.4%", "delta": "Lead to Closed-Won", "sub": "3,500 inbound prospects" }
    ],
    "categoryData": [
      { "name": "Email Marketing", "value": 1240.0, "secondary": 42.0 },
      { "name": "LinkedIn Ads", "value": 720.0, "secondary": 840.0 },
      { "name": "Organic Search (SEO)", "value": 580.0, "secondary": 110.0 },
      { "name": "Google Ads", "value": 410.0, "secondary": 380.0 },
      { "name": "Meta (Facebook/IG)", "value": 290.0, "secondary": 280.0 },
      { "name": "Influencer Partnerships", "value": -18.0, "secondary": 1571.0 }
    ],
    "timeData": [
      { "date": "Leads Entered", "value": 3500, "secondary": 100 },
      { "date": "MQL (Qualified)", "value": 2380, "secondary": 68 },
      { "date": "SQL (Sales Fit)", "value": 1380, "secondary": 39.4 },
      { "date": "Opportunities", "value": 910, "secondary": 26.0 },
      { "date": "Closed-Won Deals", "value": 574, "secondary": 16.4 }
    ],
    "segmentData": [
      { "name": "Enterprise ($24.5k avg deal)", "value": 58.4, "color": "#10B981" },
      { "name": "Mid-Market ($9.2k avg deal)", "value": 31.2, "color": "#3B82F6" },
      { "name": "SMB ($2.4k avg deal)", "value": 10.4, "color": "#F59E0B" }
    ],
    "sampleRecords": p4_clean_csv,
    "secondaryRecords": p4_channels_csv,
    "sqlFiles": [
      { "name": "schema.sql", "description": "MySQL DDL table schemas, indices on stage and campaign", "content": p4_schema },
      { "name": "data_analysis.sql", "description": "Channel CAC, ROAS, net ROI, and 6-stage funnel conversion ratios", "content": p4_analysis_sql },
      { "name": "advanced_queries.sql", "description": "Campaign ranking with DENSE_RANK() and monthly cumulative running revenue", "content": p4_adv_sql }
    ],
    "pythonFiles": [
      { "name": "data_cleaning.py", "description": "Channel name normalization, null deal value imputation, days-to-close checks", "content": p4_py_clean },
      { "name": "analysis.py", "description": "Full-funnel transition efficiencies and unit economic calculations", "content": p4_py_analysis }
    ],
    "daxMeasures": p4_dax,
    "insightsMd": p4_insights,
    "readmeMd": p4_readme,
    "streamlitCode": p4_streamlit,
    "cleaningSummary": {
      "rawRows": 3502,
      "cleanedRows": 3500,
      "issuesFound": ["2 Duplicate lead records", "70 Missing deal values in intermediate stages", "68 Lowercase and trailing space in channels ('linkedin ads  ')"],
      "actionsTaken": ["Deduplicated on lead_id", "Imputed 0.0 for non-closed stages", "Standardized and trimmed channel taxonomy"]
    }
  }
]

# Write out clean TypeScript file
with open(os.path.join(SRC_DATA_DIR, "portfolioData.ts"), "w", encoding="utf-8") as f:
    f.write("// Auto-generated portfolio dataset for Farjad Zeya's Data Analyst Suite\n\n")
    f.write("export const FARJAD_PROFILE = " + json.dumps(farjad_profile, indent=2) + ";\n\n")
    f.write("export const ROOT_PORTFOLIO_README = " + json.dumps(root_readme) + ";\n\n")
    f.write("export const PROJECTS_DATA = " + json.dumps(projects_data, indent=2) + ";\n\n")
    f.write("export type ProjectMeta = typeof PROJECTS_DATA[0];\n")

print("Exported /src/data/portfolioData.ts cleanly via JSON serialization!")
