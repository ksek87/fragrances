import os
import pandas as pd
import scraper as sc
from time import sleep

def scrape_data_for_links(links, driver):
    """Scrapes data for each link and returns a list of results."""
    all_data = []
    for link in links:
        try:
            # Scrape fragrance data for each link
            fragrance_data = sc.scrape_fragrance_data(link, driver)
            all_data.append(fragrance_data)
        except AttributeError as error:
            # Handle specific error if scraping data fails for a link
            print(f"Error scraping data for link {link}: {error}. Skipping this entry.")
        except Exception as error:
            # Handle other unexpected errors
            print(f"Unexpected error scraping data for link {link}: {error}. Skipping this entry.")
        sleep(1)  # Optional: Adds a small delay to avoid overloading the server.
    return all_data

def save_to_csv(data, file_name="fragrance-data-az.csv"):
    """Saves the scraped data to a CSV file."""
    if data:
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)
        print(f"Dataset saved as CSV file: {file_name}")
    else:
        print("No data scraped. CSV file not saved.")

def scrape_and_save_data():
    """Main function to scrape and save fragrance data."""
    try:
        # Set the file names
        input_file_name = "fragrance_links_az.csv"  # The input CSV file
        output_file_name = "fragrance-data-az.csv"  # The output CSV file

        # Get the current working directory
        cwd = os.getcwd()  # This gives the current working directory
        print(f"Current Working Directory: {cwd}")

        # Construct the full path to the input file (fragrance_links.csv)
        input_file_path = os.path.join(cwd, input_file_name)

        # Check if the input CSV file exists
        if os.path.exists(input_file_path):
            print(f"CSV file '{input_file_name}' exists. Loading links from CSV...")

            # Load the links from the existing CSV file
            df = pd.read_csv(input_file_path)
            links = df['Fragrance Link'].tolist()  # Assuming the CSV has a 'link' column
            print(f"Loaded {len(links)} links from CSV.")

            # Create a new driver for scraping
            driver = sc.create_new_driver()

            # Scrape data for the existing links
            all_data = scrape_data_for_links(links, driver)

            # Save the scraped data to the output CSV file
            save_to_csv(all_data, output_file_name)

            driver.quit()
        else:
            print(f"CSV file '{input_file_name}' not found. Starting the scraping process...")

            # Create a new driver for scraping
            driver = sc.create_new_driver()

            # Scrape the links for fragrance data
            links = sc.scrape_fragrance_links(driver)
            print(f'Number of links: {len(links)}')

            # Scrape data for the new links
            all_data = scrape_data_for_links(links, driver)

            # Save the scraped data to the output CSV file
            save_to_csv(all_data, output_file_name)

            driver.quit()

    except Exception as error:
        print(f"An unexpected error occurred: {error}")

if __name__ == "__main__":
    scrape_and_save_data()
