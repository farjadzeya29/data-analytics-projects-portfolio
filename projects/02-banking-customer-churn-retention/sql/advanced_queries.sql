-- ========================================================================
-- Project 2: Banking Customer Churn & Retention Analysis - Advanced SQL Queries
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

USE banking_retention;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 1: Multi-Dimensional Customer Risk Scoring & Capital Exposure
-- Business Question: Identify high-balance accounts with multiple risk markers
-- (inactivity, age 45-60, complaint history) to build proactive outreach lists.
-- ------------------------------------------------------------------------
WITH scored_customers AS (
    SELECT 
        customer_id,
        surname,
        geography,
        age,
        account_balance,
        num_of_products,
        is_active_member,
        complaint_filed,
        churn,
        -- Analytical composite risk score
        (CASE WHEN is_active_member = 0 THEN 25 ELSE 0 END +
         CASE WHEN num_of_products >= 3 THEN 35 WHEN num_of_products = 1 THEN 15 ELSE 0 END +
         CASE WHEN age BETWEEN 45 AND 60 THEN 20 ELSE 5 END +
         CASE WHEN account_balance > 100000 THEN 15 ELSE 0 END +
         CASE WHEN complaint_filed = 1 THEN 25 ELSE 0 END +
         CASE WHEN geography = 'Germany' THEN 10 ELSE 0 END) AS composite_risk_points
    FROM bank_customers
)
SELECT 
    customer_id,
    surname,
    geography,
    age,
    account_balance,
    num_of_products,
    is_active_member,
    composite_risk_points,
    CASE 
        WHEN composite_risk_points >= 65 THEN 'Critical Risk (Immediate Action)'
        WHEN composite_risk_points >= 40 THEN 'Elevated Risk'
        ELSE 'Stable'
    END AS retention_priority,
    churn AS actual_churn_status
FROM scored_customers
WHERE composite_risk_points >= 40
ORDER BY composite_risk_points DESC, account_balance DESC
LIMIT 50;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 2: Credit Score Percentiles & Churn Distribution
-- Business Question: Using NTILE window functions, analyze whether prime vs.
-- subprime credit score tiers correlate with churn.
-- ------------------------------------------------------------------------
WITH credit_tiers AS (
    SELECT 
        customer_id,
        credit_score,
        account_balance,
        churn,
        NTILE(5) OVER (ORDER BY credit_score ASC) AS credit_quintile
    FROM bank_customers
)
SELECT 
    credit_quintile,
    MIN(credit_score) AS min_credit_score,
    MAX(credit_score) AS max_credit_score,
    COUNT(*) AS total_customers,
    SUM(churn) AS churned_count,
    ROUND((SUM(churn) / COUNT(*)) * 100, 2) AS quintile_churn_rate_pct,
    ROUND(AVG(account_balance), 2) AS avg_balance
FROM credit_tiers
GROUP BY credit_quintile
ORDER BY credit_quintile ASC;

-- ------------------------------------------------------------------------
-- ADVANCED QUERY 3: Cumulative Balance at Risk (Window Running Total)
-- Business Question: What proportion of vulnerable capital is concentrated
-- among the top high-balance churned accounts?
-- ------------------------------------------------------------------------
WITH churned_accounts AS (
    SELECT 
        customer_id,
        surname,
        geography,
        account_balance
    FROM bank_customers
    WHERE churn = 1 AND account_balance > 0
)
SELECT 
    customer_id,
    surname,
    geography,
    account_balance,
    ROW_NUMBER() OVER (ORDER BY account_balance DESC) AS rank_order,
    ROUND(SUM(account_balance) OVER (ORDER BY account_balance DESC), 2) AS cumulative_balance_lost,
    ROUND(
        (SUM(account_balance) OVER (ORDER BY account_balance DESC) / 
         SUM(account_balance) OVER ()) * 100, 
        2
    ) AS pct_of_total_churned_capital
FROM churned_accounts
LIMIT 25;
