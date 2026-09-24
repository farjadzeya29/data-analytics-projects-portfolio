-- Project 4: Marketing Campaign & Customer Conversion Analytics
-- Database Schema (MySQL 8.0+ Compatible)
-- Author: Farjad Zeya (Data Analyst)

CREATE DATABASE IF NOT EXISTS marketing_analytics;
USE marketing_analytics;

DROP TABLE IF EXISTS fact_leads;
CREATE TABLE fact_leads (
    lead_id VARCHAR(30) PRIMARY KEY,
    lead_date DATE NOT NULL,
    campaign_id VARCHAR(20) NOT NULL,
    campaign_name VARCHAR(100) NOT NULL,
    marketing_channel VARCHAR(50) NOT NULL,
    target_segment VARCHAR(50) NOT NULL,
    funnel_stage VARCHAR(50) NOT NULL,
    is_mql TINYINT(1) NOT NULL,
    is_sql TINYINT(1) NOT NULL,
    is_opportunity TINYINT(1) NOT NULL,
    is_customer TINYINT(1) NOT NULL,
    deal_value_usd DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    days_to_close INT NOT NULL,
    INDEX idx_channel (marketing_channel),
    INDEX idx_campaign (campaign_id),
    INDEX idx_stage (funnel_stage)
);
