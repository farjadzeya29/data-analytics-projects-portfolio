-- ========================================================================
-- Project 4: Marketing Campaign Analytics - Core Analytical SQL Queries
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

USE marketing_analytics;

-- ------------------------------------------------------------------------
-- QUERY 1: Channel Performance Scorecard (Spend, Revenue, CAC, ROAS, ROI)
-- Business Question: How do marketing channels compare on Customer Acquisition
-- Cost (CAC), Return on Ad Spend (ROAS), and net Return on Investment (ROI)?
-- ------------------------------------------------------------------------
WITH lead_summary AS (
    SELECT 
        channel,
        COUNT(*) AS total_inbound_leads,
        SUM(CASE WHEN funnel_stage = 'Closed-Won' THEN 1 ELSE 0 END) AS customers_acquired,
        ROUND(SUM(deal_value_usd), 2) AS attributed_revenue
    FROM fact_marketing_leads
    GROUP BY channel
),
spend_summary AS (
    SELECT 
        channel,
        SUM(budget_spend_usd) AS channel_spend
    FROM dim_campaigns
    GROUP BY channel
)
SELECT 
    l.channel,
    s.channel_spend,
    l.total_inbound_leads,
    l.customers_acquired,
    ROUND((l.customers_acquired / l.total_inbound_leads) * 100, 2) AS overall_conversion_rate_pct,
    l.attributed_revenue,
    ROUND(s.channel_spend / l.customers_acquired, 2) AS customer_acquisition_cost_cac,
    ROUND(l.attributed_revenue / s.channel_spend, 2) AS return_on_ad_spend_roas,
    ROUND(((l.attributed_revenue - s.channel_spend) / s.channel_spend) * 100, 2) AS net_roi_pct
FROM lead_summary l
JOIN spend_summary s ON l.channel = s.channel
ORDER BY net_roi_pct DESC;

-- ------------------------------------------------------------------------
-- QUERY 2: Lead-to-Customer Multi-Stage Conversion Funnel
-- Business Question: What is the volume and transition efficiency between
-- each progressive stage in the conversion funnel?
-- ------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_leads_entered,
    SUM(CASE WHEN funnel_stage IN ('MQL', 'SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) AS stage_mql,
    SUM(CASE WHEN funnel_stage IN ('SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) AS stage_sql,
    SUM(CASE WHEN funnel_stage IN ('Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) AS stage_opportunity,
    SUM(CASE WHEN funnel_stage = 'Closed-Won' THEN 1 ELSE 0 END) AS stage_closed_won,
    
    ROUND(
        (SUM(CASE WHEN funnel_stage IN ('MQL', 'SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) / COUNT(*)) * 100, 
        2
    ) AS lead_to_mql_pct,
    ROUND(
        (SUM(CASE WHEN funnel_stage IN ('SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END) / 
         SUM(CASE WHEN funnel_stage IN ('MQL', 'SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END)) * 100, 
        2
    ) AS mql_to_sql_pct,
    ROUND(
        (SUM(CASE WHEN funnel_stage = 'Closed-Won' THEN 1 ELSE 0 END) / 
         SUM(CASE WHEN funnel_stage IN ('SQL', 'Opportunity', 'Closed-Won') THEN 1 ELSE 0 END)) * 100, 
        2
    ) AS sql_to_won_pct
FROM fact_marketing_leads;

-- ------------------------------------------------------------------------
-- QUERY 3: Customer Segment Deal Size & Sales Velocity Analysis
-- Business Question: What is the average deal size and sales velocity
-- (days to close) across Enterprise, Mid-Market, and SMB tiers?
-- ------------------------------------------------------------------------
SELECT 
    customer_segment,
    COUNT(CASE WHEN funnel_stage = 'Closed-Won' THEN 1 END) AS deals_won,
    ROUND(SUM(deal_value_usd), 2) AS total_segment_revenue,
    ROUND(AVG(CASE WHEN funnel_stage = 'Closed-Won' THEN deal_value_usd END), 2) AS avg_deal_size_usd,
    ROUND(AVG(CASE WHEN funnel_stage = 'Closed-Won' THEN days_to_close END), 1) AS avg_sales_cycle_days
FROM fact_marketing_leads
GROUP BY customer_segment
ORDER BY total_segment_revenue DESC;
