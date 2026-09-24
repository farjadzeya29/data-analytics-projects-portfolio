-- Project 1: Load Data Script
USE ecommerce_analytics;

LOAD DATA LOCAL INFILE 'data/processed/ecommerce_transactions_cleaned.csv'
INTO TABLE fact_orders
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, order_date, customer_id, customer_name, segment, region, category, sub_category, product_name, unit_price, quantity, discount, sales, profit, shipping_mode);
