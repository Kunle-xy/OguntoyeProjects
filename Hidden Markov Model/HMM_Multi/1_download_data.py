import yfinance as yf
import pandas as pd
import os
from config import (
    TICKER,
    DATA_START_DATE,
    DATA_END_DATE,
    DATA_DIR,
    DATA_FILE
)

def download_spy_data():
    ticker_symbol = TICKER
    start_date = DATA_START_DATE
    end_date = DATA_END_DATE
    output_folder = DATA_DIR
    output_file = f"{TICKER}.csv"
    output_path = DATA_FILE

    print(f"--- Starting Download for {ticker_symbol} ---")
    print(f"Period: {start_date} to {end_date}")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    df = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=False)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index.name = "Date"
    df['return'] = df['Adj Close'].pct_change()

    if df.empty:
        print("Error: No data downloaded.")
        return

    df.to_csv(output_path)
    
    print(f"\nSuccess! Data saved to: {output_path}")
    print(f"Rows downloaded: {len(df)}")
    print(df.head())

if __name__ == "__main__":
    download_spy_data()
