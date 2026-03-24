# Power BI Dashboard Design & Storytelling

A financial dashboard must go beyond being a mere "database GUI"; it must present a visual argument. To effectively visualize the Apple (AAPL) dataset (1980–2025) and avoid the "Data Dump Fallacy," our reporting approach separates macro-economic trends from micro-trading technicals through an architected two-page storytelling layout.

## Page 1: The Executive Macro View

**Objective:** Answer the strategic questions: *How has AAPL performed across different CEO eras? How does it compare to the S&P 500? What is the baseline risk?*

### Phase 1: Global Formatting & The "Scale" Fallacy
When visualizing multi-decade compounding assets, a standard linear Y-axis creates an illusion of complete flatness until recent years.
- **Logarithmic Scaling:** The main Price Line Charts use a Logarithmic Y-axis to ensure percentage gains are visually proportionate across different eras and valuations.

### Phase 2: Page 1 Layout Elements
1. **The "Z-Pattern" Header:** High-density aggregate metrics across the top.
   - **Cards:** `Latest Price`, `CAGR` (vs S&P 500), `Sharpe Ratio` (conditionally formatted green > 1.0, red < 1.0), and `Max Drawdown`.
2. **The Primary Anchor Visual:**
   - **Line Chart:** `Calendar[Date]` (Year -> Quarter) vs `Total Return %` and `SP500 Daily Return %`. Includes Error Bars to highlight the Jobs Era (1997) vs Cook Era (2011).
3. **The Risk/Reward Matrix:**
   - **Scatter Chart:** `Annualized Volatility` (X) vs `CAGR` (Y) grouped by `Decade`, visually demonstrating which decade offered the best risk-adjusted returns.
4. **Slicer Pane:**
   - Dropdown for `CEO Era` and timeline slider for `Date`.

---

## Page 2: The Technical Deep Dive

**Objective:** Answer tactical trading questions: *Is the stock currently overbought? Where are the momentum shifts? When did institutional volume spike?*

### Phase 3: Page 2 Layout Elements
1. **The Price Action Engine (Top Half):**
   - **Line Chart:** Stacked and synchronized rather than spaghetti-layered.
   - **Values:** `Latest Price` (Black), `50-Day SMA` (Light Blue), and `200-Day SMA` (Dark Blue).
2. **The Momentum & Volume Oscillators (Bottom Half):**
   - **Volume Surge (Bottom Left):** Stacked Column Chart for `Volume`. Colored Bright Orange for surge/capitulation days, Light Grey otherwise.
   - **RSI (Bottom Right):** Line Chart with static reference lines at **70** (Overbought) and **30** (Oversold).

---

## Phase 4: Advanced Storytelling Techniques & Polish

- **Report Page Tooltips:** Hovering over a massive drop reveals a hidden context page with `Days Since ATH` and a gauge for `Daily Drawdown %`.
- **Dynamic Titles:** Measures dynamically update titles based on interactions. Example: `Apple Risk & Return Profile: Jobs Era`.
- **Bookmark Toggles:** An overlay Area Chart plotting `Daily Drawdown %` on top of the Price Line. Two bookmarks ("Show Price Trend", "Show Drawdown Risk") allow analysts to toggle views contextually.

### HTML Content Visual & "Enter Dashboard" Button
To bypass native visual limitations and introduce an Apple-like SaaS experience, a custom HTML/CSS measure renders an application-like entry page. This uses the **HTML Content** visual (by Daniel Marsh-Patrick) combined with an invisible native Power BI navigation button.

**Landing Page HTML DAX Measure:**
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
\"
RETURN HtmlContent
```

*Note: Overlay a blank Power BI button set to Page Navigation over the "Enter Analytics Dashboard" rectangle to create the interactive click.*
