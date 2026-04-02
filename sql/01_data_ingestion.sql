-- =========================================================================================
-- Apple Stock Market Analysis - Data Ingestion Script
-- Purpose: This script initializes the database, creates the primary table for daily 
--          stock prices, and bulk loads the historical raw data from a CSV file.
-- Note: Ensure MySQL has the appropriate permissions for LOAD DATA INFILE.
-- =========================================================================================

-- 1. Create Schema
CREATE DATABASE apple_stock_db;
USE apple_stock_db;

-- 2. Create Table with Exact Column Mapping
CREATE TABLE aapl_daily (
    Trade_Date DATETIME PRIMARY KEY, -- The date/time of the trading session (Excel exports often include timestamps)
    Adj_Close DECIMAL(18, 6),        -- The adjusted closing price (accounts for dividends/splits)
    Close_Price DECIMAL(18, 6),      -- The standard price at market close
    High_Price DECIMAL(18, 6),       -- The highest price during the session
    Low_Price DECIMAL(18, 6),        -- The lowest price during the session
    Open_Price DECIMAL(18, 6),       -- The price at market open
    Volume BIGINT                    -- Total number of shares traded
);

-- 3. Ingestion (Load Data Infile Example)
=LOAD DATA LOCAL INFILE '../data/raw/apple_stock_history_1980_2025.csv'
INTO TABLE aapl_daily
FIELDS TERMINATED BY ',' 
IGNORE 1 LINES                         -- Skip the CSV header row
(Trade_Date, Adj_Close, Close_Price, High_Price, Low_Price, Open_Price, Volume);