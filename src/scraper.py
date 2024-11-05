import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import create_engine, text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


# Function to scrape the main fragrance list
# def scrape_fragrance_links():
#     url = 'https://www.wikiparfum.com/en/fragrances'
#     base_url = 'https://www.wikiparfum.com'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     links_scraped = []
#     for item in soup.find_all('div', class_='col-span-4 sm:col-span-2 md:col-span-4 lg:col-span-3 xl:col-span-2'):
#         link = item.find('a')['href']
#         links_scraped.append(base_url + link)
#
#     return links_scraped
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def scrape_fragrance_links(driver):
    base_url = 'https://www.wikiparfum.com'
    links_scraped = []

    # Set up Selenium WebDriver (make sure to have the correct driver for your browser)
    driver = webdriver.Chrome()  # or webdriver.Firefox() based on your preference
    driver.get('https://www.wikiparfum.com/en/fragrances')

    while True:
        time.sleep(2)  # Wait for the page to load

        # Scrape the current items
        items = driver.find_elements(By.CSS_SELECTOR,
                                     'div.col-span-4.sm\\:col-span-2.md\\:col-span-4.lg\\:col-span-3.xl\\:col-span-2')

        if not items:
            break  # Break the loop if no items are found

        for item in items:
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            links_scraped.append(link)

        print(f'Page scraped, found {len(items)} items.')  # Print the number of items found

        # Click the "Load More" button
        try:
            # Wait for the button to be clickable
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Load more']")))

            button = driver.find_element(By.XPATH, "//button[text()='Load more']")

            # Check if the button is disabled by checking class or disabled attribute
            if "disabled" in button.get_attribute("class") or button.get_attribute("disabled") is not None:
                # Remove the 'disabled' class or attribute and try clicking it
                driver.execute_script("arguments[0].removeAttribute('disabled');", button)
                driver.execute_script("arguments[0].classList.remove('disabled:text-grey700');", button)

                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", button)

                # Use ActionChains to click the button to ensure no interception
                actions = ActionChains(driver)
                actions.move_to_element(button).click().perform()

                print("Clicked 'Load more' button.")
            else:
                print("Button is not disabled or already clicked.")

        except Exception as e:
            print("No more items to load or error occurred:", e)
            continue  # Exit if the button is not found or another error occurs

    driver.quit()  # Close the browser
    return links_scraped



def create_new_driver():
    # Initialize the Selenium WebDriver
    service = Service(r"C:\Users\admin\Documents\fragrances\chromedriver.exe")

    # Set options for Chrome
    options = webdriver.ChromeOptions()

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# Function to scrape data from individual fragrance pages
def scrape_fragrance_data(lnk, driver):
    driver.get(lnk)

    # Give the page time to load (if necessary)
    WebDriverWait(driver, 10)
    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    brand = soup.find('h6', class_='uppercase text-14 md:text-labLarge').text.strip()
    name = soup.find('h1', class_='text-h1Mobile md:text-h1 font-secondary mt-6 mb-1.5').text.strip()
    desc = soup.find('span', class_='text-16 md:text-18 font-light markdown').text.strip()
    meta_tag = soup.find('meta', {'name': 'description'})
    content = meta_tag['content']
    ingredients_start = content.find("made from") + len("made from ")
    ingredients_string = content[ingredients_start:]
    # Split the ingredients by commas and clean up spaces
    ingredients = [ingredient.strip() for ingredient in ingredients_string.split(',')]
    ings = []
    for ingredient in ingredients:
        sub_ingredients = [sub.strip() for sub in ingredient.split('/')]
        ings.extend(sub_ingredients)

    # Locate the <dt> for "Concepts" and find the next <dl> element
    concepts_dl = soup.find('dt', string='Concepts').find_next('dl')
    # Fetch concepts directly from the located <dl> tag
    concepts = [concept.strip().strip(',') for concept in concepts_dl.get_text(strip=True).split(',')]

    return {'Brand': brand, 'Name': name, 'Description': desc, 'Notes': ings, 'Concepts': concepts}


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
