import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

from login import login

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


def perform_login():
    try:
        # Login
        login(driver, email, password)
    except Exception as e:
        print('An error occurred during login:', str(e))
        raise  # Propagate the exception


def navigate_to_products():
    driver.get('https://affiliate.gramedia.com/content/products')
    print("Navigated to the products page.")
    time.sleep(5)  # Tunggu beberapa detik untuk memastikan halaman sudah termuat
    print("Current URL:", driver.current_url)


def generate_affiliate_link(product_url):
    try:
        driver.get(product_url)
        print(f"Opened product URL: {product_url}")

        # Tunggu hingga tombol "Generate Link" muncul
        generate_button_xpath = "//*[@id='fuse-main']/div/div/div[2]/div[3]/div/div[1]/button"
        generate_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, generate_button_xpath))
        )
        time.sleep(2)  # Tunggu tambahan 2 detik setelah tombol muncul

        generate_button.click()
        print("Clicked on 'Generate Link' button.")
        
        # Tunggu sampai hasil link muncul
        result_input_xpath = "/html/body/div[1]/div/div/main/div/div/div[2]/div[3]/div/div[2]/div/div/input"
        result_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, result_input_xpath))
        )
        
        generated_link = result_element.get_attribute('value')
        print(f"Generated affiliate link: {generated_link}")
        
        time.sleep(3)  # Tunggu beberapa detik setelah mengklik tombol

    except TimeoutException:
        print(f"Timeout waiting for element on {product_url}")
    except Exception as e:
        print(f"Failed to generate link for {product_url}: {str(e)}")


def search_product(keyword, processed_urls):
    try:
        # Navigate to the product search page
        navigate_to_products()

        # Wait for the search input element to be present
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="input-search"]'))
        )
        search_input.clear()
        search_input.send_keys(keyword)
        time.sleep(2)  # Tunggu sebentar untuk memastikan hasil muncul

        wait = WebDriverWait(driver, 10)
        products_list = wait.until(EC.presence_of_element_located((By.ID, 'products-list')))
        product_elements = products_list.find_elements(By.XPATH, ".//a[@href]")

        page_urls = [product.get_attribute('href') for product in product_elements]
        
        # Filter hanya URL yang belum diproses
        new_urls = [url for url in page_urls if url not in processed_urls]
        
        print(f"Found {len(new_urls)} new product URLs.")
        
        for url in new_urls:
            print(url)
            generate_affiliate_link(url)  # Panggil fungsi untuk mengklik tombol di setiap URL produk
            processed_urls.add(url)  # Tambahkan URL ke set URL yang sudah diproses

    except Exception as e:
        print('An error occurred during product search:', str(e))
        raise  # Propagate the exception


def main():
    processed_urls = set()  # Set untuk menyimpan URL yang sudah diproses
    try:
        perform_login()
        search_product('ebook', processed_urls)  # Ganti dengan nama produk yang Anda cari
    finally:
        driver.quit()  # Pastikan browser ditutup setelah selesai


if __name__ == "__main__":
    main()

