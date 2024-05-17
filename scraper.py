from selenium import webdriver
from bs4 import BeautifulSoup
import time

def scrape_financial_values(url):
    # Create a new instance of the Chrome driver
    driver_path = r'M:\a\facultate\disertatie\myDisertation\chromedriver-win64\chromedriver-win64.exe'  # make sure this is the correct path

# Initialize Chrome WebDriver
    options = webdriver.ChromeOptions()  # This line ensures you're using ChromeOptions

    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    driver = webdriver.Chrome()
    
    # Open the URL
    driver.get(url)
    
    # Wait for the page to fully load (adjust the time.sleep value if needed)
    time.sleep(5)
    
    # Get the page source after it's fully loaded
    page_source = driver.page_source
    
    # Close the driver
    driver.quit()
    
    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find all <div> elements with the specified class
    divs = soup.find_all('div', class_='w-20 py-1 text-foreground pr-3 text-right text-2xs')
    
    # Extract and return the values
    values = [div.text.strip() for div in divs]
    return values

# URL of the website to scrape
url = "https://roic.ai/quote/AAPL:US"

# Call the function to scrape financial values
financial_values = scrape_financial_values(url)

# Print the scraped values
if financial_values:
    for value in financial_values:
        print(value)
else:
    print("No financial values found.")