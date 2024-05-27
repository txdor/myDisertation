import pandas as pd
from sqlalchemy import create_engine
import os

# SQL Server connection details for Windows Authentication
server = 'DESKTOP-B8G31OU'  # Replace with your server name or IP
database = 'testDBscript'  # Replace with your database name
driver = 'ODBC Driver 17 for SQL Server'  # Ensure this driver is installed

# Create the connection string for Windows Authentication
connection_string = f'mssql+pyodbc://@{server}/{database}?driver={driver}&Trusted_Connection=yes'

# Create a SQLAlchemy engine
engine = create_engine(connection_string)

# Directory containing transformed CSV files
directory = 'transformed_data'

# List of tickers
tickers = ['AAPL', 'BLK', 'BMY', 'JNJ', 'MSFT', 'NKE', 'SBUX', 'TXN', 'V', 'VZ']  # Add more tickers as needed

# Loop through each ticker and load their CSV files into SQL Server
for ticker in tickers:
    # Load Balance Sheet
    balance_file_path = os.path.join(directory, f'{ticker}_balanceSheet.csv')
    if os.path.exists(balance_file_path):
        df_balance = pd.read_csv(balance_file_path)
        df_balance.to_sql(f'{ticker}_balanceSheet', engine, if_exists='replace', index=False)

    # Load Income Statement
    income_file_path = os.path.join(directory, f'{ticker}_incomeStatement.csv')
    if os.path.exists(income_file_path):
        df_income = pd.read_csv(income_file_path)
        df_income.to_sql(f'{ticker}_incomeStatement', engine, if_exists='replace', index=False)

    # Load Cashflow Statement
    cashflow_file_path = os.path.join(directory, f'{ticker}_cashflowStatement.csv')
    if os.path.exists(cashflow_file_path):
        df_cashflow = pd.read_csv(cashflow_file_path)
        df_cashflow.to_sql(f'{ticker}_cashflowStatement', engine, if_exists='replace', index=False)

    # Load Ratios data
    ratios_file_path = os.path.join(directory, f'{ticker}_ratios.csv')
    if os.path.exists(ratios_file_path):
        df_ratios = pd.read_csv(ratios_file_path)
        df_ratios.to_sql(f'{ticker}_ratios', engine, if_exists='replace', index=False)

    # Load Dividend data
    dividend_file_path = os.path.join(directory, f'{ticker}_dividendData.csv')
    if os.path.exists(dividend_file_path):
        df_dividend = pd.read_csv(dividend_file_path)
        df_dividend.to_sql(f'{ticker}_dividendData', engine, if_exists='replace', index=False)

print("Data loading into SQL Server complete.")
