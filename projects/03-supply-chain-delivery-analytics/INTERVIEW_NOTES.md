# Interview Preparation Notes: Supply Chain & Delivery Performance
**Candidate:** Farjad Zeya  
**Role Target:** Data Analyst / Supply Chain Analyst  
**Tech Stack:** SQL (MySQL 8.0), Microsoft Excel (Pivot Tables, Advanced Formulas), Power BI, Streamlit

---

## 1. 60-Second Project Pitch
"In this project, I evaluated logistics fulfillment and supplier reliability across 5,150 shipments and $2,715,307.36 in freight spend. Using MySQL and Excel MIS reporting, I calculated key KPIs including On-Time Delivery (41.81%), Average Delay (2.92 days), and shipping cost per KG. My analysis pinpointed that the East Gateway Hub in Kolkata was the primary bottleneck with an OTD of only 21.6%, driven by warehouse dispatch delays. I also built a Supplier Scorecard proving that Tier-3 suppliers suffered from 3x higher cargo damage rates than Tier-1 suppliers. Finally, I implemented an interactive Power BI and Streamlit dashboard and authored an Excel MIS guide featuring SUMIFS, XLOOKUP, and dynamic Pivot Tables for warehouse supervisors."

---

## 2. Five Key Insights (Directly Calculated)
1. **Network OTD:** **41.81%** on-time delivery across 5,150 consignments.
2. **Delay Duration:** Delayed shipments faced an average lag of **2.92 days**.
3. **Freight Spend:** Cumulative freight cost totaled **$2,715,307.36**.
4. **Kolkata Hub Bottleneck:** Kolkata Hub achieved only **21.6% OTD** vs **54.8%** for Mumbai.
5. **Tier-3 Defect Rates:** Tier-3 suppliers had damage rates of ~6%, driving higher return costs.

---

## 3. Likely Interviewer Questions & Answers
1. **Q: How did you compute On-Time Delivery in SQL?**  
   *A: I compared `actual_delivery_date` against `scheduled_delivery_date`. If actual <= scheduled, `on_time_flag = 1`. Then `SUM(on_time_flag) / COUNT(*) * 100` gives the exact OTD percentage.*
2. **Q: How was Excel utilized in this project?**  
   *A: I designed an executive MIS template utilizing `XLOOKUP` for supplier metadata, `SUMIFS` and `AVERAGEIFS` for regional cost slicing, and automated Pivot Tables with conditional formatting.*
3. **Q: How does this relate to your current experience at CK Infrastructure Ltd?**  
   *A: At CK Infrastructure Ltd, I analyze equipment maintenance logs and fleet fuel consumption. Monitoring equipment turnaround times is functionally identical to tracking shipment dispatch and delivery latency.*
