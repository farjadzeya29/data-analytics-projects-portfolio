-- ========================================================================
-- Project 1: E-Commerce Customer & Sales Analytics - Core Business Queries
-- Author: Farjad Zeya (Data Analyst)
-- Dialect: MySQL 8.0+
-- ========================================================================

USE ecommerce_analytics;

-- ------------------------------------------------------------------------
-- QUERY 1: Executive KPI Overview
-- Business Question: What is the overall revenue, gross profit, overall profit
-- margin, total units sold, distinct orders and total unique customers?
-- ------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales_amount) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM fact_ecommerce_sales;

-- ------------------------------------------------------------------------
-- QUERY 2: Sales & Profitability Breakdown by Product Category
-- Business Question: Which product categories generate the bulk of revenue
-- and which categories are underperforming on profit margins?
-- ------------------------------------------------------------------------
SELECT 
    category,
    COUNT(DISTINCT order_id) AS order_volume,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(sales_amount), 2) AS category_revenue,
    ROUND(SUM(profit), 2) AS category_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS margin_percentage,
    ROUND(AVG(discount) * 100, 2) AS average_discount_pct
FROM fact_ecommerce_sales
GROUP BY category
ORDER BY category_revenue DESC;

-- ------------------------------------------------------------------------
-- QUERY 3: Regional Sales & Profit Performance Analysis
-- Business Question: How do sales and margins vary across geographic regions,
-- and are certain regions discounting excessively?
-- ------------------------------------------------------------------------
SELECT 
    region,
    COUNT(DISTINCT customer_id) AS active_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales_amount) / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM fact_ecommerce_sales
GROUP BY region
ORDER BY total_sales DESC;

-- ------------------------------------------------------------------------
-- QUERY 4: Monthly Revenue & Profit Trend Analysis (Seasonality)
-- Business Question: What is the monthly trajectory of sales and profitability
-- over time?
-- ------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS order_month,
    COUNT(DISTINCT order_id) AS monthly_orders,
    ROUND(SUM(sales_amount), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS monthly_margin_pct
FROM fact_ecommerce_sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month ASC;

-- ------------------------------------------------------------------------
-- QUERY 5: Top 10 High-Revenue Generating Products
-- Business Question: Which top 10 specific products drive the highest revenue,
-- and are they sustainably profitable?
-- ------------------------------------------------------------------------
SELECT 
    product_name,
    category,
    sub_category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct
FROM fact_ecommerce_sales
GROUP BY product_name, category, sub_category
ORDER BY total_revenue DESC
LIMIT 10;
