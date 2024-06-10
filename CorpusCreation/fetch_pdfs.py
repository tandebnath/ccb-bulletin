from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import requests
import os
import time

def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*\n\r' + ''.join([chr(i) for i in range(32)])  # Add any other invalid characters
    sanitized = ''.join([c if c not in invalid_chars else '_' for c in filename])  # Replace invalid characters with '_'
    return sanitized.strip().replace(' ', '_')

# Setup the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

url = "https://www.ideals.illinois.edu/units/119"
driver.get(url)

# Wait for the page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "pagination"))
)

# Directory to save PDF files
download_dir = "downloaded_pdfs"
os.makedirs(download_dir, exist_ok=True)

main_window = driver.current_window_handle

for i in range(1, 26):  # 25 pages
    print(f"Accessing page {i}...")  # Log the current page number
    
    # Wait and find the pagination container
    pagination_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pagination"))
    )

    # Locate all divs with class 'd-flex resource-list mb-3' and store PDF links
    resource_list_divs = driver.find_elements(By.CSS_SELECTOR, 'div.d-flex.resource-list.mb-3')
    pdf_links = [div.find_element(By.CSS_SELECTOR, 'div.flex-grow-1.ms-3 h5 a').get_attribute('href') for div in resource_list_divs]
    
    for pdf_link in pdf_links:
        print(f"Opening link: {pdf_link}")  # Print the href of the PDF
        # Open the link in a new tab
        driver.execute_script(f"window.open('{pdf_link}', 'new_window')")
        driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab
        
        # Wait for the dropdown to be present and extract the data-bitstream-url
        bitstream_url = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.dropdown a#copy-link'))
        ).get_attribute('data-bitstream-url')

        # Extract the title from the page
        page_title = driver.find_element(By.TAG_NAME, 'title').get_attribute('innerText').strip()
        sanitized_title = sanitize_filename(page_title)  # Sanitize the page title to use it as a filename

        # Close the current tab and switch back to the main window
        driver.close()
        driver.switch_to.window(main_window)
        
        # Download the PDF
        response = requests.get(bitstream_url, stream=True)
        pdf_file_path = os.path.join(download_dir, sanitized_title + ".pdf")  # Use the sanitized page title as the filename
        with open(pdf_file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {pdf_file_path}")  # Log the downloaded file path
    
    # Click the "next page" link (»), which is the 8th item in the pagination container
    if i < 25:  # No need to click on the last page
        next_page_link = pagination_container.find_elements(By.CSS_SELECTOR, "li.page-item a.page-link")[7]
        # Scroll the element into view and then click
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page_link)
        time.sleep(1)  # Wait a bit for scrolling to finish
        next_page_link.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination")))  # Wait for the next page to load

# Cleanup
driver.quit()

print("All PDFs downloaded.")
