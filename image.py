# System librairies
import os

# Scraping libraries
from selenium.webdriver.common.by import By
import requests


def save_image(title, images):
    directory = f'{title}/images'
    os.makedirs(directory, exist_ok=True)
    image = images.find_elements(By.TAG_NAME, 'a')

    for idx, img in enumerate(image):
        url = img.get_attribute('href')
        if url:
            img_data = requests.get(url).content
            with open(f'{directory}/image_{idx}.png', 'wb') as img_file:
                img_file.write(img_data)
