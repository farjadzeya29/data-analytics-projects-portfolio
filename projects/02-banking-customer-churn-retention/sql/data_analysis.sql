-- ========================================================================
-- Project 2: Banking Customer Churn & Retention Analysis - Core SQL Queries
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

USE banking_retention;

-- ------------------------------------------------------------------------
-- QUERY 1: Overall Bank Customer Churn Rate & Total Capital at Risk
-- Business Question: What is the bank's baseline churn rate, and how much
-- total balance was lost to churned accounts?
-- ------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN churn = 0 THEN 1 ELSE 0 END) AS retained_customers,
    ROUND((SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS overall_churn_rate_pct,
    ROUND(SUM(CASE WHEN churn = 1 THEN account_balance ELSE 0 END), 2) AS total_balance_lost_usd,
    ROUND(AVG(CASE WHEN churn = 1 THEN account_balance ELSE NULL END), 2) AS avg_churned_balance
FROM bank_customers;

-- ------------------------------------------------------------------------
-- QUERY 2: Churn by Customer Tenure Cohorts
-- Business Question: Does churn occur primarily during early onboarding
-- (years 0-2) or among long-standing mature clients?
-- ------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN tenure_years <= 1 THEN '0-1 Year (New / Onboarding)'
        WHEN tenure_years BETWEEN 2 AND 4 THEN '2-4 Years (Early Stage)'
        WHEN tenure_years BETWEEN 5 AND 7 THEN '5-7 Years (Established)'
        ELSE '8+ Years (Mature / Veteran)'
    END AS tenure_cohort,
    COUNT(*) AS customer_count,
    SUM(churn) AS churned_count,
    ROUND((SUM(churn) / COUNT(*)) * 100, 2) AS cohort_churn_rate_pct,
    ROUND(AVG(account_balance), 2) AS avg_cohort_balance
FROM bank_customers
GROUP BY 
    CASE 
        WHEN tenure_years <= 1 THEN '0-1 Year (New / Onboarding)'
        WHEN tenure_years BETWEEN 2 AND 4 THEN '2-4 Years (Early Stage)'
        WHEN tenure_years BETWEEN 5 AND 7 THEN '5-7 Years (Established)'
        ELSE '8+ Years (Mature / Veteran)'
    END
ORDER BY cohort_churn_rate_pct DESC;

-- ------------------------------------------------------------------------
-- QUERY 3: Activity Status vs Account Balance Interaction
-- Business Question: How does digital/branch activity status correlate with
-- churn across zero-balance vs funded bank accounts?
-- ------------------------------------------------------------------------
SELECT 
    CASE WHEN is_active_member = 1 THEN 'Active Member' ELSE 'Inactive Member' END AS activity_status,
    CASE 
        WHEN account_balance = 0 THEN 'Zero Balance ($0)'
        WHEN account_balance < 75000 THEN 'Low Balance (<$75k)'
        WHEN account_balance BETWEEN 75000 AND 140000 THEN 'Medium Balance ($75k-$140k)'
        ELSE 'High Balance (>$140k)'
    END AS balance_tier,
    COUNT(*) AS customer_count,
    SUM(churn) AS churned_count,
    ROUND((SUM(churn) / COUNT(*)) * 100, 2) AS churn_rate_pct,
    ROUND(SUM(account_balance), 2) AS total_segment_balance
FROM bank_customers
GROUP BY activity_status, balance_tier
ORDER BY activity_status, churn_rate_pct DESC;

-- ------------------------------------------------------------------------
-- QUERY 4: Number of Bank Products vs Churn
-- Business Question: How does product bundling (accounts, cards, loans) impact
-- customer retention? Are multi-product clients stickier?
-- ------------------------------------------------------------------------
SELECT 
    num_of_products,
    COUNT(*) AS customer_count,
    SUM(churn) AS churned_count,
    ROUND((SUM(churn) / COUNT(*)) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction,
    ROUND(AVG(account_balance), 2) AS avg_balance
FROM bank_customers
GROUP BY num_of_products
ORDER BY num_of_products ASC;

-- ------------------------------------------------------------------------
-- QUERY 5: Geographic & Demographic Churn Profile
-- Business Question: What geographic markets and age segments exhibit elevated churn?
-- ------------------------------------------------------------------------
SELECT 
    geography,
    gender,
    COUNT(*) AS total_customers,
    SUM(churn) AS churned_count,
    ROUND((SUM(churn) / COUNT(*)) * 100, 2) AS geo_churn_rate_pct,
    ROUND(AVG(age), 1) AS avg_age,
    ROUND(AVG(credit_score), 1) AS avg_credit_score
FROM bank_customers
GROUP BY geography, gender
ORDER BY geo_churn_rate_pct DESC;
