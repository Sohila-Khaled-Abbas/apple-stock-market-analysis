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

| Metric | Value / Observation |
| :--- | :--- |
| **Row Count** | ~11,300+ *(Approx. 252 trading days/year * 45 years)* |
| **Date Range** | `1980-12-12` to `2025-Q1` |
| **Missing Values** | Check for weekend gaps *(expected)* vs. midweek nulls *(errors).* |
| **Data Types** | Date (`Date/Object`), Prices (`Float64`), Volume (`Int64`) |
| **Outliers** | Massive volume spikes detected during the **1987 Black Monday**, **2000 Dotcom Collapse**, and **2020 COVID-19 Crash**. |

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
├── notebooks/             # Jupyter notebooks for data profiling (01_data_profiling.ipynb)
├── sql/                   # MySQL schema definitions and analytical queries
└── docs/                  # Project documentation and visualizations
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

2. Navigate to the project directory and install profiling tools:

   ```bash
   pip install pandas openpyxl jupyter
   ```

3. Run the profiling notebook:

   ```bash
   jupyter notebook notebooks/01_data_profiling.ipynb
   ```

4. Load the raw data from `data/raw/` into your standard MySQL Server setup using the scripts provided in `/sql/`.

5. Open the interactive dashboard found in `/dashboard/` with Power BI.
