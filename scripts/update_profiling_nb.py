import json

notebook_path = r"d:\courses\Data Science\Data Engineering\Projects\Apple Stock Market Analysis\notebooks\01_data_profiling.ipynb"

new_nb = {
 "cells": [
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "864893bb",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import necessary libraries\n",
    "import pandas as pd\n",
    "from sqlalchemy import create_engine\n",
    "\n",
    "# Connect to the MySQL database containing the updated, API-enriched dataset\n",
    "DB_USER = 'root'\n",
    "DB_PASSWORD = 'EqV2P9j$0!MduLH'\n",
    "DB_HOST = 'localhost'\n",
    "DB_NAME = 'apple_stock_db'\n",
    "TABLE_NAME = 'aapl_daily'\n",
    "\n",
    "engine = create_engine(f\"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}\")\n",
    "\n",
    "# Load data into a pandas DataFrame directly from the database\n",
    "df = pd.read_sql(f\"SELECT * FROM {TABLE_NAME}\", con=engine)\n",
    "print(f\"Loaded {len(df)} records.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "a4e7b64b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Quality Check: Understand the data distribution and identify any missing values\n",
    "\n",
    "# Generate descriptive statistics summarizing central tendency, dispersion, and shape of the dataset\n",
    "display(df.describe())\n",
    "\n",
    "# Check for missing values in each column and calculate the total count of nulls per column\n",
    "print(\"\\n--- Null Value Check ---\")\n",
    "print(df.isnull().sum())\n",
    "\n",
    "# Verify price logic: The 'High' price must always be greater than or equal to both 'Low' and 'Close' prices\n",
    "# Create a new DataFrame containing any rows where this logic is violated\n",
    "logic_errors = df[(df['High_Price'] < df['Low_Price']) | (df['High_Price'] < df['Close_Price'])]\n",
    "if not logic_errors.empty:\n",
    "    print(\"\\n--- Logic Errors Found ---\")\n",
    "    display(logic_errors)\n",
    "else:\n",
    "    print(\"\\nNo price logic errors found.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(new_nb, f, indent=1)
    f.write('\n')
