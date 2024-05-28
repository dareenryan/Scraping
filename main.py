from time import sleep

import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def save_data(title, ref_producer_list, char_table_name, char_table_value, row_brand_model):
    list_ref = []
    list_producer = []
    list_char_name = []
    list_char_value = []
    list_brand = []
    list_model = []

    for element in ref_producer_list:
        list_ref.append(element.find_element(By.TAG_NAME, 'a').text)
        list_producer.append(element.find_element(By.CLASS_NAME, '_producer_1s9a0_56').text)

    for char_name in char_table_name:
        list_char_name.append(char_name.text)

    for char_value in char_table_value:
        list_char_value.append(char_value.text)

    for i in row_brand_model:
        list_brand.append(row_brand_model[0].text)
        list_model.append(row_brand_model[1].text)

    file = open(f'{title}.txt', 'a', encoding='utf-8')
    file.write('#Référence\n\n')
    for i in range(len(list_ref)):
        file.write(str(list_ref[i]) + ' ' + str(list_producer[i])+'\n')

    file.write('\n\n\n#Caractéristique\n\n')
    for j in range(len(list_char_name)):
        file.write(str(list_char_name[j]) + ' ' + str(list_char_value[j])+'\n')

    file.write('\n\n\n#Applications\n\n')
    for k in range(len(list_brand)):
        file.write(str(list_brand[k]) + ' ' + str(list_model[k])+'\n')

    file.close()


def scrape(url):
    options = Options()

    options.add_argument("--headless")

    browser = webdriver.Chrome(options=options)
    browser.get(url)
    sleep(3)

    title = browser.find_element(By.CLASS_NAME, 'product-name').text

    element_list = browser.find_elements(By.CLASS_NAME, '_referenceRow_1s9a0_47')

    char_table = browser.find_element(By.CLASS_NAME, 'table-bordered')
    char_table_name = char_table.find_elements(By.CSS_SELECTOR, '[style="width: 210px;"]')
    char_table_value = char_table.find_elements(By.TAG_NAME, 'a')

    applications_list = browser.find_elements(By.CLASS_NAME, 'usage-el')

    for item in applications_list:
        item.click()
        sleep(3)
        #WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-striped')))
        brand_model = browser.find_element(By.CLASS_NAME, 'table-striped')
        row_brand_model = brand_model.find_elements(By.TAG_NAME, 'td')

    save_data(title, element_list, char_table_name, char_table_value, row_brand_model)
    browser.quit()


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
