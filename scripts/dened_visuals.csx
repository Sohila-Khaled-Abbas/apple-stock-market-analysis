// ═══════════════════════════════════════════════════════════════════
// AAPL Technical View — Deneb Vega-Lite Specs
// Run in Tabular Editor 2 or 3 C# Script window
// ═══════════════════════════════════════════════════════════════════

var tbl = Model.Tables["_Measures"];
string folder = "🔬 Deneb Specs";

// Helper: converts a raw JSON string to a valid DAX string literal
// by doubling internal double-quotes and wrapping in outer quotes.
string ToDax(string json) {
    return "\"" + json.Replace("\"", "\"\"") + "\"";
}

// ─── SPEC 1: Candlestick OHLC ───────────────────────────────────
string spec1 = @"{
  ""$schema"": ""https://vega.github.io/schema/vega-lite/v5.json"",
  ""data"": { ""name"": ""dataset"" },
  ""background"": ""transparent"",
  ""padding"": { ""top"": 12, ""right"": 16, ""bottom"": 8, ""left"": 8 },
  ""config"": {
    ""view"": { ""stroke"": ""transparent"" },
    ""axis"": {
      ""domainColor"": ""#424245"",
      ""gridColor"": ""#2a2a2d"",
      ""gridDash"": [2, 4],
      ""tickColor"": ""#424245"",
      ""tickSize"": 4,
      ""labelColor"": ""#86868b"",
      ""labelFont"": ""system-ui, -apple-system, sans-serif"",
      ""labelFontSize"": 11
    }
  },
  ""encoding"": {
    ""x"": {
      ""field"": ""Trade_Date"",
      ""type"": ""temporal"",
      ""axis"": { ""title"": null, ""format"": ""%b '%y"", ""labelAngle"": -30, ""gridColor"": ""transparent"" }
    }
  },
  ""layer"": [
    {
      ""mark"": { ""type"": ""rule"", ""strokeWidth"": 1 },
      ""encoding"": {
        ""y"": {
          ""field"": ""Low_Price"", ""type"": ""quantitative"",
          ""scale"": { ""zero"": false, ""nice"": false },
          ""axis"": { ""title"": null, ""format"": ""$,.0f"", ""tickCount"": 6, ""domainColor"": ""transparent"" }
        },
        ""y2"": { ""field"": ""High_Price"" },
        ""color"": {
          ""condition"": [
            { ""test"": ""datum['Candlestick_Direction'] === 'Bullish'"", ""value"": ""#30d158"" },
            { ""test"": ""datum['Candlestick_Direction'] === 'Doji (Flat)'"", ""value"": ""#86868b"" }
          ],
          ""value"": ""#ff453a""
        },
        ""tooltip"": [
          { ""field"": ""Trade_Date"", ""type"": ""temporal"", ""title"": ""Date"", ""format"": ""%B %d, %Y"" },
          { ""field"": ""Open_Price"", ""type"": ""quantitative"", ""title"": ""Open"", ""format"": ""$,.2f"" },
          { ""field"": ""High_Price"", ""type"": ""quantitative"", ""title"": ""High"", ""format"": ""$,.2f"" },
          { ""field"": ""Low_Price"", ""type"": ""quantitative"", ""title"": ""Low"", ""format"": ""$,.2f"" },
          { ""field"": ""Close_Price"", ""type"": ""quantitative"", ""title"": ""Close"", ""format"": ""$,.2f"" },
          { ""field"": ""Volume"", ""type"": ""quantitative"", ""title"": ""Volume"", ""format"": "","" },
          { ""field"": ""Candlestick_Direction"", ""title"": ""Signal"" }
        ]
      }
    },
    {
      ""mark"": { ""type"": ""bar"", ""size"": 5, ""clip"": true },
      ""encoding"": {
        ""y"": { ""field"": ""Open_Price"", ""type"": ""quantitative"" },
        ""y2"": { ""field"": ""Close_Price"" },
        ""color"": {
          ""condition"": [
            { ""test"": ""datum['Candlestick_Direction'] === 'Bullish'"", ""value"": ""#30d158"" },
            { ""test"": ""datum['Candlestick_Direction'] === 'Doji (Flat)'"", ""value"": ""#86868b"" }
          ],
          ""value"": ""#ff453a""
        },
        ""opacity"": { ""value"": 0.85 }
      }
    }
  ]
}";

var m1 = tbl.AddMeasure("Deneb - Candlestick OHLC", ToDax(spec1));
m1.DisplayFolder  = folder;
m1.Description    = "Vega-Lite 2-layer candlestick. Rule=wick, Bar=body. Bullish=#30d158, Doji=#86868b, Bearish=#ff453a. Bind: Trade_Date, Open_Price, High_Price, Low_Price, Close_Price, Candlestick_Direction, Volume.";

// ─── SPEC 2: Price Action & SMA Lines ───────────────────────────
string spec2 = @"{
  ""$schema"": ""https://vega.github.io/schema/vega-lite/v5.json"",
  ""data"": { ""name"": ""dataset"" },
  ""background"": ""transparent"",
  ""padding"": { ""top"": 12, ""right"": 16, ""bottom"": 8, ""left"": 8 },
  ""config"": {
    ""view"": { ""stroke"": ""transparent"" },
    ""axis"": {
      ""domainColor"": ""#424245"", ""gridColor"": ""#2a2a2d"", ""gridDash"": [2, 4],
      ""tickColor"": ""#424245"", ""tickSize"": 4, ""labelColor"": ""#86868b"",
      ""labelFont"": ""system-ui, -apple-system, sans-serif"", ""labelFontSize"": 11
    },
    ""legend"": {
      ""labelColor"": ""#f5f5f7"", ""labelFont"": ""system-ui, -apple-system, sans-serif"",
      ""labelFontSize"": 11, ""titleColor"": ""#86868b"",
      ""fillColor"": ""#1d1d1f"", ""strokeColor"": ""#424245"",
      ""padding"": 10, ""cornerRadius"": 8
    }
  },
  ""layer"": [
    {
      ""mark"": { ""type"": ""area"", ""opacity"": 0.04, ""clip"": true },
      ""encoding"": {
        ""x"": { ""field"": ""Trade_Date"", ""type"": ""temporal"" },
        ""y"": { ""field"": ""Adj_Close"", ""type"": ""quantitative"", ""scale"": { ""zero"": false, ""nice"": false } },
        ""color"": {
          ""condition"": { ""test"": ""datum['50-Day SMA'] >= datum['200-Day SMA']"", ""value"": ""#30d158"" },
          ""value"": ""#ff453a""
        }
      }
    },
    {
      ""transform"": [
        { ""fold"": [""Adj_Close"", ""50-Day SMA"", ""200-Day SMA""], ""as"": [""Series"", ""Price""] },
        { ""filter"": ""isValid(datum.Price)"" }
      ],
      ""mark"": { ""type"": ""line"", ""interpolate"": ""monotone"", ""clip"": true },
      ""encoding"": {
        ""x"": {
          ""field"": ""Trade_Date"", ""type"": ""temporal"",
          ""axis"": { ""title"": null, ""format"": ""%b '%y"", ""labelAngle"": -30, ""gridColor"": ""transparent"" }
        },
        ""y"": {
          ""field"": ""Price"", ""type"": ""quantitative"",
          ""scale"": { ""zero"": false, ""nice"": false },
          ""axis"": { ""title"": null, ""format"": ""$,.0f"", ""tickCount"": 6, ""domainColor"": ""transparent"" }
        },
        ""color"": {
          ""field"": ""Series"", ""type"": ""nominal"",
          ""scale"": {
            ""domain"": [""Adj_Close"", ""50-Day SMA"", ""200-Day SMA""],
            ""range"": [""#f5f5f7"", ""#ff9f0a"", ""#bf5af2""]
          },
          ""legend"": {
            ""title"": null, ""orient"": ""top-left"",
            ""labelExpr"": ""datum.label === 'Adj_Close' ? 'AAPL Price' : datum.label""
          }
        },
        ""strokeWidth"": {
          ""condition"": { ""test"": ""datum.Series === 'Adj_Close'"", ""value"": 2 },
          ""value"": 1.5
        },
        ""opacity"": {
          ""condition"": { ""test"": ""datum.Series === 'Adj_Close'"", ""value"": 0.95 },
          ""value"": 0.8
        },
        ""tooltip"": [
          { ""field"": ""Trade_Date"", ""type"": ""temporal"", ""title"": ""Date"", ""format"": ""%B %d, %Y"" },
          { ""field"": ""Price"", ""type"": ""quantitative"", ""title"": ""Price"", ""format"": ""$,.2f"" },
          { ""field"": ""Series"", ""title"": ""Series"" }
        ]
      }
    }
  ]
}";

var m2 = tbl.AddMeasure("Deneb - Price & SMA Lines", ToDax(spec2));
m2.DisplayFolder  = folder;
m2.Description    = "Vega-Lite multi-line with fold transform. Golden/Death Cross background shading. Bind: Trade_Date, Adj_Close, [50-Day SMA], [200-Day SMA].";

// ─── SPEC 3: RSI Oscillator ─────────────────────────────────────
string spec3 = @"{
  ""$schema"": ""https://vega.github.io/schema/vega-lite/v5.json"",
  ""data"": { ""name"": ""dataset"" },
  ""background"": ""transparent"",
  ""padding"": { ""top"": 12, ""right"": 16, ""bottom"": 8, ""left"": 8 },
  ""config"": {
    ""view"": { ""stroke"": ""transparent"" },
    ""axis"": {
      ""domainColor"": ""transparent"", ""gridColor"": ""#2a2a2d"", ""gridDash"": [2, 4],
      ""tickColor"": ""transparent"", ""labelColor"": ""#86868b"",
      ""labelFont"": ""system-ui, -apple-system, sans-serif"", ""labelFontSize"": 11
    }
  },
  ""layer"": [
    { ""mark"": { ""type"": ""rect"", ""opacity"": 0.06 }, ""encoding"": { ""y"": { ""datum"": 70, ""type"": ""quantitative"" }, ""y2"": { ""datum"": 100 }, ""color"": { ""value"": ""#ff453a"" } } },
    { ""mark"": { ""type"": ""rect"", ""opacity"": 0.06 }, ""encoding"": { ""y"": { ""datum"": 0, ""type"": ""quantitative"" }, ""y2"": { ""datum"": 30 }, ""color"": { ""value"": ""#30d158"" } } },
    { ""mark"": { ""type"": ""rule"", ""strokeDash"": [4, 4], ""strokeWidth"": 1, ""opacity"": 0.6 }, ""encoding"": { ""y"": { ""datum"": 70, ""type"": ""quantitative"" }, ""color"": { ""value"": ""#ff453a"" } } },
    { ""mark"": { ""type"": ""rule"", ""strokeDash"": [4, 4], ""strokeWidth"": 1, ""opacity"": 0.6 }, ""encoding"": { ""y"": { ""datum"": 30, ""type"": ""quantitative"" }, ""color"": { ""value"": ""#30d158"" } } },
    { ""mark"": { ""type"": ""rule"", ""strokeDash"": [2, 6], ""strokeWidth"": 1, ""opacity"": 0.25 }, ""encoding"": { ""y"": { ""datum"": 50, ""type"": ""quantitative"" }, ""color"": { ""value"": ""#86868b"" } } },
    {
      ""mark"": { ""type"": ""line"", ""interpolate"": ""monotone"", ""strokeWidth"": 2, ""clip"": true },
      ""encoding"": {
        ""x"": {
          ""field"": ""Trade_Date"", ""type"": ""temporal"",
          ""axis"": { ""title"": null, ""format"": ""%b '%y"", ""labelAngle"": -30, ""gridColor"": ""transparent"" }
        },
        ""y"": {
          ""field"": ""RSI (14-Day)"", ""type"": ""quantitative"",
          ""scale"": { ""domain"": [0, 100] },
          ""axis"": { ""title"": null, ""values"": [0, 30, 50, 70, 100], ""tickCount"": 5 }
        },
        ""color"": {
          ""field"": ""RSI (14-Day)"", ""type"": ""quantitative"",
          ""scale"": { ""type"": ""threshold"", ""domain"": [30, 70], ""range"": [""#30d158"", ""#64d2ff"", ""#ff453a""] },
          ""legend"": null
        },
        ""tooltip"": [
          { ""field"": ""Trade_Date"", ""type"": ""temporal"", ""title"": ""Date"", ""format"": ""%B %d, %Y"" },
          { ""field"": ""RSI (14-Day)"", ""type"": ""quantitative"", ""title"": ""RSI"", ""format"": "".1f"" }
        ]
      }
    }
  ]
}";

var m3 = tbl.AddMeasure("Deneb - RSI Oscillator", ToDax(spec3));
m3.DisplayFolder  = folder;
m3.Description    = "Vega-Lite 6-layer RSI oscillator. Threshold color scale: green<30, blue 30-70, red>70. Shaded zones + dashed threshold lines. Bind: Trade_Date, [RSI (14-Day)].";

// ─── SPEC 4: Volume & Surge ──────────────────────────────────────
string spec4 = @"{
  ""$schema"": ""https://vega.github.io/schema/vega-lite/v5.json"",
  ""data"": { ""name"": ""dataset"" },
  ""background"": ""transparent"",
  ""padding"": { ""top"": 12, ""right"": 16, ""bottom"": 8, ""left"": 8 },
  ""config"": {
    ""view"": { ""stroke"": ""transparent"" },
    ""axis"": {
      ""domainColor"": ""transparent"", ""gridColor"": ""#2a2a2d"", ""gridDash"": [2, 4],
      ""tickColor"": ""transparent"", ""labelColor"": ""#86868b"",
      ""labelFont"": ""system-ui, -apple-system, sans-serif"", ""labelFontSize"": 11
    }
  },
  ""layer"": [
    {
      ""mark"": { ""type"": ""bar"", ""cornerRadiusTopLeft"": 2, ""cornerRadiusTopRight"": 2, ""clip"": true },
      ""encoding"": {
        ""x"": {
          ""field"": ""Trade_Date"", ""type"": ""temporal"",
          ""axis"": { ""title"": null, ""format"": ""%b '%y"", ""labelAngle"": -30, ""gridColor"": ""transparent"" }
        },
        ""y"": { ""field"": ""Volume"", ""type"": ""quantitative"", ""axis"": { ""title"": null, ""format"": ""~s"", ""tickCount"": 4 } },
        ""color"": {
          ""condition"": { ""test"": ""datum['Is Volume Surge'] == 1"", ""value"": ""#ff9f0a"" },
          ""value"": ""#2997ff""
        },
        ""opacity"": {
          ""condition"": { ""test"": ""datum['Is Volume Surge'] == 1"", ""value"": 1 },
          ""value"": 0.45
        },
        ""tooltip"": [
          { ""field"": ""Trade_Date"", ""type"": ""temporal"", ""title"": ""Date"", ""format"": ""%B %d, %Y"" },
          { ""field"": ""Volume"", ""type"": ""quantitative"", ""title"": ""Volume"", ""format"": "","" },
          { ""field"": ""Is Volume Surge"", ""title"": ""Surge? (1=Yes)"" }
        ]
      }
    },
    {
      ""transform"": [
        { ""window"": [{ ""op"": ""mean"", ""field"": ""Volume"", ""as"": ""Avg30Volume"" }], ""frame"": [-29, 0] }
      ],
      ""mark"": { ""type"": ""line"", ""color"": ""#ff9f0a"", ""strokeDash"": [4, 3], ""strokeWidth"": 1.5, ""opacity"": 0.6, ""interpolate"": ""monotone"", ""clip"": true },
      ""encoding"": {
        ""x"": { ""field"": ""Trade_Date"", ""type"": ""temporal"" },
        ""y"": { ""field"": ""Avg30Volume"", ""type"": ""quantitative"" },
        ""tooltip"": [
          { ""field"": ""Trade_Date"", ""type"": ""temporal"", ""title"": ""Date"", ""format"": ""%B %d, %Y"" },
          { ""field"": ""Avg30Volume"", ""type"": ""quantitative"", ""title"": ""30D Avg"", ""format"": "","" }
        ]
      }
    },
    {
      ""transform"": [{ ""filter"": ""datum['Is Volume Surge'] == 1"" }],
      ""mark"": { ""type"": ""text"", ""dy"": -8, ""fontSize"": 9, ""fontWeight"": ""bold"", ""color"": ""#ff9f0a"", ""text"": ""▲"", ""clip"": true },
      ""encoding"": {
        ""x"": { ""field"": ""Trade_Date"", ""type"": ""temporal"" },
        ""y"": { ""field"": ""Volume"", ""type"": ""quantitative"" }
      }
    }
  ]
}";

var m4 = tbl.AddMeasure("Deneb - Volume & Surge", ToDax(spec4));
m4.DisplayFolder  = folder;
m4.Description    = "Vega-Lite 3-layer volume chart. Surge bars orange/full opacity, normal blue/45%. 30D rolling avg line (Vega window transform). Surge event markers. Bind: Trade_Date, Volume, [Is Volume Surge].";

Info("✅ Created 4 Deneb measures in _Measures[🔬 Deneb Specs]");