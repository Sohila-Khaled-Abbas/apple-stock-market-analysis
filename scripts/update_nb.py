import json
import os

notebook_path = r"d:\courses\Data Science\Data Engineering\Projects\Apple Stock Market Analysis\notebooks\03_data_validation.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_markdown_cell = {
 "cell_type": "markdown",
 "id": "api_cross_validation",
 "metadata": {},
 "source": [
  "## 8. External API Cross-Validation\n",
  "\n",
  "To ensure that our historical data in MySQL is accurate, we will take a random sample of dates from our database and fetch those exact dates from the `yfinance` API. We then compare the database values against the API values to assert factual accuracy."
 ]
}

new_code_cell = {
 "cell_type": "code",
 "execution_count": None,
 "id": "api_code",
 "metadata": {},
 "outputs": [],
 "source": [
  "import yfinance as yf\n",
  "import numpy as np\n",
  "\n",
  "# Sample 5 random dates from the database for validation\n",
  "sample_dates = df['Trade_Date'].sample(5, random_state=42).dt.strftime('%Y-%m-%d').tolist()\n",
  "print(f\"Validating dates: {sample_dates}\")\n",
  "\n",
  "validation_errors = 0\n",
  "\n",
  "for date in sample_dates:\n",
  "    # Fetch data for the specific date (+1 day for end date to get the single day)\n",
  "    next_day = (pd.to_datetime(date) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')\n",
  "    api_data = yf.download(\"AAPL\", start=date, end=next_day, auto_adjust=False, progress=False)\n",
  "    \n",
  "    if api_data.empty:\n",
  "        print(f\"⚠️ API Data missing for {date}\")\n",
  "        continue\n",
  "        \n",
  "    if isinstance(api_data.columns, pd.MultiIndex):\n",
  "        api_data.columns = [col[0] for col in api_data.columns]\n",
  "        \n",
  "    api_close = float(api_data['Close'].iloc[0])\n",
  "    db_close = float(df[df['Trade_Date'] == date]['Close_Price'].values[0])\n",
  "    api_volume = float(api_data['Volume'].iloc[0])\n",
  "    db_volume = float(df[df['Trade_Date'] == date]['Volume'].values[0])\n",
  "    \n",
  "    # Compare allowing a small floating point tolerance due to potential historical adjustments/splits\n",
  "    if not np.isclose(api_close, db_close, rtol=1e-2):\n",
  "        print(f\"❌ Mismatch on {date}: DB Close={db_close:.4f}, API Close={api_close:.4f}\")\n",
  "        validation_errors += 1\n",
  "    elif not np.isclose(api_volume, db_volume, rtol=1e-2) and db_volume != 0:\n",
  "        print(f\"⚠️ Volume Variance on {date}: DB Volume={db_volume}, API Volume={api_volume}\")\n",
  "        # Not counting volume as a rigid error because different API endpoints report slight variations in volume\n",
  "    else:\n",
  "        print(f\"✅ Match on {date}: Close Price = {db_close:.4f}\")\n",
  "\n",
  "if validation_errors == 0:\n",
  "    print(\"\\n🏆 API Cross-Validation Passed: Historical numbers match the external source.\")\n",
  "else:\n",
  "    print(f\"\\n⚠️ API Cross-Validation completed with {validation_errors} errors.\")"
 ]
}

nb['cells'].extend([new_markdown_cell, new_code_cell])

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
    f.write('\n')
