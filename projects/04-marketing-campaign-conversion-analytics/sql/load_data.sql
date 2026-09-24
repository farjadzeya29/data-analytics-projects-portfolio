-- Project 4: Load Data Script
USE marketing_analytics;

LOAD DATA LOCAL INFILE 'data/processed/marketing_leads_cleaned.csv'
INTO TABLE fact_leads
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(lead_id, lead_date, campaign_id, campaign_name, marketing_channel, target_segment, funnel_stage, is_mql, is_sql, is_opportunity, is_customer, deal_value_usd, days_to_close);
