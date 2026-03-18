# 🍏 Apple Stock Market Analysis (1980-2025)

[![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=Power%20BI&logoColor=black)](https://powerbi.microsoft.com/)
[![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> An end-to-end data engineering and analytics project analyzing 45 years of Apple Inc. (AAPL) historical stock market data to extract actionable business insights and investment strategies.

---

## 📑 Table of Contents

- [🍏 Apple Stock Market Analysis (1980-2025)](#-apple-stock-market-analysis-1980-2025)
  - [📑 Table of Contents](#-table-of-contents)
  - [🚀 Project Overview](#-project-overview)
  - [🏗️ Project Architecture](#️-project-architecture)
  - [📊 Data Profile Summary](#-data-profile-summary)
  - [💡 Business Recommendations](#-business-recommendations)
    - [1. The "Cook" Premium](#1-the-cook-premium)
    - [2. The "Buy the Dip" Signal](#2-the-buy-the-dip-signal)
    - [3. 2026 Outlook \& AI Hype](#3-2026-outlook--ai-hype)
  - [📂 Repository Structure](#-repository-structure)
  - [⚙️ Getting Started](#️-getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)

---

## 🚀 Project Overview

This project focuses on the ingestion, processing, and visualization of Apple’s stock market data spanning from **1980 to 2025**. By combining **Python** for initial profiling, **MySQL** for robust relational data storage and querying, and **Power BI** for interactive dashboards, this project highlights how historical market trends can inform future investment strategies.

---

## 🏗️ Project Architecture

1. **Data Profiling (Python/Pandas):** Initial dataset exploration, quality checking, and anomaly detection.
2. **Data Storage & Transformation (MySQL):** Aggregations, window functions for moving averages, and structured queries to prep the data for visualization.
3. **Interactive Visualization (Power BI):** Business intelligence dashboards that bring the "Cook Premium" and the "Buy the Dip" signals to life.

---

## 📊 Data Profile Summary

| Metric | Profile Result | Status |
| :--- | :--- | :--- |
| **Row Count** | `11,107` | Consistent with 44 years of trading |
| **Date Range** | `1980-12-12` to `2025-01-03` | Covers all major modern market cycles |
| **Missing Values** | 0 Nulls | High Quality |
| **Price Consistency** | High >= Low/Open/Close | 100% Logic Pass |
| **Volume Anomaly** | 1 row with 0 Volume (1981-08-10) | Needs imputation |
| **Adj Close Range** | $0.037 to $259.02 | Verified (Split-adjusted) |

**Quality Score:** 98% (Excellent completeness; only one minor volume anomaly detected).

---

## 💡 Business Recommendations

*Based on preliminary data profiling and historical analysis:*

### 1. The "Cook" Premium

Post-2011 (under Tim Cook's leadership), Apple's volatility steadily decreased while institutional ownership and share buybacks increased.

- **Recommendation for Portfolio Managers:** AAPL should be treated as a **"Core Equity"** (value/stability) rather than purely a **"Growth Speculation."**

### 2. The "Buy the Dip" Signal

Historical backtesting data shows a prominent and recurring pattern.

- **Recommendation:** A price drawdown of **>20%** while the **200-day Simple Moving Average (SMA)** remains upward-sloping has been a high-probability entry point for over 30 years.

### 3. 2026 Outlook & AI Hype

Looking ahead, based on the 2024-2025 "AI Hype" trend in the data:

- **Recommendation:** Monitor volume-to-price divergence closely. If trading volume *declines* while the stock price continues to hit new all-time highs, it serves as a strong technical suggestion for **partial profit-taking**.

---

## 📂 Repository Structure

```plaintext
├── data/                  # Datasets
│   ├── raw/               # Original, immutable datasets (CSV, Excel)
│   └── processed/         # Cleaned and transformed data for DB ingestion
├── dashboard/             # Power BI (.pbix) dashboard files
├── docs/                  # Technical documentation (e.g., data_pipeline.md)
├── notebooks/             # Jupyter notebooks
│   ├── 01_data_profiling.ipynb  # Initial EDA and assertions
│   └── 02_data_loading.ipynb    # Incremental data pipeline via yfinance
├── sql/                   # MySQL scripts for ELT
│   ├── 01_data_ingestion.sql    # Schema initialization and CSV bulk loading
│   ├── 02_data_cleaning.sql     # Validation, imputation, and anomaly checks
│   └── 03_eda_and_metrics.sql   # CAGR & Simple Moving Average tracking
├── requirements.txt       # Python dependencies
└── .gitignore             # Git ignore definitions
```

---

## ⚙️ Getting Started

### Prerequisites

- **Python 3.10+**
- **MySQL Server 8.0+**
- **Power BI Desktop**

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Sohila-Khaled-Abbas/apple-stock-analytics.git
   ```

2. Navigate to the project directory and install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the Database:
   - Execute `sql/01_data_ingestion.sql` in your MySQL environment to load the historical CSV.

4. Fetch the latest live data increments:
   - Run `notebooks/02_data_loading.ipynb` to automatically append new dates via the Yahoo Finance API.

5. Validate and calculate indicators:
   - Run `sql/02_data_cleaning.sql` to impute missing volumes and check logic.
   - Run `sql/03_eda_and_metrics.sql` to generate Moving Averages and CAGR metrics.

6. Launch Dashboard:
   - Open the interactive dashboard found in `/dashboard/` with Power BI.
