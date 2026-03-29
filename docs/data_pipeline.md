# Apple Stock Data Pipeline Documentation

This document serves as a technical reference for the data engineering pipeline backing the Apple Stock Market Analysis project. It outlines the workflows spread across the `notebooks/` and `sql/` directories.

## Pipeline Architecture

The data pipeline follows an **ELT (Extract, Load, Transform)** pattern combined with incremental API polling to ensure the database remains current without requiring massive bulk reloads.

---

## 1. Data Ingestion & Incremental Loading

### Initial Database Setup (`sql/01_data_ingestion.sql`)

- **Action:** Initializes the `apple_stock_db` MySQL database and provisions the `aapl_daily` table schema.
- **Bulk Load:** Executes a `LOAD DATA LOCAL INFILE` command. This uses the massive, historically complete `apple_stock_history_1980_2025.csv` (located in `data/raw/`) to seed the database instantly up to the last known date.

### Incremental Fetching (`notebooks/02_data_loading.ipynb`)

- **Action:** Runs a Python script utilizing `yfinance`, `pandas`, and `sqlalchemy`.
- **Process:** 
  1. Queries MySQL (`SELECT MAX(Trade_Date)...`) to uniquely identify the most recent trading session registered.
  2. Pings the Yahoo Finance API to dynamically fetch any missing days between the recorded max date and today's date.
  3. Formats the parsed data gracefully into strict MySQL columns (`Trade_Date`, `Adj_Close`, etc.), flattens multi-indexes, and handles NaNs.
  4. Appends only new records to the database.

### Automated Data Loading (Python Daemon)

- **Action:** Automates the execution of the incremental data extraction on a daily schedule natively within Python.
- **Process:**
  1. The daemon script `scripts/yf_update.py` utilizes the Python `schedule` library.
  2. Running persistently in the background locally, it triggers automatically every day at 18:00 (after market close).
  3. The script executes the incremental update logic to pull historical data safely into the MySQL database, followed by an automated CSV export to `data/processed/aapl_daily.csv`.

---

## 2. Data Cleaning & Automated QA

### Pre-Analysis Profiling (`notebooks/01_data_profiling.ipynb`)

- **Action:** Exploratory Jupyter notebook serving as the initial sandbox.
- **Process:** Generates Pandas-driven `describe()` metrics, null-value tallies, and manual logic assertions (e.g., confirming `High` >= `Low`) before committing structural schema definitions to SQL.

### SQL Cleaning Validation (`sql/02_data_cleaning.sql`)

- **Objective:** Maintain persistent data integrity and resolve anomalies inside the data warehouse.
- **Duplicate Handing:** A self-join DELETE strategy drops exact duplicate dates, specifically favoring rows with a higher reported `Volume` under the assumption they represent more granular precision.
- **Logical Rules Validation:** Detects illogical inputs natively, throwing warning rows if `High_Price < Low_Price` or `High_Price < Close_Price`.
- **Imputation:** Resolves anomalous entries (such as the 1981-08-10 zero-volume day) natively in SQL by patching it over with an averaged 20-day moving volume window (`AVG(Volume) BETWEEN '1981-08-01' AND '1981-08-20'`).

### Database & API Cross-Validation (`notebooks/03_data_validation.ipynb`)

- **Objective:** Validates the structural integrity and factual accuracy of the `aapl_daily` table after it has been populated and cleaned.
- **Process:**
  1. Executes Pandas-driven structural asserts natively against the SQL engine (e.g., verifying zero nulls, strictly unique dates, and robust price boundaries).
  2. Integrates an external data audit by sampling historical dates from the local database and cross-referencing them against fresh Yahoo Finance API calls.
  3. Audits the `Adj_Close` mapping consistency against `Close_Price`.

---

## 3. Metrics & Exploratory Data Analysis (EDA)

### Advanced Analytics (`sql/03_eda_and_metrics.sql`)

- **Objective:** Translates raw stock prices into meaningful financial derivatives to be served directly into Power BI.
- **Compound Annual Growth Rate (CAGR):** Performs a mathematical scaling equation `(Ending Value / Beginning Value) ^ (1 / Number of Years) - 1` across the dataset's entire footprint footprint.
- **Moving Average Signals:**
  - Employs SQL Server window functions `AVG(...) OVER(ORDER BY ... ROWS BETWEEN X PRECEDING)` to compute 50-day and 200-day Simple Moving Averages.
  - Implements a declarative `CASE WHEN` statement to label market momentum. The label evaluates as `Bullish` (Golden Cross) when the 50-day SMA supersedes the 200-day SMA, and `Bearish` (Death Cross) when it drops below.
