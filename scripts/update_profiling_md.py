import json

notebook_path = r"d:\courses\Data Science\Data Engineering\Projects\Apple Stock Market Analysis\notebooks\01_data_profiling.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Extract existing code cells
code_cell_0 = nb['cells'][0]
code_cell_1 = nb['cells'][1]

# Create new markdown cells
md_title = {
 "cell_type": "markdown",
 "id": "title_md",
 "metadata": {},
 "source": [
  "# 📊 Initial Data Profiling\n",
  "\n",
  "This notebook establishes a direct connection to our `apple_stock_db` MySQL database to profile the continuously updated AAPL dataset. Here we perform initial exploratory data analysis (EDA) to summarize the dataset's central tendency, dispersion, and overall shape."
 ]
}

md_connect = {
 "cell_type": "markdown",
 "id": "connect_md",
 "metadata": {},
 "source": [
  "## 1. Database Connection & Data Extraction\n",
  "We utilize SQLAlchemy to connect to our MySQL instance and load the `aapl_daily` table into a Pandas DataFrame for profiling."
 ]
}

md_qa = {
 "cell_type": "markdown",
 "id": "qa_md",
 "metadata": {},
 "source": [
  "## 2. Quality Assurance Checks\n",
  "This section executes a high-level statistical overview (`describe`), checks for missing data points (`nulls`), and performs basic assertion checks on the logical structure of market prices (e.g., ensuring a trading day's High price is mathematically sound relative to its Low and Close prices)."
 ]
}

# Reassemble
nb['cells'] = [md_title, md_connect, code_cell_0, md_qa, code_cell_1]

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
    f.write('\n')
