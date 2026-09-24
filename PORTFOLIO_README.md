# Farjad Zeya — Data Analyst Portfolio
**Location:** Hazaribagh, Jharkhand, India | **Email:** farjadzeya1234@gmail.com | **Phone:** +91 6204812301  
**GitHub Portfolio Repositories:** 4 Production-Ready Analytics Projects  
**Core Technologies:** SQL (MySQL, PostgreSQL), Python (pandas, NumPy, Matplotlib, Seaborn), Power BI (DAX, Star Schemas, Power Query), Advanced Microsoft Excel (Pivot Tables, XLOOKUP, MIS Reporting), Streamlit

---

## 📌 Portfolio Overview
This portfolio contains **four complete, production-grade, reproducible data analytics projects** aligned directly with the professional experience and projects documented in **Farjad Zeya's Resume**. 

Each project is architected as an independent, standalone GitHub repository containing raw and cleaned datasets, data cleaning scripts, analytical engines, production-ready SQL scripts, interactive Streamlit cockpits, DAX measure specifications, executive business insight reports, and structured interview preparation guides.

*Dataset Note: All datasets in this portfolio are realistic synthetic data generated specifically for portfolio and analytical demonstration purposes.*

---

## 📂 The Four Projects

### 1. [E-Commerce Customer & Sales Analytics](./projects/01-ecommerce-customer-sales-analytics)
- **Tech Stack:** SQL (MySQL 8.0), Python (pandas, NumPy, Matplotlib), Power BI, Streamlit
- **Scale:** 10,450 transactions across 850 retail customer accounts
- **Core Scope:** Multi-region sales and profit margin analysis, product category profit erosion, RFM (Recency, Frequency, Monetary) quintile customer segmentation, Pareto revenue analysis, interactive Streamlit/Power BI dashboard.
- **Key Empirical Results:**
  - Total Gross Revenue: **$8,320,783.24** | Net Profit: **$1,585,109.20** | Profit Margin: **19.05%** | AOV: **$796.25**
  - **Category Margins:** Technology delivered healthy 28.4% margins, while Furniture was compressed to 8.2% due to discounts >15%.
  - **RFM Pareto Effect:** Top 14.1% of customers (Champions cohort) generated 38.2% of total cumulative revenue.
- **Artifacts:** `src/data_cleaning.py`, `src/analysis.py`, `src/visualization.py`, `sql/schema.sql`, `sql/analysis.sql`, `dashboard/app.py`, `reports/business_insights.md`, `INTERVIEW_NOTES.md`.

---

### 2. [Banking Customer Churn & Retention Analysis](./projects/02-banking-customer-churn-retention)
- **Tech Stack:** SQL (MySQL 8.0), Python (pandas, NumPy, Matplotlib), Power BI, Streamlit
- **Scale:** 5,250 retail banking accounts across France, Germany, and Spain ($444.8M deposit base)
- **Core Scope:** Baseline attrition calculation, tenure hazard rates, account balance exposure, digital activity correlation, the "Multi-Product Paradox", and an interactive churn monitoring cockpit.
- **Key Empirical Results:**
  - Overall Churn Rate: **27.30%** (1,433 exited accounts) resulting in **$134,810,610.14** in churned deposits.
  - **The Multi-Product Paradox:** Customers holding 2 products demonstrated the lowest churn (18.3%), whereas customers cross-sold 3 products (73.2% churn) and 4 products (76.2% churn) experienced severe attrition.
  - **Digital Inactivity:** Inactive members churned at 34.3% vs. 20.7% for active members.
- **Artifacts:** `src/data_cleaning.py`, `src/analysis.py`, `src/visualization.py`, `sql/schema.sql`, `sql/analysis.sql`, `dashboard/app.py`, `reports/business_insights.md`, `INTERVIEW_NOTES.md`.

---

### 3. [Supply Chain & Delivery Performance Analytics](./projects/03-supply-chain-delivery-analytics)
- **Tech Stack:** SQL (MySQL 8.0), Microsoft Excel (Pivot Tables, SUMIFS, XLOOKUP, MIS Reporting), Power BI, Streamlit
- **Scale:** 5,150 freight shipments across 8 suppliers and 4 regional warehouse hubs ($2.71M spend)
- **Core Scope:** On-Time Delivery (OTD %) benchmarks, delivery delay distributions, warehouse dispatch bottlenecks, supplier tier scorecard, carrier rate analysis, and Excel MIS operational guide.
- **Key Empirical Results:**
  - Network On-Time Delivery (OTD): **41.81%** | Delayed Consignments: **2,997** | Average Delay Duration: **2.92 days**
  - **Primary Bottleneck:** East Gateway Hub (Kolkata) registered only 21.6% OTD due to 2.4-day average warehouse dispatch latency, compared to 54.8% at West Port (Mumbai).
  - **Supplier Quality:** Tier-3 suppliers exhibited a 5.8% cargo defect/damage rate compared to <1.5% for Tier-1 suppliers.
- **Artifacts:** `src/data_cleaning.py`, `src/analysis.py`, `src/visualization.py`, `sql/schema.sql`, `sql/analysis.sql`, `dashboard/app.py`, `reports/excel_analysis_guide.md`, `reports/business_insights.md`, `INTERVIEW_NOTES.md`.

---

### 4. [Marketing Campaign & Customer Conversion Analytics](./projects/04-marketing-campaign-conversion-analytics)
- **Tech Stack:** SQL (MySQL 8.0), Python (pandas, NumPy, Matplotlib), Power BI, Streamlit
- **Scale:** 10,500 inbound marketing leads across 10 campaigns and 6 channels ($226k spend, $5.19M pipeline)
- **Core Scope:** End-to-end 5-stage conversion funnel (Lead -> MQL -> SQL -> Opportunity -> Closed Won), Customer Acquisition Cost (CAC), Return on Ad Spend (ROAS), and sales cycle velocity.
- **Key Empirical Results:**
  - Total Leads: **10,500** | Closed Won: **414** (3.94% end-to-end conversion) | Pipeline Revenue: **$5,194,949.55**
  - Blended CAC: **$545.89** | Overall ROAS: **22.99x**
  - **Top Performing Channels:** Email Marketing (220.7x ROAS) and LinkedIn Ads (16.8x ROAS, driving $24.5k enterprise contracts).
  - **Underperforming Channel:** Influencer Partnerships operated at negative ROAS (0.00x), failing to close enterprise deals.
- **Artifacts:** `src/data_cleaning.py`, `src/analysis.py`, `src/visualization.py`, `sql/schema.sql`, `sql/analysis.sql`, `dashboard/app.py`, `reports/business_insights.md`, `INTERVIEW_NOTES.md`.

---

## 🛠️ Repository Standards & Structure
Every project repository adheres to strict production engineering conventions:
```
project-name/
│
├── README.md                      # Comprehensive project documentation
├── requirements.txt               # Pinned Python package dependencies
├── .gitignore                     # Git exclusions
├── LICENSE                        # MIT License
├── INTERVIEW_NOTES.md             # 13-section technical interview prep guide
│
├── data/
│   ├── raw/                       # Raw datasets with deliberate edge cases & anomalies
│   └── processed/                 # Fully sanitized, validated datasets
│
├── src/
│   ├── data_cleaning.py           # Automated data validation & cleaning pipeline
│   ├── analysis.py                # Pure analytical & statistical calculations
│   └── visualization.py           # Publication-ready matplotlib chart generation
│
├── sql/
│   ├── schema.sql                 # DDL schema definition with indexing
│   ├── load_data.sql              # Bulk data ingestion script
│   └── analysis.sql               # Complex SQL queries (CTEs, Window Functions, Group By)
│
├── notebooks/
│   └── exploratory_analysis.ipynb # Interactive Jupyter exploratory notebook
│
├── dashboard/
│   ├── app.py                     # Interactive Streamlit application
│   ├── powerbi_specification.md   # Data model, visual layout, and theme specs
│   └── dax_measures.dax           # Production DAX formulas
│
└── reports/
    └── business_insights.md       # Executive findings with real computed numbers
```

---

## 🚀 Interactive Web Application
In addition to the standalone project repositories, this workspace includes an interactive, browser-based Data Analyst Portfolio Web Application featuring:
- **Interactive Dashboards** with live multi-dimensional slicing and dynamic metric recalculation
- **In-Browser SQL Query Studio** with syntax-highlighted sample queries and results
- **Python Pipeline Viewer** displaying data cleaning logic and statistical engines
- **Power BI & DAX Blueprints** with full formula specifications
- **Data Quality & Hygiene Audits** showing raw vs. cleaned validation steps
- **Interactive Git Repository File Explorer** allowing direct inspection of all source code files
- **Complete Resume Modal** reflecting Farjad Zeya's education, experience, and certifications
