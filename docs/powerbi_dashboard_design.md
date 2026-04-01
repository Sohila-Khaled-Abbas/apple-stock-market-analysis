# Power BI Dashboard Design & Architecture Blueprint

[![Power BI](https://img.shields.io/badge/Power_BI_Desktop-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![PBIP Format](https://img.shields.io/badge/Format-.pbip_Project-0078D4?style=for-the-badge&logo=microsoftpowerpoint&logoColor=white)](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
[![TMDL](https://img.shields.io/badge/Semantic_Model-TMDL-00BCF2?style=for-the-badge&logo=databricks&logoColor=white)](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview)
[![DAX](https://img.shields.io/badge/DAX-47_Measures-FF6B35?style=for-the-badge&logo=microsoftexcel&logoColor=white)](#dax-measure-catalogue)
[![Python](https://img.shields.io/badge/Python-Power_Query_Embedded-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-python-scripts)
[![MySQL](https://img.shields.io/badge/MySQL-Source_Database-005C84?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Deneb](https://img.shields.io/badge/Deneb-Vega_Lite_Charts-0078D4?style=for-the-badge&logo=vega&logoColor=white)](https://deneb-viz.github.io/)

> A financial dashboard must go beyond being a mere "database GUI" — it must present a visual argument. The semantic model and visualization layers are strictly separated, highly performant, and structurally sound. This document serves as the **definitive deployment checklist** to assemble the distinct codebases, external UDF libraries, and optimized data models into a cohesive, web-tier financial application.

---

## 📑 Table of Contents

- [Phase 0: Project Format \& Version Control](#phase-0-project-format--version-control)
- [Phase 1: The Semantic Model (Backend)](#phase-1-the-semantic-model-backend)
  - [Star Schema Architecture](#star-schema-architecture)
  - [Table Reference](#table-reference)
  - [Model Relationships](#model-relationships)
  - [Power Query (M) Data Transformations](#power-query-m-data-transformations)
- [Phase 2: Data Model Optimization](#phase-2-data-model-optimization)
- [Phase 3: UDF Libraries Installation](#phase-3-udf-libraries-installation)
- [Phase 4: Page Assembly (7 Pages)](#phase-4-page-assembly-7-pages)
  - [Page 1 — Home (Landing Page)](#page-1--home-landing-page)
  - [Page 2 — Executive Macro View](#page-2--executive-macro-view)
  - [Page 3 — Technical \& Momentum Deep Dive](#page-3--technical--momentum-deep-dive)
  - [Pages 4–5 — Hidden Tooltip Layers](#pages-45--hidden-tooltip-layers)
  - [Pages 6–7 — Additional Analytics Pages](#pages-67--additional-analytics-pages)
- [DAX Measure Catalogue](#dax-measure-catalogue)
  - [01 — Price \& Volume](#01--price--volume)
  - [02 — Returns \& Performance](#02--returns--performance)
  - [03 — Technical Indicators](#03--technical-indicators)
  - [04 — Risk \& Drawdown](#04--risk--drawdown)
  - [05 — Benchmark \& Market (S\&P 500)](#05--benchmark--market-sp-500)
  - [06 — Deneb Chart Data](#06--deneb-chart-data)
  - [07 — KPI Cards (HTML)](#07--kpi-cards-html)
  - [08 — SVG \& Tooltips](#08--svg--tooltips)
  - [09 — Page HTML \& Navigation](#09--page-html--navigation)
  - [10 — Filters \& Titles](#10--filters--titles)
  - [11 — Metadata](#11--metadata)
- [Appendix: Key DAX Snippets](#appendix-key-dax-snippets)

---

## Phase 0: Project Format & Version Control

[![PBIP](https://img.shields.io/badge/File_Format-.pbip-0078D4?style=flat-square&logo=microsoft&logoColor=white)](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
[![Git](https://img.shields.io/badge/Version_Control-Git_Enabled-F05032?style=flat-square&logo=git&logoColor=white)](https://git-scm.com/)

To enable proper source control and separation of the data model from the UI layer, this project uses the **Power BI Project (`.pbip`)** format rather than a monolithic `.pbix` file.

### Dashboard Repository Structure

```
dashboard/
├── Apple-AAPL-Stock-Market-Analysis-Dashboard.pbip       ← Open this to edit
├── Apple-AAPL-Stock-Market-Analysis-Dashboard.pbix       ← Compiled snapshot
│
├── Apple-AAPL-Stock-Market-Analysis-Dashboard.Report/    ← Frontend (UI Layer)
│   ├── definition/
│   │   ├── report.json                                   ← Global report settings
│   │   ├── version.json
│   │   └── pages/                                        ← 7 report pages (JSON)
│   │       ├── e27774228289ca9fe100/  (Home)
│   │       ├── 3244a5c5ada8b5854b5a/  (Macro View)
│   │       ├── ca8e0f16a462c76d7abe/  (Technical View)
│   │       ├── 371ac19207831651e86f/  (Tooltip / Hidden)
│   │       ├── bed9852626b0e92ebdda/  (Tooltip / Hidden)
│   │       ├── a2ee985a02561e2f16aa/  (Analytics Page)
│   │       └── 75bf5858e393f5ad8802/  (Analytics Page)
│   └── StaticResources/
│
├── Apple-AAPL-Stock-Market-Analysis-Dashboard.SemanticModel/  ← Backend (Data Model)
│   ├── definition/
│   │   ├── model.tmdl                                    ← Model-level settings
│   │   ├── relationships.tmdl                            ← Table relationships
│   │   ├── functions.tmdl                                ← Injected UDF libraries
│   │   ├── tables/
│   │   │   ├── aapl_daily.tmdl                           ← Primary fact table
│   │   │   ├── sp500_daily.tmdl                          ← Benchmark fact table
│   │   │   ├── Calendar.tmdl                             ← Date dimension
│   │   │   ├── _Measures.tmdl                            ← All 47 DAX measures
│   │   │   ├── Technical_Metrics.tmdl                    ← Python-computed indicators
│   │   │   └── Data Dictionary.tmdl                      ← Auto-generated data catalog
│   │   └── cultures/en-US/
│   ├── DAXQueries/                                       ← Saved DAX Query View scripts
│   └── diagramLayout.json                                ← Model diagram layout
│
└── theme/                                                ← Custom JSON theme & assets
```

> **Workflow:** Always open the `.pbip` file. Changes save as human-readable TMDL/JSON, enabling full Git diff tracking.

---

## Phase 1: The Semantic Model (Backend)

### Star Schema Architecture

```
                    ┌─────────────────────────────┐
                    │         Calendar             │  (Dimension)
                    │  Date · Year · Quarter       │
                    │  MonthName · Decade          │
                    │  CEO Era · IsWeekend         │
                    └─────────────┬───────────────┘
                                  │ 1:N (both sides)
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       │                       ▼
┌──────────────────┐              │             ┌──────────────────┐
│   aapl_daily     │◄─────────────┤             │   sp500_daily    │
│  (Fact: AAPL)    │  related by  │             │  (Fact: Market)  │
│  Trade_Date (PK) │  Trade_Date  │             │  Trade_Date (PK) │
│  OHLCV + Spreads │              │             │  SP500_Close     │
│  Calc. Columns   │              │             │  Historical_Return│
└────────┬─────────┘              │             └──────────────────┘
         │ 1:M (non-filtering)    │
         ▼                        │
┌──────────────────┐              │
│ Technical_Metrics│              │
│  (Derived Table) │              │
│  Trade_Date (FK) │              │
│  50-Day SMA      │              │
│  200-Day SMA     │              │
│  RSI (14-Day)    │              └──► _Measures (hidden — all DAX)
└──────────────────┘                  Data Dictionary (reference)
```

### Table Reference

| Table | Type | Rows | Source | Key Columns |
|:------|:-----|:----:|:-------|:------------|
| `aapl_daily` | Fact | ~11,400+ | MySQL `apple_stock_db` | `Trade_Date` (PK), OHLCV, computed spreads, calc. columns |
| `sp500_daily` | Fact | ~11,400+ | yfinance Python API | `Trade_Date` (PK), `SP500_Close`, `Historical_SP500_Return` |
| `Calendar` | Dimension | ~16,000 | Power Query (generated) | `Date` (PK), `CEO Era`, `Decade`, `IsWeekend` |
| `Technical_Metrics` | Derived Fact | ~11,200+ | aapl_daily → Python script | `Trade_Date` (FK), `50-Day SMA`, `200-Day SMA`, `RSI (14-Day)` |
| `_Measures` | Measure Table | 0 rows | Empty placeholder | Houses all 47 DAX measures |
| `Data Dictionary` | Reference | ~40 rows | DAX `DATATABLE` | Auto-generated measure/column catalog |

### Model Relationships

```
aapl_daily[Trade_Date]        → Calendar[Date]          (Many-to-One, active)
sp500_daily[Trade_Date]       → Calendar[Date]          (Many-to-One, active)
Technical_Metrics[Trade_Date] → aapl_daily[Trade_Date]  (Many-to-One, active, no RI check)
```

> **Note:** `Technical_Metrics` links to `aapl_daily` directly (not `Calendar`) because it is a derived view of fact data. The `relyOnReferentialIntegrity` flag is set on the `aapl_daily → Calendar` and `sp500_daily → Calendar` relationships for VertiPaq compression optimization.

### Power Query (M) Data Transformations

#### `aapl_daily` — MySQL → Power Query

[![MySQL](https://img.shields.io/badge/Source-MySQL_localhost-005C84?style=flat-square&logo=mysql&logoColor=white)]()

The `aapl_daily` table is sourced from `MySQL.Database("localhost", "apple_stock_db")` and enriched exclusively within Power Query:

| Step | Added Column | Logic |
|:-----|:-------------|:------|
| 1 | `Intraday_Spread_Pct` | `(High - Low) / Open` — formatted as Percentage |
| 2 | `Candlestick_Direction` | `IF Close > Open THEN "Bullish" ELSE IF Close < Open THEN "Bearish" ELSE "Doji (Flat)"` |
| 3 | `Intraday_Return_Pct` | `(Close - Open) / Open` — formatted as Percentage |
| 4 | `Daily_Spread_USD` | `High - Low` — formatted as Number |
| 5 | `Open_Placement` | `IF Open >= High THEN "Gap Up / High Open" ELSE IF Open <= Low THEN "Gap Down / Low Open" ELSE "Inside Range"` |

#### `sp500_daily` — Python → Power Query

[![yfinance](https://img.shields.io/badge/Source-yfinance_API-720e9e?style=flat-square&logo=yahoo&logoColor=white)]()

The `sp500_daily` table bypasses MySQL entirely via an **embedded Python script** in Power Query:

```python
import yfinance as yf
import pandas as pd

df = yf.download('^GSPC', start='1980-12-12', progress=False)
df.reset_index(inplace=True)
df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
df.rename(columns={'Date': 'Trade_Date', 'Close': 'SP500_Close'}, inplace=True)
df = df[['Trade_Date', 'Open', 'High', 'Low', 'SP500_Close', 'Volume']]
```

> The OHLCV columns (except `SP500_Close`) are hidden in the field list to declutter model noise.

#### `Technical_Metrics` — Derived via Python in Power Query

[![Python](https://img.shields.io/badge/Engine-Power_Query_Python-3776AB?style=flat-square&logo=python&logoColor=white)]()

This table starts from `aapl_daily[Close_Price]`, runs a Python script via `Python.Execute()` to compute:

- **`50-Day SMA`** — `Close_Price.rolling(window=50).mean()`
- **`200-Day SMA`** — `Close_Price.rolling(window=200).mean()`
- **`RSI (14-Day)`** — Wilder's Smoothing EWM method: `100 - (100 / (1 + avg_gain/avg_loss))`

> The first 200 rows (mathematically incomplete warm-up period) are **dropped** via `dropna()` before the table is returned to Power BI.

#### `Calendar` — Dynamically Generated

The Calendar table is fully generated in Power Query from the `aapl_daily` date bounds:

| Column | Logic |
|:-------|:------|
| `Date` | Continuous date sequence from `MIN` to `MAX` of `aapl_daily[Trade_Date]` |
| `Year`, `Quarter`, `MonthNumber`, `MonthName` | Standard date decomposition |
| `DayOfWeek` | 0 = Monday … 6 = Sunday |
| `IsWeekend` | `DayOfWeek >= 5` |
| `Decade` | e.g., `"1980s"`, `"1990s"` |
| `CEO Era` | Apple-specific business era labels — see below |

**CEO Era Definitions:**

| Era Label | Date Range |
|:----------|:-----------|
| `Markkula Era (Early Days)` | Before Apr 8, 1983 |
| `Sculley Era (Mac Intro)` | Apr 8, 1983 – Jun 18, 1993 |
| `Spindler/Amelio Era (Struggle)` | Jun 18, 1993 – Jul 9, 1997 |
| `Jobs Era (iPod/iPhone)` | Jul 9, 1997 – Aug 24, 2011 |
| `Cook Era (Services/Scale)` | Aug 24, 2011 – Present |

---

## Phase 2: Data Model Optimization

[![VertiPaq](https://img.shields.io/badge/Engine-VertiPaq_Optimized-00BCF2?style=flat-square&logo=microsoft&logoColor=white)]()
[![O(N)](https://img.shields.io/badge/Complexity-O(N)_Column_Scans-30d158?style=flat-square)]()

> ⚠️ **Critical:** Do NOT attempt to render complex visuals without materializing heavy statistical calculations into Calculated Columns. Skipping this causes O(N²) VertiPaq engine timeouts on 11,000+ row datasets.

### Calculated Columns — `aapl_daily`

| Column | DAX Logic | Purpose |
|:-------|:----------|:--------|
| `Historical_Daily_Return` | `DIVIDE(Adj_Close - PreviousAdj_Close, PreviousAdj_Close)` | Pre-materializes daily return for volatility/beta measures |
| `Historical_Rolling_Max` | `MAX(Adj_Close) over all dates ≤ CurrentDate` | Rolling ATH — base for Drawdown (hidden in field list) |
| `Historical_Drawdown` | `DIVIDE(Adj_Close - Rolling_Max, Rolling_Max)` | Peak-to-trough decline percentage |

### Calculated Columns — `sp500_daily`

| Column | DAX Logic | Purpose |
|:-------|:----------|:--------|
| `Historical_SP500_Return` | `DIVIDE(SP500_Close - PreviousClose, PreviousClose)` | Pre-materializes S&P 500 daily return for Beta regression |

> **Performance Impact:** The original `Beta (AAPL to Market)` measure used `FILTER(ALLSELECTED(...))` causing ~2,900ms FE latency. Using pre-materialized columns reduces this to ~5ms — a **580x speedup**.

---

## Phase 3: UDF Libraries Installation

[![TabularEditor](https://img.shields.io/badge/Tabular_Editor-TMDL_Import-brightgreen?style=flat-square&logo=databricks&logoColor=white)](https://tabulareditor.com/)

Install the following UDF libraries via Tabular Editor (`.tmdl` scripts in `functions.tmdl`):

| Library | Badge | Function Used | Purpose |
|:--------|:------|:--------------|:--------|
| `PowerofBI.IBCS` | [![IBCS](https://img.shields.io/badge/IBCS-Variance_Bars-red?style=flat-square)]() | `.BarChart.AbsoluteVariance()` | Year-over-Year absolute variance delta bars in matrices |
| `SavoryData.Selection2List` | [![SavoryData](https://img.shields.io/badge/SavoryData-Filter_Text-blue?style=flat-square)]() | `.Text2List_MaxNumberOfElements_TextColumnName()`, `.Date2List()` | Converts slicer selections to human-readable strings |
| `DaxLib.SVG` | [![DaxLib](https://img.shields.io/badge/DaxLib-SVG_Charts-orange?style=flat-square)]() | `.Viz.Area()`, `.Viz.Boxplot()` | Area sparklines and boxplots as ImageUrl data URIs |
| `XU.SVG.Progress` | [![XU](https://img.shields.io/badge/XU-Progress_Bars-purple?style=flat-square)]() | Progress donuts & capsule bars | Tooltip report page visual encoding |
| `PiotrBartela.TitleContext` | [![PiotrBartela](https://img.shields.io/badge/PiotrBartela-Dynamic_Titles-teal?style=flat-square)]() | `.Period()`, `.Filtered()` | Converts slicer inputs to "Last 5 Years" narrative strings |

> **Data Category Enforcement (Critical):** After installing, select every measure that outputs HTML or SVG in `_Measures`. In Measure Tools → Data Category → set to **Image URL**.

---

## Phase 4: Page Assembly (7 Pages)

[![Canvas](https://img.shields.io/badge/Canvas_Size-1920×1080-000000?style=flat-square&logo=figma&logoColor=white)]()
[![Theme](https://img.shields.io/badge/Theme-Dark_Mode_%23000000-1d1d1f?style=flat-square)]()

> **For every HTML Content visual:** Go to Format Pane → General → Effects → turn **Background OFF** and **Visual Border OFF**.

### Page 1 — Home (Landing Page)

`Page ID: e27774228289ca9fe100`

| Element | Specification |
|:--------|:-------------|
| Canvas | Standard · 1920×1080 · Zero background |
| HTML Visual | Full-screen (W: 1920, H: 1080, X: 0, Y: 0) |
| Measure | `Landing Page HTML` |
| Navigation | Blank Button overlaid on "Enter Analytics Dashboard" CTA → **Action: Page Navigation → Macro View** |

**Landing Page HTML Features:**
- Apple SVG logo with `fadeUp` CSS3 keyframe animation
- Dynamic metric cards: Dataset Horizon (from `Last Refresh Date`), Total Trading Days, Historical ATH
- GitHub + Google Slides nav links with hover state transitions
- CTA button with `pulseGlow` animation on hover
- Glassmorphism cards (`.metric-card`) with cubic-bezier transitions

---

### Page 2 — Executive Macro View

`Page ID: 3244a5c5ada8b5854b5a`

| Zone | Visual | Size (W×H) | Position (X, Y) | Measure |
|:-----|:-------|:----------:|:---------------:|:--------|
| Left Sidebar | HTML Content | 240×1080 | 0, 0 | `Sidebar Navigation HTML` (`VAR ActivePage = "Macro"`) |
| Top Header | HTML Content | 1680×90 | 240, 0 | `Header - Macro View HTML` |
| Slicer Strip | Native Slicers | — | Below header | `CEO Era` (Dropdown) · `Date` (Between) |
| KPI #1 | HTML Content | 400×120 | 240, 160 | `KPI - Latest Price` |
| KPI #2 | HTML Content | 400×120 | 640, 160 | `KPI - CAGR` (with SP500 benchmark) |
| KPI #3 | HTML Content | 400×120 | 1040, 160 | `KPI - Sharpe Ratio` (color-coded) |
| KPI #4 | HTML Content | 400×120 | 1440, 160 | `KPI - Max Drawdown` |
| Price Chart | Native Line Chart | 1000×740 | 240, 300 | `Latest Price` — Logarithmic Y-Axis · Legend: `CEO Era` |
| Decade Matrix | HTML Content | 640×740 | 1260, 300 | `HTML - Decade Summary Table` (inline SVG sparklines + boxplots) |

**Header Context Chips:** `Active Segment` (Era filter via PiotrBartela) · `Market Horizon` (date range) · `Latest Close` (price)

---

### Page 3 — Technical & Momentum Deep Dive

`Page ID: ca8e0f16a462c76d7abe`

| Zone | Visual | Measure |
|:-----|:-------|:--------|
| Left Sidebar | HTML Content | `Sidebar Navigation HTML 2` (`VAR ActivePage = "Technical"`) |
| Top Header | HTML Content | `Header - Technical View HTML` (shows Period Volatility chip) |
| Date Slicer | Relative Date Slicer | Default: Last 1 Year |
| Date Badge | Native Pill Button | Text: `Button Text - Active Dates` (SavoryData) |
| KPI Strip | 3 × HTML Content | `KPI - Volatility` · `KPI - RSI` · `KPI - Trend State` |
| Price Chart | Native Line | `Latest Price` + `50-Day SMA` + `200-Day SMA` |
| Volume Chart | Stacked Column | `Volume` with `Is Volume Surge` conditional formatting |
| RSI Oscillator | Native Line | `RSI (14-Day)` — Y-axis reference lines at 30 and 70 |
| Advisory Engine | HTML Content | `Dynamic Business Recommendation` (footer) |

**Quantitative Advisory Logic (`Dynamic Business Recommendation`):**

| Market State | Condition | Action Signal |
|:------------|:----------|:-------------|
| Severe Capitulation | Death Cross + RSI ≤ 30 | Monitor for institutional accumulation |
| Macro Downtrend | Death Cross + RSI > 30 | Capital preservation — avoid accumulation |
| Overbought Bull | Golden Cross + RSI ≥ 70 | Hold — delay new capital deployment |
| Healthy Bull | Golden Cross + RSI < 70 | Favorable accumulation window |

---

### Pages 4–5 — Hidden Tooltip Layers

[![Tooltip](https://img.shields.io/badge/Pages-Hidden_Tooltip_Report_Pages-555?style=flat-square)]()

#### Tooltip Page — Macro (`Tooltip_Macro`)

- **Canvas:** Tooltip type · 320×240 · Background `#1d1d1f` (0% transparency)
- **Measure:** `HTML Tooltip - Macro`
- **Content:** Date header · Closing price + day % change · Drawdown progress bar · 200-Day SMA premium/discount
- **Linked to:** Price Action Line Chart on Macro View page

#### Tooltip Page — Technical (`Tooltip_Tech`)

- **Canvas:** Tooltip type · 320×300 · Background `#1d1d1f`
- **Measures:** `HTML Tooltip - RSI Enriched` · `HTML Tooltip - Tech`
- **Content:** RSI value + day-over-day delta · Color-coded RSI heat bar (0–30 green, 70–100 red) · Intraday spread · Volume traded
- **Linked to:** Technical charts on Page 3

---

### Pages 6–7 — Additional Analytics Pages

`Page IDs: a2ee985a02561e2f16aa · 75bf5858e393f5ad8802`

These pages extend the dashboard with advanced financial analytics:

- **Deneb Candlestick Chart** powered by `Trade Date Key`, `Is Trading Day` measures (filtered to exclude weekends/holidays to prevent flat-step artifacts)
- **Volume-at-Price Analysis** via `Deneb - VAP Chart JSON` (Vega-Lite spec embedded directly in Deneb visual)
- **IBCS YoY Variance Chart** (`IBCS YoY Variance Chart`) — standardized absolute variance bars (YoY Avg Price AC vs PY) using IBCS notation

---

## DAX Measure Catalogue

> All 47 measures reside in the `_Measures` table. Organized by Display Folder. Measures with `/// ...` comments are documented in the semantic model.

### 01 — Price & Volume

[![Folder](https://img.shields.io/badge/Display_Folder-01_Price_%26_Volume-2997ff?style=flat-square)]()

| Measure | Format | Description |
|:--------|:-------|:------------|
| `Latest Price` | `$#,0.00` | Most recent adjusted closing price — skips non-trading days via `LASTNONBLANK` |
| `Avg Price AC` | `$#,0.00` | Average adjusted close for the selected context (Actual) |
| `Avg Price PY` | `$#,0.00` | Average adjusted close for the equivalent prior-year period |
| `30-Day Avg Volume` | Number | Rolling 30-day average volume via `DATESINPERIOD` |
| `Is Volume Surge` | Integer (0/1) | `1` if current volume > 2× trailing 30-day average |

### 02 — Returns & Performance

[![Folder](https://img.shields.io/badge/Display_Folder-02_Returns_%26_Performance-30d158?style=flat-square)]()

| Measure | Format | Description |
|:--------|:-------|:------------|
| `Total Return %` | `0.00%` | Absolute % return from first to last trading day in context |
| `CAGR` | `0.00%` | Compound Annual Growth Rate — `(EndPrice/StartPrice)^(1/Years) - 1` |
| `Daily Return %` | `0.00%` | Day-over-day % change — reads pre-materialized `Historical_Daily_Return` column |
| `Sharpe Ratio` | `0.00` | Risk-free rate = 4% · `(CAGR - 0.04) / AnnualizedVolatility` |
| `Alpha (Annualized)` | `0.00%` | Jensen's Alpha — actual CAGR minus CAPM-expected return |

### 03 — Technical Indicators

[![Folder](https://img.shields.io/badge/Display_Folder-03_Technical_Indicators-ff9f0a?style=flat-square)]()

| Measure | Format | Description |
|:--------|:-------|:------------|
| `50-Day SMA` | `0.00` | `AVERAGE(Technical_Metrics[50-Day SMA])` |
| `200-Day SMA` | `0.00` | `AVERAGE(Technical_Metrics[200-Day SMA])` |
| `RSI (14-Day)` | `0.00` | `AVERAGE(Technical_Metrics[RSI (14-Day)])` |
| `Trend State` | Text | `"Bullish (Golden)"` if SMA50 > SMA200, else `"Bearish (Death)"` |
| `Annualized Volatility` | `0.00%` | `STDEV.S(Historical_Daily_Return) × √252` |
| `Beta (AAPL to Market)` | `0.00` | Linear regression slope via `LINESTX` on materialized return columns |

### 04 — Risk & Drawdown

[![Folder](https://img.shields.io/badge/Display_Folder-04_Risk_%26_Drawdown-ff453a?style=flat-square)]()

| Measure | Format | Description |
|:--------|:-------|:------------|
| `Daily Drawdown %` | `0.00%` | `AVERAGE(aapl_daily[Historical_Drawdown])` |
| `Max Drawdown` | `0.00%` | `MIN(aapl_daily[Historical_Drawdown])` — worst peak-to-trough |
| `Days Since ATH` | Integer | Calendar days since the price reached its rolling maximum |

### 05 — Benchmark & Market (S&P 500)

[![Folder](https://img.shields.io/badge/Display_Folder-05_Benchmark_%26_Market-64d2ff?style=flat-square)]()

| Measure | Format | Description |
|:--------|:-------|:------------|
| `SP500 Latest Price` | `$#,0.00` | Latest S&P 500 closing price via `LASTNONBLANK` |
| `SP500 CAGR` | `0.00%` | S&P 500 CAGR — benchmark denominator for Alpha |
| `SP500 Daily Return %` | `0.00%` | Reads pre-materialized `Historical_SP500_Return` column |

### 06 — Deneb (Chart Data)

[![Deneb](https://img.shields.io/badge/Display_Folder-06_Deneb_Chart_Data-0078D4?style=flat-square)]()

These measures feed Vega-Lite specifications in Deneb custom visuals. All return `BLANK()` on non-trading days to prevent rendering artifacts.

| Measure | Format | Purpose |
|:--------|:-------|:--------|
| `Is Trading Day` | Integer (0/1) | Filter flag — 1 only when AAPL data exists for the date |
| `Trade Date Key` | Text (`YYYY-MM-DD`) | X-axis date string for Deneb transforms |
| `RSI (14-Day) Deneb` | `0.00` | RSI restricted to trading days only |
| `50-Day SMA Deneb` | `0.00` | SMA50 restricted to trading days only |
| `200-Day SMA Deneb` | `0.00` | SMA200 restricted to trading days only |
| `Daily Drawdown % Deneb` | `0.00%` | Drawdown restricted to trading days only |
| `Deneb - VAP Chart JSON` | Text | Placeholder — Vega spec lives directly in Deneb visual |

### 07 — KPI Cards (HTML)

[![Folder](https://img.shields.io/badge/Display_Folder-07_KPI_Cards-ff9f0a?style=flat-square)]()

Each KPI measure outputs a self-contained HTML card with inline CSS. All use `dataCategory: ImageUrl` for rendering.

| Measure | Color Accent | Content |
|:--------|:------------|:--------|
| `KPI - Latest Price` | `#2997ff` (Blue) | Latest adjusted close price |
| `KPI - CAGR` | `#30d158` (Green) | AAPL CAGR + SP500 benchmark comparison |
| `KPI - Sharpe Ratio` | Dynamic (green/orange/red by value) | Risk-adjusted ratio with threshold coloring |
| `KPI - Max Drawdown` | `#ff453a` (Red) | Maximum peak-to-trough decline |
| `KPI - Volatility` | `#ff9f0a` (Orange) | Annualized volatility percentage |
| `KPI - RSI` | Dynamic (per threshold) | RSI value + OVERBOUGHT/OVERSOLD/NEUTRAL badge |
| `KPI - Trend State` | Dynamic (by trend) | Golden Cross / Death Cross state |
| `Dynamic Business Recommendation` | `#2997ff` border | Multi-scenario narrative advisory paragraph |

### 08 — SVG & Tooltips

[![Folder](https://img.shields.io/badge/Display_Folder-08_SVG_%26_Tooltips-86868b?style=flat-square)]()

| Measure | Data Category | Purpose |
|:--------|:-------------|:--------|
| `SVG Sparkline - Price Trend` | `ImageUrl` | Area sparkline in blue (`#2997ff`) — 160×45px for matrix cells |
| `SVG Boxplot - Daily Returns` | `ImageUrl` | Orange boxplot with outliers (`#ff9f0a`) — 160×45px |
| `HTML Tooltip - Macro` | — | Rich HTML tooltip: price, day return %, drawdown bar, SMA premium |
| `HTML Tooltip - RSI Enriched` | — | RSI with day-over-day delta, momentum bar, closing price context |
| `HTML Tooltip - Tech` | — | RSI + intraday spread + daily volume |

### 09 — Page HTML & Navigation

[![Folder](https://img.shields.io/badge/Display_Folder-09_Page_HTML_%26_Navigation-1d1d1f?style=flat-square)]()

| Measure | Description |
|:--------|:------------|
| `Landing Page HTML` | Full-screen Apple-style landing page with CSS3 animations, metric cards, and CTA |
| `Sidebar Navigation HTML` | Left nav sidebar for Macro View — `VAR ActivePage = "Macro"` |
| `Sidebar Navigation HTML 2` | Left nav sidebar for Technical View — `VAR ActivePage = "Technical"` |
| `Header - Macro View HTML` | Top header bar with globe icon, context chips, and latest close price |
| `Header - Technical View HTML` | Top header bar with chart icon and volatility chip |
| `HTML - Decade Summary Table` | Full custom HTML table with inline SVG sparklines & boxplots (replaces native matrix) |

### 10 — Filters & Titles

[![Folder](https://img.shields.io/badge/Display_Folder-10_Filters_%26_Titles-000000?style=flat-square)]()

| Measure | Description |
|:--------|:------------|
| `Filter Text - CEO Era` | SavoryData: converts CEO Era slicer to text string, max 3 items before "…" |
| `Filter Text - Dates` | SavoryData: converts Date slicer to readable range string |
| `Button Text - Active Dates` | `"🗓️ Horizon: " & [Filter Text - Dates]` — for native Pill Button |
| `Title - Macro Price Chart` | Dynamic narrative: "YTD", "Last N Years", or "YYYY – YYYY" |
| `Title - Native Price` | Chart title including active CEO Era filter |
| `Title - Decade Matrix` | Matrix title including active CEO Era filter |
| `Title - Decadal Volume` | Volume chart title including active CEO Era filter |
| `Title - Native RSI` | RSI chart title including active CEO Era filter |

### 11 — Metadata

[![Folder](https://img.shields.io/badge/Display_Folder-11_Metadata-555?style=flat-square)]()

| Measure | Format | Description |
|:--------|:-------|:------------|
| `Last Refresh Date` | `MMMM dd, yyyy` | `FORMAT(MAX(aapl_daily[Trade_Date]), ...)` — latest physical record |
| `Last Refresh Date Button` | Text | `"Data Current as of: " & [Last Refresh Date]` |

---

## Appendix: Key DAX Snippets

### IBCS YoY Variance Chart

```dax
IBCS YoY Variance Chart =
PowerofBI.IBCS.BarChart.AbsoluteVariance(
    'Calendar'[Year],                                         -- dimensionColumn
    [Avg Price AC],                                           -- mainValueExpr (Actuals)
    BLANK(),                                                  -- secondValueExpr (Forecast — unused)
    [Avg Price PY],                                           -- baseValueExpr (Prior Year)
    CALCULATE([Avg Price AC], ALLSELECTED('Calendar'[Year])), -- scaleValueExpr (for bar width)
    "grey",                                                   -- baseType (IBCS standard for PY)
    NOT(ISINSCOPE('Calendar'[Year])),                         -- totalRow
    FORMAT([Avg Price AC] - [Avg Price PY], "+$#,0.00;-$#,0.00;$0.00"), -- dataLabel
    250,                                                      -- imageWidth
    35,                                                       -- imageHeight
    1                                                         -- businessImpact (1 = Positive = Green)
)
```

### Beta (AAPL to Market) — Linear Regression via LINESTX

```dax
Beta (AAPL to Market) =
-- 1. Build a virtual table from the materialized return columns
VAR ReturnTable =
    FILTER(
        ADDCOLUMNS(
            VALUES('Calendar'[Date]),
            "AssetReturn",  CALCULATE(MAX(aapl_daily[Historical_Daily_Return])),
            "MarketReturn", CALCULATE(MAX(sp500_daily[Historical_SP500_Return]))
        ),
        NOT(ISBLANK([AssetReturn])) && NOT(ISBLANK([MarketReturn]))
    )
-- 2. Run OLS linear regression
VAR RegressionTable = LINESTX(ReturnTable, [AssetReturn], [MarketReturn])
-- 3. Extract slope (Beta coefficient)
RETURN MAXX(RegressionTable, [Slope1])
```

### Days Since ATH — Optimized via Pre-materialized Column

```dax
Days Since ATH =
// OPTIMIZED: Historical_Rolling_Max pre-materialized at Python load time.
// Old O(N²) FILTER(ALLSELECTED) version caused ~2,900ms FE latency.
// This version uses pure Storage Engine scan = ~5ms.
VAR CurrentDate     = MAX('Calendar'[Date])
VAR CurrentPrice    = [Latest Price]
VAR RollingMaxPrice = CALCULATE(
    MAX(aapl_daily[Historical_Rolling_Max]),
    FILTER(ALLSELECTED('Calendar'[Date]), 'Calendar'[Date] <= CurrentDate)
)
VAR DateOfMaxPrice  = CALCULATE(
    MAX(aapl_daily[Trade_Date]),
    aapl_daily[Historical_Rolling_Max] = RollingMaxPrice,
    FILTER(ALLSELECTED('Calendar'[Date]), 'Calendar'[Date] <= CurrentDate)
)
RETURN
    IF(
        ISBLANK(CurrentPrice) || ISBLANK(RollingMaxPrice), BLANK(),
        IF(CurrentPrice >= RollingMaxPrice, 0, DATEDIFF(DateOfMaxPrice, CurrentDate, DAY))
    )
```

---

*For the data pipeline architecture, automation scripts, and the full repository structure, refer to the [README](../README.md).*
