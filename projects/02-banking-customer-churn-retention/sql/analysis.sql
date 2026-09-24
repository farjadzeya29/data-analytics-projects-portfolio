-- Project 2: Analytical SQL Scripts
USE banking_retention;

-- 1. Baseline Attrition KPIs
SELECT 
    COUNT(*) AS total_customers,
    SUM(exited) AS churned_customers,
    ROUND((SUM(exited) / COUNT(*)) * 100, 2) AS overall_churn_rate_pct,
    ROUND(SUM(balance), 2) AS total_deposits_usd,
    ROUND(SUM(CASE WHEN exited = 1 THEN balance ELSE 0 END), 2) AS churned_deposits_usd
FROM fact_bank_customers;

-- 2. Multi-Product Paradox Query
SELECT 
    num_of_products,
    COUNT(*) AS customer_count,
    SUM(exited) AS churn_count,
    ROUND((SUM(exited) / COUNT(*)) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(balance), 2) AS avg_account_balance
FROM fact_bank_customers
GROUP BY num_of_products
ORDER BY num_of_products;

-- 3. Geography & Activity Cohort Evaluation
SELECT 
    geography,
    CASE WHEN is_active_member = 1 THEN 'Active Member' ELSE 'Inactive Member' END AS engagement_status,
    COUNT(*) AS total_accounts,
    SUM(exited) AS churned_accounts,
    ROUND((SUM(exited) / COUNT(*)) * 100, 2) AS churn_rate_pct
FROM fact_bank_customers
GROUP BY geography, is_active_member
ORDER BY geography, is_active_member;

-- 4. High-Balance Churn Risk Ranking using Window Functions
WITH at_risk_accounts AS (
    SELECT 
        customer_id,
        geography,
        age,
        balance,
        num_of_products,
        is_active_member,
        exited,
        DENSE_RANK() OVER (ORDER BY balance DESC) AS balance_rank
    FROM fact_bank_customers
    WHERE exited = 1 AND balance > 50000
)
SELECT 
    customer_id,
    geography,
    age,
    balance,
    num_of_products,
    is_active_member,
    balance_rank
FROM at_risk_accounts
LIMIT 25;
