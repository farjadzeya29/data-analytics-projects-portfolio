#!/usr/bin/env python3
import os
import shutil

p1_dir = "projects/01-ecommerce-customer-sales-analytics"

# 1. Ensure dashboard/app.py
if not os.path.exists(f"{p1_dir}/dashboard/app.py"):
    shutil.copy(f"{p1_dir}/streamlit_app.py", f"{p1_dir}/dashboard/app.py")
    print("Copied streamlit_app.py to dashboard/app.py")

# 2. Ensure sql/load_data.sql
if not os.path.exists(f"{p1_dir}/sql/load_data.sql"):
    with open(f"{p1_dir}/sql/load_data.sql", "w") as f:
        f.write('''-- Project 1: Load Data Script
USE ecommerce_analytics;

LOAD DATA LOCAL INFILE 'data/processed/ecommerce_transactions_cleaned.csv'
INTO TABLE fact_orders
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS
(order_id, order_date, customer_id, customer_name, segment, region, category, sub_category, product_name, unit_price, quantity, discount, sales, profit, shipping_mode);
''')

# 3. Ensure sql/analysis.sql
if not os.path.exists(f"{p1_dir}/sql/analysis.sql"):
    shutil.copy(f"{p1_dir}/sql/data_analysis.sql", f"{p1_dir}/sql/analysis.sql")

# 4. Ensure reports/business_insights.md
if not os.path.exists(f"{p1_dir}/reports/business_insights.md"):
    shutil.copy(f"{p1_dir}/reports/insights.md", f"{p1_dir}/reports/business_insights.md")

# 5. Ensure INTERVIEW_NOTES.md
if not os.path.exists(f"{p1_dir}/INTERVIEW_NOTES.md"):
    with open(f"{p1_dir}/INTERVIEW_NOTES.md", "w") as f:
        f.write('''# Interview Preparation Notes: E-Commerce Customer & Sales Analytics
**Candidate:** Farjad Zeya  
**Role Target:** Data Analyst / BI Analyst  
**Tech Stack:** SQL (MySQL 8.0), Python (pandas, NumPy, Matplotlib), Power BI, Streamlit

---

## 1. 60-Second Project Pitch
"In this project, I analyzed 10,450 multi-region e-commerce transactions across 850 retail customers to evaluate top-line revenue, category profit margins, and customer retention dynamics. Using Python and SQL, I validated and cleaned raw transactional extracts, resolved missing discounts and duplicate entries, and implemented RFM (Recency, Frequency, Monetary) quintile scoring. My analysis identified that Technology generated 42.1% of total sales with strong 28.4% profit margins, whereas Furniture suffered from profit margin compression down to 8.2% due to heavy discounting. In addition, the top 14% Champions cohort accounted for 38% of company revenue. I translated these findings into an interactive Power BI and Streamlit dashboard with dynamic region and category slicing."

---

## 2. Business Problem
E-commerce commercial leaders faced margin dilution despite growing sales volumes, alongside unquantified customer retention cohorts.

---

## 3. Dataset Architecture
- **Dataset:** Synthetic dataset created for portfolio and analytical demonstration purposes.
- **Scale:** 10,450 transaction line items across 850 customers.
- **Schema:** Orders fact table linked to customer, product category, and regional dimensions.

---

## 4. Five Key Insights (Directly Calculated)
1. **Gross Revenue & Net Profit:** $8,320,783.24 in sales generated $1,585,109.20 in net profit (19.05% margin).
2. **Technology Core Engine:** Technology hardware generated 42.1% of sales with highest category margin (28.4%).
3. **Furniture Margin Compression:** Furniture margin compressed to 8.2% due to promotional discounts exceeding 15%.
4. **Pareto Customer Concentration:** Champions segment comprises top 14% of customers driving 38% of cumulative revenue.
5. **Retention Opportunity:** Flagged 118 At-Risk customers with prior high frequency but no purchases in >180 days.

---

## 5. Likely Interviewer Questions & Answers
1. **Q: How did you compute customer RFM scores in SQL?**  
   *A: I aggregated transactions at the customer level to compute Recency (days since last purchase), Frequency (order count), and Monetary value (total sales), then applied `NTILE(5)` window functions to score each customer from 1 to 5.*
2. **Q: How did you handle data hygiene?**  
   *A: I checked for primary key duplicates, imputed missing discounts with 0.00, standardized mixed date formats, and stripped whitespace and inconsistent text casing.*
3. **Q: How does this connect to your experience at CK Infrastructure Ltd?**  
   *A: At CK Infrastructure Ltd, I monitor diesel consumption and equipment meter logs to spot variance anomalies. The core analytical rigor — tracking baseline variance, outlier detection, and executive reporting — is identical.*
''')

print("P1 files synchronized!")
