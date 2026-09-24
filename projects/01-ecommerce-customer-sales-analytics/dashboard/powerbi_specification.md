# Power BI Dashboard Specification
## Project: E-Commerce Customer & Sales Analytics
**Author:** Farjad Zeya (Data Analyst)

---

### 1. Data Model & Architecture (Star Schema)
The Power BI semantic model is organized into a clean Star Schema:

- **Fact Table:** `Fact_Sales` (loaded from `ecommerce_transactions_cleaned.csv`)
- **Dimension Tables:**
  - `Dim_Customer` (Customer_ID, Customer_Name, Segment, Region)
  - `Dim_Product` (Category, Sub_Category, Product_Name, Unit_Price)
  - `Dim_Date` (Generated via DAX `CALENDARAUTO()`)
  - `Dim_RFM` (loaded from `ecommerce_customers_rfm.csv`)

#### Relationships:
1. `Dim_Customer[Customer_ID]` (1) ───< (Many) `Fact_Sales[Customer_ID]` (Single direction)
2. `Dim_Date[Date]` (1) ───< (Many) `Fact_Sales[Order_Date]` (Single direction)
3. `Dim_RFM[Customer_ID]` (1) ─── (1) `Dim_Customer[Customer_ID]` (Bi-directional for segment cross-filtering)

---

### 2. Core DAX Measures Table (`_Measures`)

#### Base Metrics
```dax
Total Revenue = SUM(Fact_Sales[sales_amount])

Total Profit = SUM(Fact_Sales[profit])

Profit Margin % = 
DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(Fact_Sales[order_id])

Total Units Sold = SUM(Fact_Sales[quantity])

Total Customers = DISTINCTCOUNT(Fact_Sales[customer_id])

Average Order Value (AOV) = 
DIVIDE([Total Revenue], [Total Orders], 0)
```

#### Time Intelligence & Growth
```dax
Revenue LY = 
CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))

Revenue YoY Growth % = 
DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], 0)

Revenue MoM % = 
VAR PrevMonth = CALCULATE([Total Revenue], DATEADD(Dim_Date[Date], -1, MONTH))
RETURN
DIVIDE([Total Revenue] - PrevMonth, PrevMonth, 0)
```

#### RFM & Segment Measures
```dax
Champions Revenue = 
CALCULATE([Total Revenue], Dim_RFM[customer_rfm_segment] = "Champions (High-Value)")

At-Risk Revenue Exposure = 
CALCULATE([Total Revenue], Dim_RFM[customer_rfm_segment] = "At-Risk Customers")
```

---

### 3. Dashboard Visual Layout (Canvas: 16:9 - 1920x1080)

- **Header Banner:**
  - Title: "E-Commerce Executive Sales & Customer Analytics"
  - Subtitle: "Portfolio Dashboard | Farjad Zeya | Data Analyst"
  - Slicers: Date Range (Relative Slider), Region (Dropdown), Segment (Buttons)

- **Row 1: KPI Cards**
  - Card 1: Total Revenue ($) with YoY comparison indicator
  - Card 2: Total Gross Profit ($) with target indicator
  - Card 3: Overall Profit Margin % (Conditional formatting: Green > 20%, Yellow 15-20%, Red < 15%)
  - Card 4: Total Orders & AOV ($)
  - Card 5: High-Value Customer Share %

- **Row 2: Trends & Breakdown**
  - Visual 1 (Line & Clustered Column Chart): Monthly Revenue (Bar) vs Profit Margin % (Line)
  - Visual 2 (Tree Map): Sales & Profit Margin by Category & Sub-Category
  - Visual 3 (Donut Chart): Revenue share by Customer Segment (Consumer vs Corporate vs Home Office)

- **Row 3: Customer Intelligence & Regional Matrix**
  - Visual 4 (Scatter Plot): RFM Matrix (Recency vs Monetary, bubble size = Frequency)
  - Visual 5 (Horizontal Bar Chart): Sales by Region with Profit Margin Data Labels
  - Visual 6 (Interactive Table): Top 10 Products with Sales, Profit, Units, and Discount %

---

### 4. Step-by-Step Power BI Reproduction Guide
1. Launch Power BI Desktop -> Click **Get Data** -> Select **Text/CSV**.
2. Select `data/processed/ecommerce_transactions_cleaned.csv` and click **Transform Data**.
3. Verify data types: `order_date` as Date, `sales_amount` and `profit` as Decimal Number.
4. Add Date Table using Modeling tab:
   `Dim_Date = CALENDAR(MIN(Fact_Sales[order_date]), MAX(Fact_Sales[order_date]))`
5. Create relationships in Model View as described in Section 1.
6. Create an empty Table named `_Measures` and paste the DAX formulas from `dax_measures.dax`.
7. Drag and drop visuals onto the report canvas following the layout guide.
