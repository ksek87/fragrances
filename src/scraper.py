import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine, text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

# Function to scrape the main fragrance list
def scrape_fragrance_links():
    url = 'https://www.wikiparfum.com/en/fragrances'
    base_url = 'https://www.wikiparfum.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links_scraped = []
    for item in soup.find_all('div', class_='col-span-4 sm:col-span-2 md:col-span-4 lg:col-span-3 xl:col-span-2'):
        link = item.find('a')['href']
        links_scraped.append(base_url + link)

    return links_scraped


# Function to scrape data from individual fragrance pages
def scrape_fragrance_data(lnk):
    # Initialize the Selenium WebDriver
    service = Service(r"C:\Users\admin\Documents\fragrances\chromedriver.exe")

    # Set options for Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(lnk)

    # Give the page time to load (if necessary)
    driver.implicitly_wait(10)
    sleep(1.5)
    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    brand = soup.find('h6',class_='uppercase text-14 md:text-labLarge').text.strip()
    name = soup.find('h1', class_='text-h1Mobile md:text-h1 font-secondary mt-6 mb-1.5').text.strip()
    desc = soup.find('span', class_='text-16 md:text-18 font-light markdown').text.strip()

    driver.quit()
    return {'Brand': brand, 'Name': name, 'Description': desc}


# Function to save new data to the database
def save_new_to_database(df):
    engine = create_engine('sqlite:///fragrance_db.sqlite')  # Change as needed
    with engine.connect() as conn:
        for index, row in df.iterrows():
            # Check if the record already exists
            query = text("SELECT COUNT(*) FROM fragrances WHERE Name = :name")
            count = conn.execute(query, {'name': row['Name']}).scalar()
            if count == 0:
                # Insert new record if it doesn't exist
                insert_query = text("INSERT INTO fragrances (Name, Price) VALUES (:name, :price)")
                conn.execute(insert_query, {'name': row['Name'], 'price': row['Price']})

# if __name__ == "__main__":
#     links = scrape_fragrance_links()
#     all_data = []
#
#     for link in links:
#         fragrance_data = scrape_fragrance_data(link)
#         all_data.append(fragrance_data)
#
#     df = pd.DataFrame(all_data)
#     df.to_csv("fragrance-data.csv")
#     #save_new_to_database(df)
