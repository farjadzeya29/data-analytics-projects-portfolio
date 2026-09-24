-- Project 3: Load Data Script
USE supply_chain_analytics;

LOAD DATA LOCAL INFILE 'data/processed/supply_chain_shipments_cleaned.csv'
INTO TABLE fact_shipments
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(shipment_id, order_date, supplier_id, supplier_name, supplier_tier, warehouse_id, origin_warehouse, carrier_name, weight_kg, shipping_cost_usd, scheduled_delivery_date, actual_delivery_date, delivery_delay_days, delivery_status, on_time_flag, damage_flag);
