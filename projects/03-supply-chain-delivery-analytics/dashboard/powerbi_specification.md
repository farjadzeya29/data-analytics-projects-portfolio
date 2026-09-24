# Power BI Dashboard Specification
## Project: Supply Chain & Delivery Performance Analytics
**Author:** Farjad Zeya (Data Analyst)

---

### 1. Data Model
- **Fact Table:** `Fact_Shipments`
- **Dimension Tables:** `Dim_Suppliers`, `Dim_Warehouses`, `Dim_Date`, `Dim_Routes`

---

### 2. Core DAX Measures (`_SupplyChainMeasures`)

```dax
Total Shipments = COUNTROWS(Fact_Shipments)

On-Time Shipments = 
CALCULATE(COUNTROWS(Fact_Shipments), Fact_Shipments[delivery_status] IN {"On-Time", "Early"})

Delayed Shipments = 
CALCULATE(COUNTROWS(Fact_Shipments), Fact_Shipments[delivery_status] = "Delayed")

On-Time Delivery % (OTD) = 
DIVIDE([On-Time Shipments], [Total Shipments], 0)

Average Delay Days = 
CALCULATE(AVERAGE(Fact_Shipments[delay_days]), Fact_Shipments[delay_days] > 0)

Total Freight Cost ($) = 
SUM(Fact_Shipments[shipping_cost_usd])

Freight Cost per KG = 
DIVIDE([Total Freight Cost ($)], SUM(Fact_Shipments[weight_kg]), 0)

Defect / Damage Rate % = 
DIVIDE(SUM(Fact_Shipments[damage_reported]), [Total Shipments], 0)
```

---

### 3. Dashboard Visual Layout (1920x1080)
- **Top Metrics:** OTD % (Target Gauge 85%), Avg Delay Days, Total Shipping Spend, Cost / KG, Damage Rate.
- **Visual 1 (Matrix):** Bottleneck Route Heatmap (Origin Warehouse vs Destination Region).
- **Visual 2 (Scatter):** Supplier Scorecard (OTD % vs Defect Rate, size = Volume).
- **Visual 3 (Clustered Bar):** Carrier Performance (BlueDart vs Delhivery vs FedEx vs DTDC).
- **Visual 4 (Table):** Delayed Shipments Exception Log with Days Delayed and Delay Penalty.
