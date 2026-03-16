-- =========================================================================================
-- Apple Stock Market Analysis - Data Cleaning & Validation Script
-- Purpose: This script performs data quality assertions and data imputation on the 
--          aapl_daily table to ensure the dataset is ready for reliable analytics.
-- =========================================================================================

-- -----------------------------------------------------------------------------------------
-- 1. Logical Range Assertion (Price Boundaries)
-- -----------------------------------------------------------------------------------------
-- Description: Retrieves any records where the daily High_Price is unexpectedly lower than 
-- the Low_Price or Close_Price, or where the Low_Price is higher than the Close_Price.
-- Expected Result: 0 rows (Ideally, all standard prices should fall between High and Low).
SELECT * FROM aapl_daily 
WHERE High_Price < Low_Price OR High_Price < Close_Price OR Low_Price > Close_Price;

-- -----------------------------------------------------------------------------------------
-- 2. Data Imputation: Fix the 0 Volume Anomaly
-- -----------------------------------------------------------------------------------------
-- Description: The data profiling step identified a trading day (e.g., 1981-08-10) with an 
-- erroneous trading volume of 0. This query imputes that missing volume by calculating the 
-- average volume over a surrounding 20-day period ('1981-08-01' to '1981-08-20') and 
-- updates the anomalous row with this moving average to maintain data continuity.
UPDATE aapl_daily t1
JOIN (SELECT AVG(Volume) as avg_v FROM aapl_daily WHERE Trade_Date BETWEEN '1981-08-01' AND '1981-08-20') t2
SET t1.Volume = t2.avg_v
WHERE t1.Volume = 0;

-- -----------------------------------------------------------------------------------------
-- 3. Consistency Check: Adjusted Close vs. Close Price
-- -----------------------------------------------------------------------------------------
-- Description: Counts records where the Adjusted Close price is strictly greater than the 
-- standard Close Price. 
-- Note: Adjusted Close usually accounts for historical stock splits and dividends, meaning 
-- it should typically be less than or equal to the actual Close Price on that day. If 
-- Adj_Close > Close_Price, the data provider might be using a non-standard adjustment method.
SELECT COUNT(*) FROM aapl_daily WHERE Adj_Close > Close_Price;