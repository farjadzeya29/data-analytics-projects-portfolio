-- Project 2: Load Data Script
USE banking_retention;

LOAD DATA LOCAL INFILE 'data/processed/banking_churn_cleaned.csv'
INTO TABLE fact_bank_customers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, geography, gender, age, tenure, credit_score, balance, num_of_products, has_cr_card, is_active_member, estimated_salary, exited, risk_tier);
