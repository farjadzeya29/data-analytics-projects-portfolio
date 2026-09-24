-- ========================================================================
-- Project 1: E-Commerce Customer & Sales Analytics - Advanced SQL Queries
-- Author: Farjad Zeya (Data Analyst)
-- Features: CTEs, Window Functions (NTILE, LAG, SUM OVER), RFM Scoring
-- ========================================================================

USE ecommerce_analytics;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 1: Month-over-Month (MoM) Sales Growth Using LAG()
-- Business Question: What is the month-over-month sales growth rate and
-- profit variance?
-- ------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
        ROUND(SUM(sales_amount), 2) AS current_month_sales,
        ROUND(SUM(profit), 2) AS current_month_profit
    FROM fact_ecommerce_sales
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    sales_month,
    current_month_sales,
    LAG(current_month_sales, 1) OVER (ORDER BY sales_month) AS previous_month_sales,
    ROUND(
        ((current_month_sales - LAG(current_month_sales, 1) OVER (ORDER BY sales_month)) 
        / LAG(current_month_sales, 1) OVER (ORDER BY sales_month)) * 100, 
        2
    ) AS mom_sales_growth_pct,
    current_month_profit,
    LAG(current_month_profit, 1) OVER (ORDER BY sales_month) AS previous_month_profit
FROM monthly_metrics;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 2: Full RFM Segmentation using CTEs and NTILE(5)
-- Business Question: Calculate Recency, Frequency, and Monetary scores
-- for each customer and segment into actionable tiers (Champions, Loyal, At Risk).
-- ------------------------------------------------------------------------
WITH customer_aggregates AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        MAX(order_date) AS last_order_date,
        DATEDIFF('2025-12-31', MAX(order_date)) AS recency_days,
        COUNT(DISTINCT order_id) AS frequency_orders,
        ROUND(SUM(sales_amount), 2) AS monetary_spend
    FROM fact_ecommerce_sales
    GROUP BY customer_id, customer_name, segment, region
),
rfm_ranked AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        recency_days,
        frequency_orders,
        monetary_spend,
        -- Higher recency days means longer absence, so invert NTILE
        6 - NTILE(5) OVER (ORDER BY recency_days ASC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency_orders ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_spend ASC) AS m_score
    FROM customer_aggregates
)
SELECT 
    customer_id,
    customer_name,
    segment,
    region,
    recency_days,
    frequency_orders,
    monetary_spend,
    r_score,
    f_score,
    m_score,
    CONCAT(r_score, f_score, m_score) AS rfm_code,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions (High-Value)'
        WHEN f_score >= 3 AND m_score >= 3 AND r_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Promising New Customers'
        WHEN r_score <= 2 AND (f_score >= 3 OR m_score >= 3) THEN 'At-Risk High Spenders'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost / Dormant Customers'
        ELSE 'Needs Nurturing'
    END AS customer_rfm_segment
FROM rfm_ranked
ORDER BY monetary_spend DESC;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 3: Pareto Principle (80/20 Rule) Verification
-- Business Question: What percentage of cumulative revenue is driven
-- by top customer cohorts?
-- ------------------------------------------------------------------------
WITH customer_spend AS (
    SELECT 
        customer_id,
        customer_name,
        ROUND(SUM(sales_amount), 2) AS total_spend
    FROM fact_ecommerce_sales
    GROUP BY customer_id, customer_name
),
cumulative_spend AS (
    SELECT 
        customer_id,
        customer_name,
        total_spend,
        ROW_NUMBER() OVER (ORDER BY total_spend DESC) AS customer_rank,
        COUNT(*) OVER () AS total_customer_count,
        SUM(total_spend) OVER (ORDER BY total_spend DESC) AS cumulative_sales,
        SUM(total_spend) OVER () AS grand_total_sales
    FROM customer_spend
)
SELECT 
    customer_rank,
    customer_name,
    total_spend,
    ROUND((customer_rank / total_customer_count) * 100, 2) AS pct_of_customer_base,
    ROUND((cumulative_sales / grand_total_sales) * 100, 2) AS cumulative_sales_pct
FROM cumulative_spend
WHERE (customer_rank / total_customer_count) <= 0.35 -- Inspect top 35%
ORDER BY customer_rank ASC;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 4: Repeat Customer Purchase Rate & Velocity
-- Business Question: How many customers made repeat purchases and what is
-- the repeat order proportion by customer segment?
-- ------------------------------------------------------------------------
WITH order_counts AS (
    SELECT 
        customer_id,
        segment,
        COUNT(DISTINCT order_id) AS orders_placed
    FROM fact_ecommerce_sales
    GROUP BY customer_id, segment
)
SELECT 
    segment,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN orders_placed > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND((SUM(CASE WHEN orders_placed > 1 THEN 1 ELSE 0 END) / COUNT(customer_id)) * 100, 2) AS repeat_customer_rate_pct,
    ROUND(AVG(orders_placed), 2) AS avg_orders_per_customer
FROM order_counts
GROUP BY segment;
