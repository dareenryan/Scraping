import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys


def save_form(bar_code, title, prix):
    result = open(f'{title}/{title}.txt', 'r', encoding='utf-8').readline()
    descript = open(f'{title}/description.html', 'r', encoding='utf-8').read()
    char = open(f'{title}/caractéristique.html', 'r', encoding='utf-8').read()

    options = Options()
    options.add_argument("start-maximized")

    profile_path = os.path.expanduser('~') + '\\AppData\\Local\\Google\\Chrome\\User Data\\'
    options.add_argument(f"--user-data-dir={profile_path}")
    profile_name = 'Profile 2'
    options.add_argument(f'--profile-directory={profile_name}')

    browser = webdriver.Chrome(options=options)
    browser.get('https://autotruck42.com/at@42300/index.php/sell/catalog/products-v2/')
    sleep(2)

    browser.find_element(By.ID, 'page-header-desc-configuration-add').click()
    sleep(4)
    browser.switch_to.frame(browser.find_element(By.TAG_NAME, 'iframe'))
    browser.find_element(By.ID, 'create_product_create').click()
    sleep(4)
    browser.switch_to.parent_frame()
    article = browser.find_element(By.ID, 'product_header_name_2')
    article.send_keys(title)

    browser.execute_script("window.scrollBy(0,400)")
    sleep(2)

    browser.find_element(By.ID, 'mceu_0-button').click()
    sleep(3)
    recap = browser.find_element(By.CLASS_NAME, 'mce-textbox')
    recap.send_keys(char)
    browser.find_element(By.CLASS_NAME, 'mce-primary').click()
    sleep(2)

    browser.execute_script("window.scrollBy(0,400)")

    browser.find_element(By.ID, 'mceu_147-button').click()
    sleep(2)
    description = browser.find_element(By.CLASS_NAME, 'mce-textbox')
    description.send_keys(descript)
    browser.find_element(By.CLASS_NAME, 'mce-primary').click()
    sleep(2)

    browser.execute_script("window.scrollBy(0,-600)")

    browser.find_element(By.ID, 'product_details-tab-nav').click()
    sleep(2)
    ref = browser.find_element(By.ID, 'product_details_references_reference')
    ref.send_keys(result)
    code = browser.find_element(By.ID, 'product_details_references_ean_13')
    code.send_keys(bar_code)

    browser.find_element(By.ID, 'product_pricing-tab-nav').click()
    sleep(2)
    browser.execute_script("window.scrollBy(0,-600)")
    sleep(2)
    div_price = browser.find_element(By.CLASS_NAME, 'retail-price-tax-excluded')
    price = div_price.find_element(By.TAG_NAME, 'input')

    price.click()
    sleep(5)
    price.clear()
    sleep(2)
    for i in range(8):
        price.send_keys(Keys.BACKSPACE)
    sleep(1)
    price.send_keys(str(round(float(prix.split(' ')[0])*1.5, 4)))
    sleep(2)

    browser.find_element(By.ID, 'product_seo-tab-nav').click()
    sleep(3)
    balise = browser.find_element(By.ID, 'product_seo_meta_title_2')
    balise.send_keys(result)
    meta = browser.find_element(By.ID, 'product_seo_meta_description_2')
    meta.send_keys(f'{result}. Livraison express 24h')

    save_button = browser.find_element(By.ID, 'product_footer_save')
    wait(browser, 1200).until(EC.element_to_be_selected(save_button))
    browser.quit()
