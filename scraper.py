from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Setează calea către driverul browserului tău (ex. chromedriver)
driver_path = 'https://roic.ai/quote/AAPL:USr'
driver = webdriver.Chrome(driver_path)

# Deschide URL-ul
url = 'https://roic.ai/quote/AAPL:US'
driver.get(url)

# Așteaptă câteva secunde pentru a se încărca pagina
time.sleep(5)

# Obține sursa paginii și creează un obiect BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Închide browserul
driver.quit()

# Acum poți folosi BeautifulSoup pentru a extrage datele
data_containers = soup.find_all('div', {'data-cy': 'financial_table_value'})
rows = []
for container in data_containers:
    cols = container.find_all('div', class_='w-20 py-1 text-foreground pr-3 text-right text-2xs')
    row_data = [col.get_text(strip=True) for col in cols]
    rows.append(row_data)

# Creare DataFrame cu datele
df = pd.DataFrame(rows)

# Afișează DataFrame-ul
print(df)
