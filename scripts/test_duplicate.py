import yfinance as yf
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

DB_USER = 'root'
DB_PASSWORD = 'EqV2P9j$0!MduLH' 
DB_HOST = 'localhost'
DB_NAME = 'apple_stock_db'
TABLE_NAME = 'aapl_daily'

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
try:
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT MAX(Trade_Date) FROM {TABLE_NAME}")).fetchone()
        last_db_date = result[0]
        print("Last DB Date:", last_db_date)
except Exception as e:
    print("DB connection failed:", e)

# test yfinance
df = yf.download("AAPL", start="2026-03-26", end="2026-03-29", auto_adjust=False)
print(df.index)
print("Duplicate index elements?", df.index.duplicated().any())
