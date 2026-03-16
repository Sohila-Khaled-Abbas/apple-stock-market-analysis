-- =========================================================================================
-- Apple Stock Market Analysis - Data Cleaning & Validation Script
-- Purpose: This script performs data quality checks, resolves duplicates, and calculates 
--          derived financial metrics (like daily return) needed for the Power BI dashboard.
-- =========================================================================================

-- 1. Identify and Remove Potential Duplicates
-- If multiple rows exist for the same Date, this query deletes the one with the 
-- lower volume, assuming the row with higher volume is the more accurate/updated record.
DELETE t1 FROM `apple stock historical stock market data (1980-2025)` t1
INNER JOIN `apple stock historical stock market data (1980-2025)` t2 
WHERE t1.`Date` = t2.`Date` AND t1.`Volume` < t2.`Volume`; -- Keep higher precision row

-- 2. Logical Consistency Check
-- Verifies the fundamental rule of stock pricing: The High price must always be greater 
-- than or equal to both the Low price and the Closing price. Any results returned here 
-- indicate bad data that requires manual review.
SELECT * FROM `apple stock historical stock market data (1980-2025)`
WHERE `High` < `Low` OR `High` < `Close`;

-- 3. Calculate Derived Metrics for Analytics (Daily Return)
-- Adds a new column to store the percentage change in adjusted closing price 
-- from the previous trading day.
ALTER TABLE `apple stock historical stock market data (1980-2025)` ADD COLUMN `daily_return` DECIMAL(10, 6);

-- Disable safe updates temporarily to allow updating the entire table without a WHERE clause
SET SQL_SAFE_UPDATES = 0;

-- Calculate the day-over-day return using the LAG() window function
-- Note: Ordering by `Date` (which is textual) assumes it is in a sortable format (like YYYY-MM-DD). If it's not, you may need STR_TO_DATE().
UPDATE `apple stock historical stock market data (1980-2025)` t1
JOIN (
    SELECT `Date`, 
           (`Adj Close` - LAG(`Adj Close`) OVER (ORDER BY `Date`)) / 
           LAG(`Adj Close`) OVER (ORDER BY `Date`) as ret
    FROM `apple stock historical stock market data (1980-2025)`
) t2 ON t1.`Date` = t2.`Date`
SET t1.`daily_return` = t2.ret;