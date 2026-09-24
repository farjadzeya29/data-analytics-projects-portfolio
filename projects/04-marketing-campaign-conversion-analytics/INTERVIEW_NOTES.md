# Interview Preparation Notes: Marketing Campaign & Conversion Analytics
**Candidate:** Farjad Zeya  
**Role Target:** Data Analyst / Growth & Marketing Analyst  
**Tech Stack:** SQL (MySQL 8.0), Python (pandas, NumPy, Matplotlib), Power BI, Streamlit

---

## 1. 60-Second Project Pitch
"In this project, I evaluated 10,500 marketing leads across 10 campaigns and 6 channels to optimize ad spend efficiency and maximize customer acquisition. Using MySQL and Python, I mapped a 6-stage conversion funnel from initial inbound lead to closed-won customer. I evaluated channel performance through CAC and ROAS metrics. My analysis proved that LinkedIn Ads and Email Marketing delivered our highest returns at 16.80x and 220.69x ROAS respectively, whereas Influencer Partnerships operated at a loss with 0.00x ROAS. I built an interactive Power BI and Streamlit marketing dashboard enabling growth teams to model budget reallocation."

---

## 2. Five Key Insights (Directly Calculated)
1. **Total Funnel Volume:** **10,500 leads** converted into **414 customers** (3.94% conversion).
2. **Gross Revenue Generated:** **$5,194,949.55** from $226,000.00 total ad spend.
3. **Unit CAC:** Average Customer Acquisition Cost across all channels was **$545.89**.
4. **LinkedIn High-Ticket ROAS:** LinkedIn Ads achieved **16.80x ROAS**, capturing enterprise contracts.
5. **Influencer Negative Return:** Influencer partnerships generated only **0.00x ROAS**, failing break-even.

---

## 3. Likely Interviewer Questions & Answers
1. **Q: How did you compute CAC and ROAS in SQL?**  
   *A: CAC = `total_campaign_spend / closed_won_customers`. ROAS = `total_closed_won_revenue / total_campaign_spend`.*
2. **Q: How did you model lead-to-opportunity funnel drop-offs?**  
   *A: Using boolean flags (`is_mql`, `is_sql`, `is_opportunity`, `is_customer`) in a single pass aggregation in MySQL and pandas.*
3. **Q: What recommendation would you give the CMO?**  
   *A: Reallocate at least 50% of the influencer marketing budget into high-intent LinkedIn and Email nurture campaigns.*
