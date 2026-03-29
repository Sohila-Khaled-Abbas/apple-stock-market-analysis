# Data Lineage Documentation: Apple Stock Market Analysis

This document traces the complete lifecycle of data within the Apple Stock Market Analysis project, illustrating how raw stock market data is ingested, transformed, and ultimately presented to end-users in Power BI. Understanding the data lineage ensures data trust, traceability, and easier debugging if issues arise in the pipeline.

## 1. Source Systems
Data originates from two primary sources, capturing both historical records and ongoing daily updates.

- **Kaggle / Excel Export (`Apple-Stock-Historical-Data.xlsx`)**
  - **Type:** Static File (CSV / Excel).
  - **Role:** Provides the initial bulk history of AAPL stock prices spanning from 1980 to early 2025.
  - **Attributes Captured:** `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`.
  
- **Yahoo Finance API (`yfinance`)**
  - **Type:** Live External API.
  - **Role:** Fetches daily incremental market data to keep the database up-to-date.
  - **Trigger:** Queried dynamically by identifying the maximum date in the database and fetching subsequent records.

## 2. Processing Layer (Python)
Raw data is extracted and prepared for database insertion using Python scripts and Jupyter Notebooks.

- **Initial Profiling (`notebooks/01_data_profiling.ipynb`)**
  - Conducts Exploratory Data Analysis (EDA) on the static Excel source to verify schema, handle null values, and ensure logical consistency (e.g., `High >= Low`).
  
- **Incremental Fetching & Cleaning (`notebooks/02_data_loading.ipynb` / `scripts/yf_update.py`)**
  - Connects to the Yahoo Finance API.
  - Flattens multi-level indexes returned by `yfinance`.
  - Normalizes column names to match the target database schema structure.
  - Validates missing trading days.
  - **Output Destination:** MySQL Database via SQLAlchemy.

## 3. Storage & Transformation Layer (MySQL)
The central data warehouse ensuring consistency, relational integrity, and analytical transformations.

- **Raw Data Ingestion (`sql/01_data_ingestion.sql`)**
  - **Table:** `aapl_daily` (Serves as the Single Source of Truth).
  - Handles the direct bulk insert mapping of the static CSV dataset into strictly typed columns (`DOUBLE`, `BIGINT`).

- **Data Cleaning (`sql/02_data_cleaning.sql`)**
  - Performs deduplication based on matching dates.
  - Applies imputation logic (e.g., replacing 0 Volume with a 20-day average).
  - Validates price consistencies directly within the storage layer.

- **Data Enrichment (`sql/03_eda_and_metrics.sql`)**
  - Computes persistent metrics essential for the dashboards.
  - Generates the 50-day and 200-day Simple Moving Averages (SMA).
  - Calculates the Compound Annual Growth Rate (CAGR).
  - Flags market momentum indicators directly into columns/views.

## 4. Presentation & Visualization Layer (Power BI)
The final stage where structured data is consumed by stakeholders.

- **On-premises Data Gateway**
  - Acts as the secure bridge between the local MySQL database and the Microsoft cloud ecosystem.
  - Facilitates the scheduled refreshes of the dataset without manual intervention.

- **Power BI Service (Cloud) & Interactive Dashboard**
  - Ingests the enriched data from `aapl_daily` via the secure gateway.
  - Presents interactive visualizations detailing the "Cook Premium", "Buy the Dip" signals, and Moving Average cross-overs.

---
## Summary Flow Diagram

**Raw Data** `(Excel/yfinance)` ➔ **Python Processing** `(Jupyter/Pandas)` ➔ **MySQL Database** `(Storage & SQL Tranformations)` ➔ **On-premises Gateway** ➔ **Power BI Dashboard**
