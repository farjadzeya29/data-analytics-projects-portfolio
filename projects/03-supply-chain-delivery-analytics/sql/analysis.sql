-- Project 3: Analytical SQL Queries
USE supply_chain_analytics;

-- 1. Operational Fulfillment Scorecard
SELECT 
    COUNT(*) AS total_shipments,
    SUM(on_time_flag) AS on_time_shipments,
    ROUND((SUM(on_time_flag) / COUNT(*)) * 100, 2) AS network_otd_pct,
    ROUND(AVG(CASE WHEN delivery_status = 'Delayed' THEN delivery_delay_days ELSE NULL END), 2) AS avg_delay_days,
    ROUND(SUM(shipping_cost_usd), 2) AS total_shipping_spend,
    ROUND(AVG(shipping_cost_usd / weight_kg), 2) AS avg_cost_per_kg
FROM fact_shipments;

-- 2. Warehouse Dispatch Bottleneck Ranking
SELECT 
    warehouse_id,
    origin_warehouse,
    COUNT(*) AS total_consignments,
    SUM(on_time_flag) AS on_time_consignments,
    ROUND((SUM(on_time_flag) / COUNT(*)) * 100, 2) AS warehouse_otd_pct,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delay_days,
    DENSE_RANK() OVER (ORDER BY (SUM(on_time_flag) / COUNT(*)) ASC) AS bottleneck_rank
FROM fact_shipments
GROUP BY warehouse_id, origin_warehouse
ORDER BY warehouse_otd_pct ASC;

-- 3. Supplier Tier Reliability & Defect Rate
SELECT 
    supplier_tier,
    COUNT(*) AS total_orders,
    ROUND((SUM(on_time_flag) / COUNT(*)) * 100, 2) AS tier_otd_pct,
    ROUND((SUM(damage_flag) / COUNT(*)) * 100, 2) AS damage_rate_pct
FROM fact_shipments
GROUP BY supplier_tier
ORDER BY tier_otd_pct DESC;
