# Power BI Dashboard Specification
## Project: Banking Customer Churn & Retention Analysis
**Author:** Farjad Zeya (Data Analyst)

---

### 1. Data Model & Architecture
- **Single Source / Fact Table:** `Fact_BankCustomers` (from `banking_churn_cleaned.csv`)
- **Dimension Parameter Tables:**
  - `Dim_AgeBuckets` (<30, 30-44, 45-59, 60+)
  - `Dim_TenureCohorts` (0-1 yr, 2-4 yrs, 5-7 yrs, 8+ yrs)
  - `Dim_Geography` (Country code, Country Name)

---

### 2. Core DAX Measures Table (`_RetentionMeasures`)

```dax
Total Customers = COUNTROWS(Fact_BankCustomers)

Churned Customers = 
CALCULATE(COUNTROWS(Fact_BankCustomers), Fact_BankCustomers[churn] = 1)

Retained Customers = 
CALCULATE(COUNTROWS(Fact_BankCustomers), Fact_BankCustomers[churn] = 0)

Overall Churn Rate % = 
DIVIDE([Churned Customers], [Total Customers], 0)

Total Balance at Risk ($) = 
CALCULATE(SUM(Fact_BankCustomers[account_balance]), Fact_BankCustomers[churn] = 1)

Active Member Churn % = 
CALCULATE([Overall Churn Rate %], Fact_BankCustomers[is_active_member] = 1)

Inactive Member Churn % = 
CALCULATE([Overall Churn Rate %], Fact_BankCustomers[is_active_member] = 0)

High Risk Customer Count = 
CALCULATE(COUNTROWS(Fact_BankCustomers), Fact_BankCustomers[retention_risk_tier] = "High Risk")

High Risk Balance Exposure = 
CALCULATE(SUM(Fact_BankCustomers[account_balance]), Fact_BankCustomers[retention_risk_tier] = "High Risk")
```

---

### 3. Dashboard Visual Layout (1920x1080)
- **Top Ribbon:**
  - KPI 1: Overall Churn Rate % (Gauge with 15% threshold target)
  - KPI 2: Total Churned Accounts
  - KPI 3: Total Capital at Risk ($)
  - KPI 4: Inactive vs Active Churn Spread (e.g. 29.4% vs 14.1%)
  - KPI 5: High Risk Accounts Flagged for Action

- **Left Column: Demographic & Geographic Drivers**
  - Bar Chart: Churn Rate by Geography (Germany vs France vs Spain)
  - Clustered Bar: Churn Rate by Age Bucket & Gender

- **Middle Column: Behavioral & Financial Drivers**
  - Column Chart: Churn Rate by Number of Products (1, 2, 3, 4)
  - Scatter / Distribution: Account Balance vs Credit Score colored by Churn Status

- **Right Column: Actionable Retention Worklist**
  - Priority Table: Top 25 High-Balance Inactive Customers in High Risk Tier with Customer ID, Geography, Balance, and Products.
