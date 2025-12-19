import yfinance as yf
import pandas as pd
import os

def download_spy_data():
    # --- CONFIGURATION ---
    ticker_symbol = "SPY"
    start_date = "2000-01-01"
    end_date = "2025-12-31"  # Downloads up to the end of 2025
    output_folder = "data"
    output_file = "SPY.csv"
    output_path = os.path.join(output_folder, output_file)

    print(f"--- Starting Download for {ticker_symbol} ---")
    print(f"Period: {start_date} to {end_date}")

    # 1. Create the 'data' folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    # 2. Download the data from Yahoo Finance
    # auto_adjust=False ensures we get 'Adj Close' and 'Close' as separate columns
    df = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=False)

    # 3. Fix Formatting Issues (Critical for your HMM script)
    # Yahoo sometimes returns a "MultiIndex" (e.g., Price -> SPY). We flatten this.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Ensure the Index is named "Date" so pandas reads it correctly later
    df.index.name = "Date"
    df['return'] = df['Adj Close'].pct_change()  # Calculate daily returns

    # Check if data was actually downloaded
    if df.empty:
        print("Error: No data downloaded. Check your internet connection or proxy settings.")
        return

    # 4. Save to CSV
    df.to_csv(output_path)
    
    print(f"\nSuccess! Data saved to: {output_path}")
    print(f"Rows downloaded: {len(df)}")
    print("\nFirst 5 rows of your new data:")
    print(df.head())

if __name__ == "__main__":
    download_spy_data()