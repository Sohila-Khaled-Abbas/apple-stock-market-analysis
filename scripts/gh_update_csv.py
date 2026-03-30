"""
Serverless Data Loading Script for GitHub Actions.
This script fetches new records from yfinance and appends 
them directly to the existing CSV file without requiring a MySQL connection.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

# Define relative path to the CSV from this script's location
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'processed', 'aapl_daily.csv')

def run_csv_update():
    print(f"Loading existing data from {CSV_PATH}...")
    
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CRITICAL ERROR: Cannot find historical CSV at {CSV_PATH}")

    # Load existing CSV
    # Parse dates immediately so we can find the max date
    df_existing = pd.read_csv(CSV_PATH, parse_dates=['Trade_Date'])
    
    if df_existing.empty:
        print("WARNING: CSV is empty. Falling back to initial 1980 load...")
        start_date = "1980-12-12"
        last_csv_date = None
    else:
        last_csv_date = df_existing['Trade_Date'].max()
        # Start fetching from the day AFTER the last record
        start_date = (last_csv_date + timedelta(days=1)).strftime('%Y-%m-%d')

    today = datetime.now().strftime('%Y-%m-%d')

    if start_date >= today:
        print(f"TERMINATING: CSV is already up to date as of {last_csv_date.strftime('%Y-%m-%d')}. No new data to fetch.")
        return

    print(f"FETCHING: Pulling data from {start_date} to {today}...")

    # Fetch data (auto_adjust=False is MANDATORY for 'Adj Close')
    df_new = yf.download("AAPL", start=start_date, end=today, auto_adjust=False)

    if df_new.empty:
        print("TERMINATING: API returned no data for the requested date range.")
        return

    # Flatten MultiIndex (yfinance >= 0.2.40 returns MultiIndex by default)
    if isinstance(df_new.columns, pd.MultiIndex):
        df_new.columns = [col[0] for col in df_new.columns]
    
    # Move Date from the Index into a standard column
    df_new.reset_index(inplace=True)

    # Rename columns to match existing structure
    rename_map = {
        'Date': 'Trade_Date',
        'Adj Close': 'Adj_Close',
        'Close': 'Close_Price',
        'High': 'High_Price',
        'Low': 'Low_Price',
        'Open': 'Open_Price',
        'Volume': 'Volume'
    }
    df_new.rename(columns=rename_map, inplace=True)

    # Enforce exact column order
    expected_cols = ['Trade_Date', 'Adj_Close', 'Close_Price', 'High_Price', 'Low_Price', 'Open_Price', 'Volume']
    missing_cols = [col for col in expected_cols if col not in df_new.columns]
    if missing_cols:
        raise ValueError(f"CRITICAL ERROR: yfinance failed to return required columns: {missing_cols}")
        
    df_new = df_new[expected_cols]

    # Drop rows where market was closed (yielding NaN prices)
    df_new.dropna(subset=['Adj_Close'], inplace=True)

    # Remove duplicate dates
    df_new.drop_duplicates(subset=['Trade_Date'], inplace=True)
    
    # Ensure we only keep dates strictly after the last recorded date in CSV
    if last_csv_date is not None:
        df_new = df_new[df_new['Trade_Date'] > last_csv_date]

    if df_new.empty:
        print("TERMINATING: No new valid records to append after filtering existing dates.")
        return

    # Concatenate new data with existing data
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    
    # Sort by date strictly
    df_final.sort_values(by='Trade_Date', inplace=True)
    
    # Export back to CSV
    print(f"EXPORTING: Saving {len(df_new)} new records to {CSV_PATH}...")
    
    # Date formatting before save to ensure consistent output string format in the CSV
    df_final['Trade_Date'] = pd.to_datetime(df_final['Trade_Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    df_final.to_csv(CSV_PATH, index=False)
    print("SUCCESS: Automated CSV enrichment complete.")

if __name__ == "__main__":
    run_csv_update()
