from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import os
import time
import io
from math import ceil

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def replace_transparent_background(image, bg_color=(255, 255, 255)):  # Default to white
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", image.size, bg_color + (255,))
        bg.paste(image, mask=alpha)
        return bg.convert('RGB')
    else:
        return image

def download_and_process_image(driver, url, filename, bg_color):
    driver.get(url)
    time.sleep(1)  # Wait for potential redirect or download to start
    
    # Check if file was downloaded
    if os.path.exists(filename):
        # Process the image
        with Image.open(filename) as img:
            processed_img = replace_transparent_background(img, bg_color)
            processed_img.save(filename)
        return True
    return False

def extract_images(base_url, output_dir, num_images=90, max_images=90, bg_color=(0, 0, 0)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    driver = setup_driver()

    # Set Chrome to download files to our output directory
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.path.abspath(output_dir)}}
    driver.execute("send_command", params)

    # Calculate the step size to evenly space out the images
    step = ceil(num_images / max_images)

    # Download and process evenly spaced images
    for i in range(0, num_images, step):
        image_url = f"{base_url}/{i}.png"
        output_file = os.path.join(output_dir, f"{i}.png")
        if download_and_process_image(driver, image_url, output_file, bg_color):
            print(f"Downloaded and processed image {i}")
        else:
            print(f"Failed to download or process image {i}")

    # Download and process the thumbnail if available
    thumbnail_url = f"{base_url}/thumbnail.png"
    thumbnail_file = os.path.join(output_dir, "thumbnail.png")
    if download_and_process_image(driver, thumbnail_url, thumbnail_file, bg_color):
        print("Downloaded and processed thumbnail")
    else:
        print("Thumbnail not available or failed to download/process")

    driver.quit()

if __name__ == "__main__":
    base_url = input("Enter the base URL for the images: ")
    output_dir = input("Enter the output directory: ")
    bg_color_input = input("Enter background color (R,G,B) or press Enter for white: ")
    
    if bg_color_input:
        bg_color = tuple(map(int, bg_color_input.split(',')))
    else:
        bg_color = (255, 255, 255)  # Default to white

    extract_images(base_url, output_dir, bg_color=bg_color)