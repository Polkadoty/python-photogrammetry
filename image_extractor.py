
import requests
import os
from math import ceil

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        return True
    return False

def extract_images(base_url, output_dir, num_images=90, max_images=50):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Calculate the step size to evenly space out the images
    step = ceil(num_images / max_images)

    # Download evenly spaced images
    for i in range(0, num_images, step):
        image_url = f"{base_url}/{i}.png"
        output_file = os.path.join(output_dir, f"image_{i:03d}.png")
        if download_image(image_url, output_file):
            print(f"Downloaded image {i}")
        else:
            print(f"Failed to download image {i}")

    # Download the thumbnail if available
    thumbnail_url = f"{base_url}/thumbnail.png"
    thumbnail_file = os.path.join(output_dir, "thumbnail.png")
    if download_image(thumbnail_url, thumbnail_file):
        print("Downloaded thumbnail")
    else:
        print("Thumbnail not available or failed to download")

if __name__ == "__main__":
    base_url = input("Enter the base URL for the images: ")
    output_dir = input("Enter the output directory: ")
    extract_images(base_url, output_dir)