# E-Commerce Customer & Sales Analytics
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
   source .venv/bin/activate # On Windows: .venv\Scripts\activate
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
