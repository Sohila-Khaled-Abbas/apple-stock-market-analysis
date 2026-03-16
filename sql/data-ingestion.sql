-- =========================================================================================
-- Apple Stock Market Analysis - Data Ingestion Script
-- Purpose: This script initializes the database, creates the primary table for daily 
--          stock prices, and bulk loads the historical raw data from a CSV file.
-- Note: Requires MySQL to be configured with 'local_infile=1' for LOAD DATA LOCAL INFILE.
-- =========================================================================================

-- 1. Initialize the Target Database
CREATE DATABASE apple_stock_db;
USE apple_stock_db;

-- 2. Define the Schema for Historical Daily Data
CREATE TABLE aapl_daily (
    trade_date DATE PRIMARY KEY,        -- The date of the trading session (unique identifier)
    open_price DECIMAL(18, 6),          -- The price at market open
    high_price DECIMAL(18, 6),          -- The highest price during the session
    low_price DECIMAL(18, 6),           -- The lowest price during the session
    close_price DECIMAL(18, 6),         -- The price at market close
    adj_close_price DECIMAL(18, 6),     -- The adjusted closing price (accounts for dividends/splits)
    volume BIGINT,                      -- Total number of shares traded
    INDEX idx_date (trade_date)         -- Index on date to optimize time-series queries
);

-- 3. Ingest Raw Data from CSV Export
-- Make sure the path matches your local environment or the project's relative structure
LOAD DATA LOCAL INFILE '../data/raw/apple_stock_history_1980_2025.csv'
INTO TABLE aapl_daily
FIELDS TERMINATED BY ',' 
IGNORE 1 LINES                          -- Skip the CSV header row
(trade_date, adj_close_price, close_price, high_price, low_price, open_price, volume);