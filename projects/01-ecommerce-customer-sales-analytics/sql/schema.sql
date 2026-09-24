-- ========================================================================
-- Project 1: E-Commerce Customer & Sales Analytics
-- Database Schema (MySQL Compatible)
-- Author: Farjad Zeya (Data Analyst)
-- ========================================================================

CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

-- Table: dim_customers
DROP TABLE IF EXISTS dim_customers;
CREATE TABLE dim_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment ENUM('Consumer', 'Corporate', 'Home Office') NOT NULL,
    region ENUM('North', 'South', 'East', 'West') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_ecommerce_sales
DROP TABLE IF EXISTS fact_ecommerce_sales;
CREATE TABLE fact_ecommerce_sales (
    order_id VARCHAR(30) NOT NULL,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(30) NOT NULL,
    region VARCHAR(30) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    discount DECIMAL(4,2) DEFAULT 0.00,
    sales_amount DECIMAL(12,2) NOT NULL,
    profit DECIMAL(12,2) NOT NULL,
    shipping_mode VARCHAR(50) NOT NULL,
    PRIMARY KEY (order_id, product_name),
    INDEX idx_order_date (order_date),
    INDEX idx_customer_id (customer_id),
    INDEX idx_region_category (region, category)
);

-- Note for local loading:
-- LOAD DATA LOCAL INFILE 'data/processed/ecommerce_transactions_cleaned.csv'
-- INTO TABLE fact_ecommerce_sales
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
