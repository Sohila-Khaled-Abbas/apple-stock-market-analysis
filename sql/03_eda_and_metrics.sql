-- =========================================================================================
-- Apple Stock Market Analysis - Exploratory Data Analysis (EDA) & Metrics Script
-- Purpose: This script calculates key financial metrics and generates trading signals 
--          based on historical price action.
-- =========================================================================================

-- -----------------------------------------------------------------------------------------
-- 1. Calculate Compound Annual Growth Rate (CAGR)
-- -----------------------------------------------------------------------------------------
-- Description: Calculates the annualized return of AAPL over the entire dataset footprint.
-- Formula: (Ending Value / Beginning Value) ^ (1 / Number of Years) - 1
SELECT 
    MIN(Trade_Date) as Start_Date, 
    MAX(Trade_Date) as End_Date,
    POW(MAX(Adj_Close) / MIN(Adj_Close), 1 / (DATEDIFF(MAX(Trade_Date), MIN(Trade_Date))/365)) - 1 as CAGR
FROM aapl_daily
WHERE Adj_Close > 0;

-- -----------------------------------------------------------------------------------------
-- 2. Moving Average Crossover Strategy (Golden Cross / Death Cross)
-- -----------------------------------------------------------------------------------------
-- Description: Uses window functions to calculate the 50-day and 200-day Simple Moving 
-- Averages (SMA). It then categorizes the current market trend as 'Bullish' if the 
-- short-term trend (50-day) is above the long-term trend (200-day), or 'Bearish' otherwise.
WITH SMAs AS (
    SELECT 
        Trade_Date, 
        Adj_Close,
        -- The window functions look at the physical rows in your table
        AVG(Adj_Close) OVER(ORDER BY Trade_Date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) as SMA_50,
        AVG(Adj_Close) OVER(ORDER BY Trade_Date ROWS BETWEEN 199 PRECEDING AND CURRENT ROW) as SMA_200,
        -- Count rows to identify 'invalid' calculations (Cold Start)
        COUNT(*) OVER(ORDER BY Trade_Date ROWS BETWEEN 199 PRECEDING AND CURRENT ROW) as Data_Points
    FROM aapl_daily
)
SELECT 
    Trade_Date, 
    Adj_Close, 
    SMA_50, 
    SMA_200,
    CASE 
        WHEN Data_Points < 200 THEN 'Insufficient Data'
        WHEN SMA_50 > SMA_200 THEN 'Bullish' 
        ELSE 'Bearish' 
    END as Trend_Status -- Renamed from reserved 'Signal'
FROM SMAs
WHERE Trade_Date >= '2024-01-01'
ORDER BY Trade_Date DESC;