from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from math import ceil

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def download_image(driver, url, filename):
    driver.get(url)
    time.sleep(1)  # Wait for potential redirect or download to start
    
    # Check if file was downloaded
    if os.path.exists(filename):
        return True
    return False

def extract_images(base_url, output_dir, num_images=90, max_images=50):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    driver = setup_driver()

    # Set Chrome to download files to our output directory
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.path.abspath(output_dir)}}
    driver.execute("send_command", params)

    # Calculate the step size to evenly space out the images
    step = ceil(num_images / max_images)

    # Download evenly spaced images
    for i in range(0, num_images, step):
        image_url = f"{base_url}/{i}.png"
        output_file = os.path.join(output_dir, f"{i}.png")
        if download_image(driver, image_url, output_file):
            print(f"Downloaded image {i}")
        else:
            print(f"Failed to download image {i}")

    # Download the thumbnail if available
    thumbnail_url = f"{base_url}/thumbnail.png"
    thumbnail_file = os.path.join(output_dir, "thumbnail.png")
    if download_image(driver, thumbnail_url, thumbnail_file):
        print("Downloaded thumbnail")
    else:
        print("Thumbnail not available or failed to download")

    driver.quit()

if __name__ == "__main__":
    base_url = input("Enter the base URL for the images: ")
    output_dir = input("Enter the output directory: ")
    extract_images(base_url, output_dir)