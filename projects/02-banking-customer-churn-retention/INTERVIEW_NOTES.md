# Interview Preparation Notes: Banking Customer Churn & Retention
**Candidate:** Farjad Zeya  
**Role Target:** Data Analyst / Retention Analyst  
**Tech Stack:** SQL (MySQL 8.0), Python (pandas, NumPy, Matplotlib), Power BI, Streamlit

---

## 1. 60-Second Project Pitch
"In this project, I evaluated churn dynamics across 5,250 retail banking customers holding $444,864,722.76 in deposits to protect bank capital from attrition. Using MySQL and Python, I cleaned raw account files, corrected negative age anomalies, and evaluated churn across tenure, balance, activity, and product count. My analysis revealed an overall churn rate of 27.30% ($134,810,610.14 in exited deposits). Crucially, I uncovered the 'Multi-Product Paradox': customers with 2 products experienced the best retention (18.3% churn), whereas churn spiked above 73.2% for clients with 3 or more products. Furthermore, inactive digital members churned at 34.3% compared to 20.7% for active users. I built an interactive Power BI and Streamlit retention dashboard to flag high-balance depositors before they close their accounts."

---

## 2. Business Problem
Retail banks suffer severe margin loss when established customers withdraw deposits. Management needed to know which demographic and behavioral cohorts carry the highest attrition risk.

---

## 3. Dataset Architecture
- **Dataset:** Synthetic dataset created for portfolio and analytical demonstration purposes.
- **Scale:** 5,250 customer records.
- **Attributes:** `customer_id`, `geography`, `gender`, `age`, `tenure`, `credit_score`, `balance`, `num_of_products`, `has_cr_card`, `is_active_member`, `estimated_salary`, `exited`, `risk_tier`.

---

## 4. Five Key Insights (Directly Calculated)
1. **Overall Churn Rate:** **27.30%** (1,433 exited accounts).
2. **Deposit Exposure:** **$134,810,610.14** in deposits lost from churned accounts.
3. **Multi-Product Paradox:** 2 products is optimal (**18.3%** churn); 3-4 products surges to **73.2% - 76.2%**.
4. **Active Member Advantage:** Active members churn at **20.7%** vs **34.3%** for inactive members.
5. **German Exposure:** Germany accounts had an attrition rate of **38.1%**, the highest across the bank.

---

## 5. Five Likely Interviewer Questions & Answers
1. **Q: Why would customers with 3 or 4 products churn at a higher rate than customers with 1 or 2?**  
   *A: In retail banking, customers with 3-4 products are often sold disparate legacy accounts with multiple maintenance fees, overlapping credit lines, or confusing statements without a unified relationship manager. When service friction occurs, they close all accounts.*
2. **Q: How did you classify customer risk tiers?**  
   *A: I combined high balance (>€100k), inactive status (`is_active_member = 0`), and product hazard weights into a composite logistic probability score (>60% High Risk, 30-60% Medium, <30% Low).*
3. **Q: Did credit score correlate strongly with churn?**  
   *A: No, credit score showed minimal correlation with attrition; churn was predominantly driven by digital activity and product complexity.*
4. **Q: How would you operationalize this in a real bank?**  
   *A: I would schedule a daily SQL batch job exporting high-balance accounts crossing the risk threshold directly into the CRM for priority outreach.*
5. **Q: How did your work at CK Infrastructure Ltd help you approach this project?**  
   *A: At CK Infrastructure Ltd, I monitor consumption anomalies and equipment meter flags. The same principle applies here: identifying early warning signs before critical operational or financial loss occurs.*
