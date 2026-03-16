-- =========================================================================================
-- Apple Stock Market Analysis - Data Cleaning & Validation Script
-- Purpose: This script performs post-ingestion quality checks, removes duplicate entries,
--          verifies logical price consistency, and calculates new analytical metrics.
-- =========================================================================================

-- -----------------------------------------------------------------------------------------
-- 1. Identify and Remove Potential Duplicates
-- -----------------------------------------------------------------------------------------
-- Description: Self-joins the aapl_daily table on the trade date. If two rows share the 
-- same date, it deletes the one with the lower trading volume (assuming higher volume 
-- records represent more complete/precise daily trading data).
DELETE t1 FROM aapl_daily t1
INNER JOIN aapl_daily t2 
WHERE t1.trade_date = t2.trade_date AND t1.volume < t2.volume;

-- -----------------------------------------------------------------------------------------
-- 2. Logical Consistency Check
-- -----------------------------------------------------------------------------------------
-- Description: Returns any anomalous rows where the highest price of the day is somehow
-- lower than the lowest price or the closing price. These indicate faulty source data 
-- that may require manual review or exclusion.
SELECT * FROM aapl_daily 
WHERE high_price < low_price 
   OR high_price < close_price;

-- -----------------------------------------------------------------------------------------
-- 3. Calculate Derived Metrics for Analytics (Daily Return)
-- -----------------------------------------------------------------------------------------
-- Description: Adds a new column to store the calculated percentage change in closing 
-- price from the previous trading day.
ALTER TABLE aapl_daily ADD COLUMN daily_return DECIMAL(10, 6);

-- Temporarily disable safe updates to allow updating all rows in the table
SET SQL_SAFE_UPDATES = 0;

-- Update the new column using the LAG() window function
-- Formula: (Current Adjusted Close - Previous Adjusted Close) / Previous Adjusted Close
UPDATE aapl_daily t1
JOIN (
    SELECT trade_date, 
           (adj_close_price - LAG(adj_close_price) OVER (ORDER BY trade_date)) / 
           LAG(adj_close_price) OVER (ORDER BY trade_date) as ret
    FROM aapl_daily
) t2 ON t1.trade_date = t2.trade_date
SET t1.daily_return = t2.ret;