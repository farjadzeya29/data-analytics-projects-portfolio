-- Project 2: Banking Customer Churn & Retention Analysis
-- Database Schema (MySQL 8.0+ Compatible)
-- Author: Farjad Zeya (Data Analyst)

CREATE DATABASE IF NOT EXISTS banking_retention;
USE banking_retention;

DROP TABLE IF EXISTS fact_bank_customers;
CREATE TABLE fact_bank_customers (
    customer_id VARCHAR(30) PRIMARY KEY,
    geography VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    tenure INT NOT NULL,
    credit_score INT NOT NULL,
    balance DECIMAL(12,2) NOT NULL,
    num_of_products INT NOT NULL,
    has_cr_card TINYINT(1) NOT NULL,
    is_active_member TINYINT(1) NOT NULL,
    estimated_salary DECIMAL(12,2) NOT NULL,
    exited TINYINT(1) NOT NULL,
    risk_tier VARCHAR(30) NOT NULL,
    INDEX idx_geo_exit (geography, exited),
    INDEX idx_products (num_of_products),
    INDEX idx_activity (is_active_member)
);
