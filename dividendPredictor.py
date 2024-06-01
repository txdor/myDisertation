import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def get_connection_string(server, database, driver):
    return f'mssql+pyodbc://@{server}/{database}?driver={driver}&Trusted_Connection=yes'

def fetch_dividend_data(engine, ticker):
    query = f"""
    SELECT year, adjDividend 
    FROM [testDBscript].[dbo].[{ticker}_dividendData]
    """
    return pd.read_sql(query, engine)

def preprocess_data(dividend_data):
    # Filtrarea rândurilor care au valori ne-numerice în coloana year
    dividend_data = dividend_data[dividend_data['year'].apply(lambda x: str(x).isnumeric())]
    # Conversia coloanei year la tipul int
    dividend_data['year'] = dividend_data['year'].astype(int)
    # Filtrarea datelor pentru anii de la 2010 în sus
    dividend_data = dividend_data[dividend_data['year'] >= 2010]
    return dividend_data

def train_model(years, dividends):
    X_train, X_test, y_train, y_test = train_test_split(years, dividends, test_size=0.2, random_state=0)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return model, mse, r2

def predict_future_dividends(model, start_year, end_year):
    future_years = np.array(range(start_year, end_year + 1)).reshape(-1, 1)
    future_dividends = model.predict(future_years)
    return future_years, future_dividends

def plot_results(years, dividends, future_years, future_dividends, model):
    plt.scatter(years, dividends, color='blue', label='Actual Dividends')
    plt.plot(years, model.predict(years), color='red', label='Linear Model')
    plt.scatter(future_years, future_dividends, color='green', label='Predicted Dividends')
    plt.xlabel('Year')
    plt.ylabel('Dividend')
    plt.title('Dividend Prediction')
    plt.legend()
    plt.show()

def main():
    server = 'DESKTOP-B8G31OU'  # Înlocuiește cu numele serverului tău
    database = 'testDBscript'  # Înlocuiește cu numele bazei de date
    driver = 'ODBC Driver 17 for SQL Server'  # Asigură-te că acest driver este instalat
    
    # Crearea string-ului de conexiune
    connection_string = get_connection_string(server, database, driver)
    engine = create_engine(connection_string)
    
    # Solicitarea ticker-ului de la utilizator
    ticker = input("Introduceți ticker-ul companiei: ")
    
    # Preluarea datelor de dividende
    dividend_data = fetch_dividend_data(engine, ticker)
    dividend_data = preprocess_data(dividend_data)
    
    # Pregătirea datelor
    years = dividend_data['year'].values.reshape(-1, 1)
    dividends = dividend_data['adjDividend'].values.reshape(-1, 1)
    
    # Antrenarea modelului
    model, mse, r2 = train_model(years, dividends)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    
    # Prezicerea dividendelor viitoare
    future_years, future_dividends = predict_future_dividends(model, 2024, 2033)
    
    # Vizualizarea rezultatelor
    plot_results(years, dividends, future_years, future_dividends, model)
    
    print("Predicted Dividends for 2024-2033:")
    for year, dividend in zip(future_years, future_dividends):
        print(f"Year: {year[0]}, Predicted Dividend: {dividend[0]}")

if __name__ == "__main__":
    main()
