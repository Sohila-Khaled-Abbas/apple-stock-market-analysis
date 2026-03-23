"""
Incremental Data Loading Script for Apple Stock Market Analysis.
This script automatically fetches new records from yfinance and appends 
them to the MySQL database without duplicating existing historical data.
"""

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, text, types
from datetime import datetime, timedelta

# 1. Database Configuration
DB_USER = 'root'
DB_PASSWORD = 'EqV2P9j$0!MduLH' # Change to your actual MySQL password
DB_HOST = 'localhost'
DB_NAME = 'apple_stock_db'
TABLE_NAME = 'aapl_daily'

# Create the SQLAlchemy engine for connecting to MySQL
# Note: ensure pymysql is installed via pip (`pip install pymysql`)
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

def ensure_table_exists():
    """Forces MySQL to use DOUBLE to prevent the 1265 Truncation Error."""
    sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        Trade_Date DATETIME PRIMARY KEY,
        Adj_Close DOUBLE,
        Close_Price DOUBLE,
        High_Price DOUBLE,
        Low_Price DOUBLE,
        Open_Price DOUBLE,
        Volume BIGINT
    );
    """
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

def run_update():
    ensure_table_exists()

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT MAX(Trade_Date) FROM {TABLE_NAME}")).fetchone()
        last_db_date = result[0]

    if last_db_date is None:
        print("WARNING: Table is empty. Falling back to initial 1980 load...")
        start_date = "1980-12-12"
    else:
        # Start fetching from the day AFTER the last record in MySQL
        start_date = (last_db_date + timedelta(days=1)).strftime('%Y-%m-%d')

    today = datetime.now().strftime('%Y-%m-%d')

    if start_date >= today:
        print(f"TERMINATING: Database is already up to date as of {last_db_date}. No new data to fetch.")
    else:
        print(f"FETCHING: Pulling data from {start_date} to {today}...")

        # 4. FETCH AND CLEAN DATA (THE FIX)
        # auto_adjust=False is MANDATORY to guarantee 'Adj Close' is returned
        df = yf.download("AAPL", start=start_date, end=today, auto_adjust=False)

        if df.empty:
            print("TERMINATING: API returned no data for the requested date range.")
        else:
            # FIX: Flatten MultiIndex (yfinance >= 0.2.40 returns MultiIndex by default)
            if isinstance(df.columns, pd.MultiIndex):
                # Extract just the 'Price' string (Level 0), ignoring the 'Ticker' string (Level 1)
                df.columns = [col[0] for col in df.columns]
            
            # Move Date from the Index into a standard column
            df.reset_index(inplace=True)

            # Dictionary mapping prevents Length Mismatch errors. 
            # It only maps what exists and ignores positional order.
            rename_map = {
                'Date': 'Trade_Date',
                'Adj Close': 'Adj_Close',
                'Close': 'Close_Price',
                'High': 'High_Price',
                'Low': 'Low_Price',
                'Open': 'Open_Price',
                'Volume': 'Volume'
            }
            df.rename(columns=rename_map, inplace=True)

            # Enforce exact column order for MySQL insertion
            expected_cols = ['Trade_Date', 'Adj_Close', 'Close_Price', 'High_Price', 'Low_Price', 'Open_Price', 'Volume']
            
            # Identify missing columns (if any) to fail gracefully rather than crashing
            missing_cols = [col for col in expected_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"CRITICAL ERROR: yfinance failed to return required columns: {missing_cols}")
                
            df = df[expected_cols]

            # Drop rows where market was closed (holidays/weekends) yielding NaN prices
            df.dropna(subset=['Adj_Close'], inplace=True)

            # 5. INGESTION TO MYSQL
            # Explicit type mapping ensures Pandas doesn't send Floats that MySQL truncates
            sql_dtypes = {
                'Trade_Date': types.DateTime,
                'Adj_Close': types.Float(precision=53), 
                'Close_Price': types.Float(precision=53),
                'High_Price': types.Float(precision=53),
                'Low_Price': types.Float(precision=53),
                'Open_Price': types.Float(precision=53),
                'Volume': types.BigInteger
            }

            # Append data
            df.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False, dtype=sql_dtypes)
            print(f"SUCCESS: {len(df)} new records appended to MySQL database.")

if __name__ == "__main__":
    run_update()
