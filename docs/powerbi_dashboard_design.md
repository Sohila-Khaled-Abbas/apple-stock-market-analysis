# Power BI Dashboard Design & Architecture Blueprint

A financial dashboard must go beyond being a mere "database GUI"; it must present a visual argument. The semantic model and visualization layers are strictly separated, highly performant, and structurally sound. This document serves as the definitive deployment checklist to assemble the distinct codebases, external UDF libraries, and optimized data models into a cohesive, web-tier financial application.

## Phase 0: Project Format & Version Control

To enable proper source control and separation of the data model from the UI layer, this project utilizes the **Power BI Project (.pbip)** format rather than a monolithic `.pbix` file.

1. **Dashboard Repository Structure:** The `dashboard/` directory contains the `.pbip` file alongside two main folders:
    * `Apple-AAPL-Stock-Market-Analysis-Dashboard.SemanticModel/`: Contains the DAX measures, table definitions, and relationships (the backend).
    * `Apple-AAPL-Stock-Market-Analysis-Dashboard.Report/`: Contains the JSON-based visual canvas, pages, and interactive elements (the frontend).
2. **Development Workflow:** Always open the `.pbip` file to edit the project. Changes will be saved as human-readable text files in their respective folders, enabling strict Git version control.

## Phase 1: The Environment & Foundation

Before placing a single visual on the canvas, the underlying environment must be strictly controlled.

1. **Apply the JSON Theme:** Import your `Apple_Stock_Theme.json` file. This locks your report canvas to a 1920x1080 resolution and enforces the global `#000000` dark mode background.
2. **Install the UDF Libraries:** Ensure your Tabular Editor TMDL scripts have successfully injected the following libraries into your semantic model:
    * `PowerofBI.IBCS` (For absolute variance bars)
    * `SavoryData.Selection2List` (For dynamic slicer text extraction)
    * `DaxLib.SVG` (For sparklines and boxplots)
    * `XU.SVG.Progress` (For tooltip progress bars and donuts)
    * `PiotrBartela.TitleContext` (For presentation-style date and filter narratives)
3. **Data Category Enforcement (Critical):** Go to your `_Measures` table. Select every measure that outputs HTML or SVG code (Headers, KPIs, Sparklines, Boxplots, IBCS charts, Tooltips). In the Measure Tools ribbon, you **must** change the Data Category from "Uncategorized" to **Image URL**. 

## Phase 2: Data Model Optimization

Do not attempt to render visuals without materializing your heavy statistical calculations. If you skip this, the VertiPaq engine will time out ($O(N^2)$ iteration failure).

1. **`aapl_daily` Calculated Columns:** Ensure you have physical columns for `Historical_Daily_Return`, `Historical_Rolling_Max`, and `Historical_Drawdown`.
2. **`sp500_daily` Calculated Columns:** Ensure you have the physical column for `Historical_SP500_Return`.
3. Verify that your measures for `Annualized Volatility`, `Max Drawdown`, and `Beta (AAPL to Market)` have been updated to read from these static columns rather than iterating over the entire calendar table.

## Phase 3: Page Assembly

For every **HTML Content** visual used in this phase, you must go to the Format Pane > General > Effects and turn **Background OFF** and **Visual Border OFF**.

### Act I: The Landing Page (`Home`)
1. **Canvas:** Set to standard page, zero background.
2. **The Visual:** Add an HTML Content visual covering the entire screen (Width: 1920, Height: 1080, X: 0, Y: 0).
3. **The Measure:** Drop in `Landing Page HTML`.
4. **The Route:** Insert a native Power BI **Blank Button**. Strip its formatting (no fill, no border, no icon). Place it perfectly over the "Enter Analytics Dashboard" UI element. Set the button Action to `Page Navigation -> Macro View`.

### Act II: Executive Macro View (`Macro View`)
1. **The Navigation Sidebar (Left Edge):**
    * HTML Content Visual (240x1080 at X: 0, Y: 0). Measure: `Sidebar Navigation HTML` (Ensure `VAR ActivePage = "Macro"`).
    * Overlay three transparent Blank Buttons mapped to navigate to your three respective pages.
2. **The Global Header (Top Right):**
    * HTML Content Visual (1680x90 at X: 240, Y: 0). Measure: `Header - Macro View HTML`.
3. **The Slicer Strip:**
    * Below the header, add native Power BI slicers for `CEO Era` (Dropdown) and `Date` (Between/Timeline Slider). Format them to blend into the dark background.
4. **The KPI Strip:**
    * Add four HTML Content visuals side-by-side (400x120 at Y: 160).
    * Map them to: `KPI - Latest Price`, `KPI - CAGR`, `KPI - Sharpe Ratio`, and `KPI - Max Drawdown`.
5. **The Price Action Chart (Center-Left):**
    * Native Line Chart (1000x740 at 240, 300).
    * X-Axis: `Date`. Y-Axis: `Latest Price`. Legend: `CEO Era`.
    * **Action:** Turn ON Logarithmic Scale for the Y-Axis.
6. **The Decade Summary Matrix (Center-Right):**
    * Native Matrix (640x740 at 1260, 300).
    * Rows: `Decade`. 
    * Values: `CAGR`, `SVG Sparkline - Price Trend`, `Annualized Volatility`, `SVG Boxplot - Daily Returns`.
    * **Action:** Go to Format > Image Size and set it to Height 45, Width 160. Increase row padding to 15px.

### Act III: Technical Deep Dive (`Technical View`)
1. **Sidebar & Header:**
    * Copy the Sidebar from Page 1 (Update measure to `ActivePage = "Technical"`).
    * HTML Content Visual (1680x90 at 240, 0). Measure: `Header - Technical View HTML`.
2. **The Slicer & Context Badge:**
    * Add a Native **Relative Date Slicer**. Set the default to "Last 1 Year".
    * Add a Native Power BI **Pill Button** above your charts. Use Conditional Formatting (`fx`) to map the button text to `Button Text - Active Dates` (the SavoryData measure). Configure hover states for tactical UI feedback.
3. **The KPI Strip:**
    * Three HTML visuals side-by-side (540x120 at Y: 160). Map to: `KPI - Volatility`, `KPI - RSI`, and `KPI - Trend State`.
4. **The Technical Stack (Center Stage vertically stacked):**
    * **Price:** Line chart (1640x350). Y-Axis: `Latest Price`, `50-Day SMA`, `200-Day SMA`. Turn off X-Axis labels.
    * **Volume:** Stacked Column Chart (1640x150). Y-Axis: `Volume`. Apply `Is Volume Surge` conditional formatting. Turn off X-Axis labels.
    * **Oscillator:** Line Chart (1640x150). Y-Axis: `RSI (14-Day)`. Add Y-Axis constant reference lines at 30 and 70. Keep X-Axis labels ON to anchor the timeline for the stack above it.
5. **The Advisory Engine (Footer):**
    * HTML Content Visual (1640x100 at the bottom). Map to `Dynamic Business Recommendation`.

## Phase 4: The Hidden Context Layers (Tooltips)

These hidden pages replace native black-box tooltips with custom SVG visual reporting.

1. **Build `Tooltip_Macro`:**
    * Create a hidden page, set Canvas Type to "Tooltip" (320x240), Background `#1d1d1f` (0% transparency).
    * Add a Matrix visual containing `[SVG Tooltip - Drawdown Recovery]`.
    * Go to Page 1, select the Price Action Line Chart, and map its Tooltip to `Tooltip_Macro`.
2. **Build `Tooltip_Tech`:**
    * Create a hidden page, set Canvas Type to "Tooltip", Background `#1d1d1f`.
    * Add a Matrix containing `[SVG Tooltip - RSI Capsule]` and `[SVG Tooltip - Volatility Donut]`.
    * Go to Page 2 and map this tooltip to your Decade Matrix or Technical charts.

## Appendix: Custom HTML DAX Measures

### Landing Page HTML DAX Measure:
```dax
Landing Page HTML = 
// 1. Fetch Dynamic Data from the Semantic Model
VAR LastDataUpdate = FORMAT(MAX('Calendar'[Date]), "MMMM dd, yyyy")

// 2. Define the HTML and Advanced CSS
VAR HtmlContent = 
"
<div style='
    font-family: -apple-system, BlinkMacSystemFont, ""Segoe UI"", Roboto, Helvetica, Arial, sans-serif;
    background-color: #000000;
    color: #f5f5f7;
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    padding: 2rem;
    overflow: hidden;
    text-align: center;
'>

    <svg viewBox='0 0 384 512' style='width: 50px; height: 50px; fill: #f5f5f7; margin-bottom: 20px;'>
        <path d='M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z'></path>
    </svg>

    <h1 style='
        font-size: 3.5vw;
        font-weight: 700;
        letter-spacing: -0.05em;
        margin: 0 0 10px 0;
        background: linear-gradient(90deg, #ffffff, #86868b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    '>
        Apple Stock Market Analysis
    </h1>
    <p style='color: #86868b; font-size: 1.2vw; font-weight: 400; margin: 0 0 40px 0; letter-spacing: 0.02em;'>
        1980 &mdash; 2025 Historical Data & Advanced Portfolio Analytics
    </p>

    <div style='display: flex; gap: 15px; margin-bottom: 40px; justify-content: center; flex-wrap: wrap;'>
        <div style='background: #1d1d1f; border: 1px solid #424245; border-radius: 12px; padding: 10px 20px; font-size: 0.9vw; display: flex; align-items: center; gap: 8px;'>
            <span style='color: #86868b;'>Dataset:</span> 11,000+ Trading Days
        </div>
        <div style='background: #1d1d1f; border: 1px solid #424245; border-radius: 12px; padding: 10px 20px; font-size: 0.9vw; display: flex; align-items: center; gap: 8px;'>
            <span style='color: #86868b;'>Sources:</span> Yahoo Finance & Stooq
        </div>
        <div style='background: #1d1d1f; border: 1px solid #424245; border-radius: 12px; padding: 10px 20px; font-size: 0.9vw; display: flex; align-items: center; gap: 8px;'>
            <span style='color: #86868b;'>Last Price Action:</span> \" & LastDataUpdate & \"
        </div>
    </div>

    <div style='display: flex; gap: 30px; margin-bottom: 50px;'>
        <a href='https://github.com/Sohila-Khaled-Abbas/apple-stock-market-analysis' target='_blank' style='color: #2997ff; text-decoration: none; font-size: 1vw; display: flex; align-items: center; gap: 8px; font-weight: 500;'>
            <svg viewBox='0 0 24 24' style='width: 18px; height: 18px; fill: currentColor;'><path d='M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z'/></svg>
            GitHub Repository
        </a>
        <a href='https://docs.google.com/presentation/d/1v5ssMhSDsMxkJXG-Xy1a-X05HoXnfY5Ce7pQUGvhGaE/edit?usp=sharing' target='_blank' style='color: #2997ff; text-decoration: none; font-size: 1vw; display: flex; align-items: center; gap: 8px; font-weight: 500;'>
            <svg viewBox='0 0 24 24' style='width: 18px; height: 18px; fill: currentColor;'><path d='M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-9 14l-5-3 5-3v6zm7-4h-5v-2h5v2zm0-4h-5V7h5v2z'/></svg>
            Project Presentation
        </a>
    </div>

    <div style='
        background-color: #f5f5f7;
        color: #000000;
        padding: 1.2vw 3vw;
        border-radius: 40px;
        font-size: 1.2vw;
        font-weight: 600;
        cursor: pointer;
        display: inline-block;
        margin-bottom: 40px;
        box-shadow: 0 4px 14px 0 rgba(255,255,255,0.1);
    '>
        Enter Analytics Dashboard
    </div>

    <div style='margin-top: auto; font-size: 0.9vw; color: #86868b; display: flex; align-items: center; justify-content: center; gap: 10px;'>
        Developed by <span style='color: #f5f5f7; font-weight: 600;'>Sohila Khaled</span> | Certified Data Analyst
        <a href='https://www.linkedin.com/in/sohilakabbas/' target='_blank' style='color: #86868b; display: flex; align-items: center; transition: 0.3s;'>
            <svg viewBox='0 0 24 24' style='width: 20px; height: 20px; fill: currentColor; margin-left: 5px;'><path d='M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z'/></svg>
        </a>
    </div>

</div>
"
RETURN HtmlContent
```

*Note: Overlay a blank Power BI button set to Page Navigation over the "Enter Analytics Dashboard" rectangle to create the interactive click.*
