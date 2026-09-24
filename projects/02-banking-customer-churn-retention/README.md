# Banking Customer Churn & Retention Analysis
[![SQL](https://img.shields.io/badge/SQL-MySQL%208.0-orange.svg)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Author:** Farjad Zeya (Data Analyst)  
**Project Alignment:** Directly corresponds to Project #2 listed on Farjad Zeya's professional resume.

---

## 1. Project Overview
Analyzed **5,250 retail banking accounts** across France, Germany, and Spain to quantify churn risk factors, evaluate deposit attrition, and identify retention levers.

*Dataset Note: Synthetic data created for portfolio and analytical demonstration purposes.*

---

## 2. Quick Execution
```bash
git clone https://github.com/farjadzeya/banking-customer-churn-retention.git
cd banking-customer-churn-retention
pip install -r requirements.txt
python src/data_cleaning.py
python src/analysis.py
streamlit run dashboard/app.py
```

---

## 3. Key Findings
- **Overall Churn Rate:** 27.30% (1,433 of 5,250 accounts)
- **Deposits at Risk:** $134,810,610.14
- **Optimal Product Holding:** 2 products (18.3% churn) vs 3 products (73.2% churn)
- **Digital Engagement:** Inactive members churn at 34.3% vs 20.7% for active members
