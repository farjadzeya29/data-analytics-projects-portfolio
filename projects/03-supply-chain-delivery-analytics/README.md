# Supply Chain & Delivery Performance Analytics
[![SQL](https://img.shields.io/badge/SQL-MySQL%208.0-orange.svg)](https://www.mysql.com/)
[![Excel](https://img.shields.io/badge/Excel-Advanced%20MIS-green.svg)](https://office.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Author:** Farjad Zeya (Data Analyst)  
**Project Alignment:** Directly corresponds to Project #3 listed on Farjad Zeya's professional resume.

---

## 1. Project Overview
Evaluated **5,150 freight consignments** across 8 suppliers, 4 warehouse hubs, and multiple carriers to eliminate delivery delays and optimize freight expenditure.

*Dataset Note: Synthetic data created for portfolio and analytical demonstration purposes.*

---

## 2. Quick Start
```bash
git clone https://github.com/farjadzeya/supply-chain-delivery-analytics.git
cd supply-chain-delivery-analytics
pip install -r requirements.txt
python src/data_cleaning.py
python src/analysis.py
streamlit run dashboard/app.py
```

---

## 3. Key Findings
- **On-Time Delivery Rate (OTD):** 41.81%
- **Average Delivery Delay:** 2.92 days
- **Total Shipping Spend:** $2,715,307.36
- **Primary Bottleneck:** East Gateway (Kolkata) with 21.6% OTD
