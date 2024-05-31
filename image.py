# System librairies
import os

# Scraping libraries
from selenium.webdriver.common.by import By
import requests


def save_image(title, images, last_image):
    directory = f'{title}/images'
    os.makedirs(directory, exist_ok=True)
    fifth_image = last_image.find_element(By.TAG_NAME, 'img')
    image = []
    for i in images:
        image.append(i.find_element(By.TAG_NAME, 'img'))
    image.append(fifth_image)
    for idx, img in enumerate(image):
        src = img.get_attribute('src')
        if src:
            img_data = requests.get(src).content
            with open(f'{directory}/image_{idx}.jpg', 'wb') as img_file:
                img_file.write(img_data)
