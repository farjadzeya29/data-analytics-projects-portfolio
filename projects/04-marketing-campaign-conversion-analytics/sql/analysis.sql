-- Project 4: Analytical SQL Queries
USE marketing_analytics;

-- 1. Multi-Stage Conversion Funnel Summary
SELECT 
    COUNT(*) AS total_inbound_leads,
    SUM(is_mql) AS marketing_qualified_leads,
    ROUND((SUM(is_mql) / COUNT(*)) * 100, 2) AS lead_to_mql_pct,
    SUM(is_sql) AS sales_qualified_leads,
    ROUND((SUM(is_sql) / SUM(is_mql)) * 100, 2) AS mql_to_sql_pct,
    SUM(is_opportunity) AS sales_opportunities,
    ROUND((SUM(is_opportunity) / SUM(is_sql)) * 100, 2) AS sql_to_opp_pct,
    SUM(is_customer) AS closed_won_customers,
    ROUND((SUM(is_customer) / SUM(is_opportunity)) * 100, 2) AS opp_to_customer_pct,
    ROUND((SUM(is_customer) / COUNT(*)) * 100, 2) AS end_to_end_conversion_pct
FROM fact_leads;

-- 2. Channel Conversion Efficiency & Revenue Performance
SELECT 
    marketing_channel,
    COUNT(*) AS total_leads,
    SUM(is_customer) AS total_customers_acquired,
    ROUND((SUM(is_customer) / COUNT(*)) * 100, 2) AS conversion_rate_pct,
    ROUND(SUM(deal_value_usd), 2) AS total_pipeline_revenue,
    ROUND(AVG(CASE WHEN is_customer = 1 THEN deal_value_usd ELSE NULL END), 2) AS avg_deal_size_usd,
    ROUND(AVG(CASE WHEN is_customer = 1 THEN days_to_close ELSE NULL END), 1) AS avg_sales_cycle_days
FROM fact_leads
GROUP BY marketing_channel
ORDER BY total_pipeline_revenue DESC;
