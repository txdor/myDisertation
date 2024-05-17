import pandas as pd
import json
import os

# List of tickers
tickers = ['AAPL', 'MSFT', 'JNJ', 'BLK']  # Add more tickers as needed

# Directory containing JSON files
directory = 'data'

# Initialize a dictionary to hold DataFrames for each ticker
data_frames = {}

# Loop through each ticker and process their JSON files
for ticker in tickers:
    # Process Balance Sheet
    balance_file_path = os.path.join(directory, f'{ticker}_balanceSheet.json')
    if os.path.exists(balance_file_path):
        with open(balance_file_path, 'r') as file:
            nested_json_data = json.load(file)
        df_balance = pd.json_normalize(nested_json_data['report'], sep='_')
        data_frames[f'{ticker}_balanceSheet'] = df_balance
        # df_balance.to_csv(f'{ticker}_balanceSheet.csv', index=False)

    # Process Income Statement
    income_file_path = os.path.join(directory, f'{ticker}_incomeStatement.json')
    if os.path.exists(income_file_path):
        with open(income_file_path, 'r') as file:
            nested_json_data = json.load(file)
        df_income = pd.json_normalize(nested_json_data['report'], sep='_')
        data_frames[f'{ticker}_incomeStatement'] = df_income
        # df_income.to_csv(f'{ticker}_incomeStatement.csv', index=False)

    # Process Cashflow Statement
    cashflow_file_path = os.path.join(directory, f'{ticker}_cashflowStatement.json')
    if os.path.exists(cashflow_file_path):
        with open(cashflow_file_path, 'r') as file:
            nested_json_data = json.load(file)
        df_cashflow = pd.json_normalize(nested_json_data['report'], sep='_')
        data_frames[f'{ticker}_cashflowStatement'] = df_cashflow
        # df_cashflow.to_csv(f'{ticker}_cashflowStatement.csv', index=False)

# Merge all tickers' data into a single Excel file with each ticker on a different sheet
with pd.ExcelWriter('All_Tickers_Data.xlsx') as writer:
    for sheet_name, df in data_frames.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Data processing and merging complete. Check the 'All_Tickers_Data.xlsx' file.")
