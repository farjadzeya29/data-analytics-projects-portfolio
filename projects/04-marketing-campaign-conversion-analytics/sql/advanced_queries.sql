-- ========================================================================
-- Project 4: Marketing Campaign Analytics - Advanced Queries
-- Author: Farjad Zeya (Data Analyst)
-- Features: CTEs, Window Ranking, Cohort Cumulative Metrics
-- ========================================================================

USE marketing_analytics;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 1: Campaign Performance Ranking & Underperformer Detection
-- Business Question: Rank all campaigns by Net ROI and flag underperforming
-- campaigns failing to achieve break-even ROAS (ROAS < 1.0).
-- ------------------------------------------------------------------------
WITH campaign_metrics AS (
    SELECT 
        c.campaign_id,
        c.campaign_name,
        c.channel,
        c.budget_spend_usd,
        COUNT(l.lead_id) AS total_leads,
        SUM(CASE WHEN l.funnel_stage = 'Closed-Won' THEN 1 ELSE 0 END) AS deals_won,
        ROUND(SUM(CASE WHEN l.funnel_stage = 'Closed-Won' THEN l.deal_value_usd ELSE 0 END), 2) AS revenue_won
    FROM dim_campaigns c
    LEFT JOIN fact_marketing_leads l ON c.campaign_id = l.campaign_id
    GROUP BY c.campaign_id, c.campaign_name, c.channel, c.budget_spend_usd
)
SELECT 
    campaign_name,
    channel,
    budget_spend_usd,
    deals_won,
    revenue_won,
    ROUND(revenue_won / budget_spend_usd, 2) AS roas,
    ROUND(((revenue_won - budget_spend_usd) / budget_spend_usd) * 100, 2) AS roi_pct,
    DENSE_RANK() OVER (ORDER BY (revenue_won / budget_spend_usd) DESC) AS efficiency_rank,
    CASE 
        WHEN (revenue_won / budget_spend_usd) >= 3.0 THEN 'High Performer (Scale Budget)'
        WHEN (revenue_won / budget_spend_usd) >= 1.2 THEN 'Moderate Performer (Optimize)'
        ELSE 'Underperformer (Reallocate / Terminate)'
    END AS budget_recommendation
FROM campaign_metrics
ORDER BY efficiency_rank ASC;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 2: Monthly Cumulative Attributed Revenue by Channel
-- Business Question: Track running total attributed revenue by channel over time.
-- ------------------------------------------------------------------------
WITH monthly_revenue AS (
    SELECT 
        channel,
        DATE_FORMAT(created_date, '%Y-%m') AS lead_month,
        ROUND(SUM(deal_value_usd), 2) AS month_revenue
    FROM fact_marketing_leads
    WHERE funnel_stage = 'Closed-Won'
    GROUP BY channel, DATE_FORMAT(created_date, '%Y-%m')
)
SELECT 
    channel,
    lead_month,
    month_revenue,
    ROUND(
        SUM(month_revenue) OVER (PARTITION BY channel ORDER BY lead_month),
        2
    ) AS cumulative_channel_revenue
FROM monthly_revenue
ORDER BY channel, lead_month;
