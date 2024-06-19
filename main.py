import os
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrape import  navigate_to_products, scrape_product_urls
from login import login
# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape product URLs from Gramedia affiliate site.')
    parser.add_argument('-p', '--pages', type=int, default=1, 
                        help='Number of pages to scrape (default: 1). Use 0 for scraping all pages.')
    return parser.parse_args()

# Path to the chromedriver executable
chromedriver_path = '/usr/bin/chromedriver'

# Email dan password diambil dari variabel lingkungan
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
# Set options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver with options
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Parse command-line arguments
    args = parse_arguments()
    pages_to_scrape = args.pages

    # Perform login
    login(driver, email, password)

    # Navigate to products page
    navigate_to_products(driver)

    # Scrape product URLs
    scraped_urls = scrape_product_urls(driver, pages_to_scrape)

    # Optionally, process scraped URLs further

except Exception as e:
    print('An error occurred:', str(e))

finally:
    driver.quit()
