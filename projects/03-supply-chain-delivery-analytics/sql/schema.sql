-- Project 3: Supply Chain & Delivery Performance Analytics
-- Database Schema (MySQL 8.0+ Compatible)
-- Author: Farjad Zeya (Data Analyst)

CREATE DATABASE IF NOT EXISTS supply_chain_analytics;
USE supply_chain_analytics;

DROP TABLE IF EXISTS fact_shipments;
CREATE TABLE fact_shipments (
    shipment_id VARCHAR(30) PRIMARY KEY,
    order_date DATE NOT NULL,
    supplier_id VARCHAR(20) NOT NULL,
    supplier_name VARCHAR(100) NOT NULL,
    supplier_tier VARCHAR(20) NOT NULL,
    warehouse_id VARCHAR(20) NOT NULL,
    origin_warehouse VARCHAR(100) NOT NULL,
    carrier_name VARCHAR(50) NOT NULL,
    weight_kg DECIMAL(10,2) NOT NULL,
    shipping_cost_usd DECIMAL(12,2) NOT NULL,
    scheduled_delivery_date DATE NOT NULL,
    actual_delivery_date DATE NOT NULL,
    delivery_delay_days INT NOT NULL,
    delivery_status VARCHAR(20) NOT NULL,
    on_time_flag TINYINT(1) NOT NULL,
    damage_flag TINYINT(1) NOT NULL,
    INDEX idx_warehouse_ontime (origin_warehouse, on_time_flag),
    INDEX idx_supplier (supplier_id),
    INDEX idx_carrier (carrier_name)
);
