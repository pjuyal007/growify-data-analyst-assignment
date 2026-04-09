-- Campaign Dimension Table
-- This table stores campaign metadata parsed form campaign names
CREATE TABLE dim_campaign (
    campaign_id INTEGER PRIMARY KEY,
    data_source_name TEXT,
    campaign_name TEXT,
    channel TEXT,
    region TEXT,
    funnel_stage TEXT,
    brand TEXT,
    persona TEXT,
    
);

-- Sales Fact Table
-- fact sales is central fact table
CREATE TABLE fact_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    date DATE,

    -- region
    funnel_region TEXT,

    geo_location_segment TEXT,

    -- Marketing metrics
    impressions REAL,
    clicks REAL,
    spend REAL,

    -- Calculated metrics
    ctr REAL,
    cpc REAL,
    cpm REAL,
    roi REAL,
    

    -- Conversion metrics
    revenue REAL,
    total_orders REAL,

    FOREIGN KEY (campaign_id) REFERENCES dim_campaign(campaign_id)
);
-- Date dimension
CREATE TABLE dim_date (
    date DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER,
    week INTEGER
);
-- Indexes for faster filtering in Power BI and AI queries
CREATE INDEX idx_fact_date ON fact_sales(date); -- for fater time-based filtering
CREATE INDEX idx_fact_campaign ON fact_sales(campaign_id); -- for faster joins   
CREATE INDEX idx_campaign_region ON dim_campaign(region); -- ofr filtering 
CREATE INDEX idx_campaign_channel ON dim_campaign(channel);
CREATE INDEX idx_campaign_platform ON dim_campaign(data_source_name);


-- power bi query 
SELECT 
    d.year,
    d.month,
    c.data_source_name AS platform,
    c.channel,
    c.region,
    
    SUM(f.spend) AS total_spend,
    SUM(f.impressions) AS total_impressions,
    SUM(f.clicks) AS total_clicks,
    SUM(f.revenue) AS total_revenue,
    
    AVG(f.ctr) AS avg_ctr,
    AVG(f.cpc) AS avg_cpc,
    AVG(f.cpm) AS avg_cpm,
    AVG(f.roi) AS avg_roi

FROM fact_sales f

JOIN dim_campaign c 
    ON f.campaign_id = c.campaign_id

JOIN dim_date d 
    ON f.date = d.date

GROUP BY 
    d.year, d.month,
    c.data_source_name,
    c.channel,
    c.region
ORDER BY d.year, d.month;


-- ai query 


SELECT 
    f.date,
    c.campaign_name,
    c.data_source_name AS platform,
    c.region,
    
    f.spend,
    f.clicks,
    f.impressions,
    f.revenue,
    f.roi

FROM fact_sales f

JOIN dim_campaign c 
    ON f.campaign_id = c.campaign_id

WHERE 
    f.date BETWEEN COALESCE(:start_date, f.date)
               AND COALESCE(:end_date, f.date)
    AND (:platform IS NULL OR c.data_source_name = :platform)
    AND (:region IS NULL OR c.region = :region)
    AND (:campaign IS NULL OR c.campaign_name = :campaign);