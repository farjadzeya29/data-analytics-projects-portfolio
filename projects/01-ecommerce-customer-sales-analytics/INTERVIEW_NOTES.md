# Interview Preparation Notes: E-Commerce Customer & Sales Analytics
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
