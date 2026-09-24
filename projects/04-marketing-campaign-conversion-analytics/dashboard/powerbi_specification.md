# Power BI Dashboard Specification
## Project: Marketing Campaign & Customer Conversion Analytics
**Author:** Farjad Zeya (Data Analyst)

---

### 1. Data Model
- **Fact Table:** `Fact_Leads`
- **Dimension Tables:** `Dim_Campaigns`, `Dim_Date`, `Dim_Segment`

---

### 2. Core DAX Measures (`_MarketingMeasures`)

```dax
Total Spend = SUM(Dim_Campaigns[budget_spend_usd])

Attributed Revenue = 
CALCULATE(SUM(Fact_Leads[deal_value_usd]), Fact_Leads[funnel_stage] = "Closed-Won")

Total Inbound Leads = COUNTROWS(Fact_Leads)

Closed-Won Customers = 
CALCULATE(COUNTROWS(Fact_Leads), Fact_Leads[funnel_stage] = "Closed-Won")

Overall Conversion Rate % = 
DIVIDE([Closed-Won Customers], [Total Inbound Leads], 0)

Customer Acquisition Cost (CAC) = 
DIVIDE([Total Spend], [Closed-Won Customers], 0)

Return on Ad Spend (ROAS) = 
DIVIDE([Attributed Revenue], [Total Spend], 0)

Net ROI % = 
DIVIDE([Attributed Revenue] - [Total Spend], [Total Spend], 0)
```

---

### 3. Dashboard Visual Layout (1920x1080)
- **Top Row:** Total Spend, Attributed Revenue, CAC, ROAS, Won Deals.
- **Visual 1 (Funnel Visual):** Lead -> MQL -> SQL -> Opportunity -> Closed-Won.
- **Visual 2 (Clustered Column):** Spend vs Revenue by Marketing Channel.
- **Visual 3 (Scatter):** CAC vs Conversion Rate (size = Deal Value).
- **Visual 4 (Table):** Campaign Performance Matrix with Budget Recommendations.
