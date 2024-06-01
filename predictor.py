import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Detalii de conexiune la SQL Server
server = 'DESKTOP-B8G31OU'  # Înlocuiește cu numele serverului tău
database = 'testDBscript'  # Înlocuiește cu numele bazei de date
driver = 'ODBC Driver 17 for SQL Server'  # Asigură-te că acest driver este instalat

# Crearea string-ului de conexiune
connection_string = f'mssql+pyodbc://@{server}/{database}?driver={driver}&Trusted_Connection=yes'
engine = create_engine(connection_string)

# Citirea datelor din tabelul AAPL_dividendData
query = """
SELECT year, adjDividend 
FROM [testDBscript].[dbo].[AAPL_dividendData]
"""
dividend_data = pd.read_sql(query, engine)

# Filtrarea rândurilor care au valori ne-numerice în coloana year
dividend_data = dividend_data[dividend_data['year'].apply(lambda x: str(x).isnumeric())]

# Conversia coloanei year la tipul int
dividend_data['year'] = dividend_data['year'].astype(int)

# Filtrarea datelor pentru anii de la 2010 în sus
dividend_data = dividend_data[dividend_data['year'] >= 2010]

# Pregătirea datelor
years = dividend_data['year'].values.reshape(-1, 1)
dividends = dividend_data['adjDividend'].values.reshape(-1, 1)

# Separarea datelor în seturi de antrenament și testare
X_train, X_test, y_train, y_test = train_test_split(years, dividends, test_size=0.2, random_state=0)

# Crearea modelului de regresie liniară
model = LinearRegression()

# Antrenarea modelului
model.fit(X_train, y_train)

# Prezicerea dividendelor pe setul de testare
y_pred = model.predict(X_test)

# Evaluarea modelului
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Prezicerea dividendelor viitoare (2024-2033)
future_years = np.array([2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033]).reshape(-1, 1)
future_dividends = model.predict(future_years)

# Vizualizarea rezultatelor
plt.scatter(years, dividends, color='blue', label='Actual Dividends')
plt.plot(years, model.predict(years), color='red', label='Linear Model')
plt.scatter(future_years, future_dividends, color='green', label='Predicted Dividends')
plt.xlabel('Year')
plt.ylabel('Dividend')
plt.title('Dividend Prediction')
plt.legend()
plt.show()

print("Predicted Dividends for 2024-2033:")
for year, dividend in zip(future_years, future_dividends):
    print(f"Year: {year[0]}, Predicted Dividend: {dividend[0]}")
