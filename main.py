from time import sleep

import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def word_replace(filename, old_word, new_word):
    file = open(filename, 'r', encoding='utf-8')
    filedata = file.read()
    data = filedata.replace(old_word, new_word)
    file.close()
    file = open(filename, 'w', encoding='utf-8')
    file.write(data)
    file.close()


def save_data(title, manufacturer, article, ref_producer_list, char_table_name, char_table_value, row_brand_model):
    list_ref = []
    list_producer = []
    list_char_name = []
    list_char_value = []
    list_brand = []
    list_model = []
    list_type = []
    producer_dict = {}

    for element in ref_producer_list:
        list_ref.append(element.find_element(By.TAG_NAME, 'a').text)
        list_producer.append(element.find_element(By.CLASS_NAME, '_producer_1s9a0_56').text)

    for char_name in char_table_name:
        list_char_name.append(char_name.text)

    for char_value in char_table_value:
        list_char_value.append(char_value.text)

    for i in range(0, len(row_brand_model), 5):
        list_brand.append(row_brand_model[0+i])
        list_model.append(row_brand_model[1+i])
        list_type.append(row_brand_model[2+i])

    file = open(f'{title}.txt', 'w', encoding='utf-8')

    file.write(article + ' ' + str(list_char_value[0]) + 'V ' + str(list_char_value[1]) + 'kW ' + str(list_char_value[5]) + ' dents ')

    for i in range(5):
        ref = list_ref[i]
        prod = list_producer[i]
        if prod in producer_dict:
            producer_dict[prod].append(ref)
        else:
            producer_dict[prod] = [ref]

    combined = [f"{prod} {' '.join(refs)}" for prod, refs in producer_dict.items()]
    result = ", ".join(combined)
    file.write(result)

    file.write('\n\nRéférence Equivalente\n\n')
    for i in range(len(list_ref)):
        file.write(str(list_ref[i]) + ' ' + str(list_producer[i])+'\n')

    file.write('\n\n#Caractéristique\n\n')
    file.write('Marque: ' + manufacturer + '\nQualité Premium\nNeuf\nGarantie 2 ans\n')
    for j in range(len(list_char_name)):
        file.write(str(list_char_name[j]) + ' ' + str(list_char_value[j])+'\n')

    file.write('\n\n#Applications\n\n')
    for k in range(len(list_brand)):
        file.write(str(list_brand[k]) + ' ' + str(list_model[k])+'\n')

    file.close()
    word_replace(f'{title}.txt', 'Demarreur', 'Démarreur')
    word_replace(f'{title}.txt', 'demarreur', 'démarreur')
    word_replace(f'{title}.txt', 'filetes', 'filetés')
    word_replace(f'{title}.txt', 'Tention', 'Tension')
    word_replace(f'{title}.txt', 'qty.', 'qté.')


def scrape(url):
    row_brand_model = []
    options = Options()

    options.add_argument("--headless")

    browser = webdriver.Chrome(options=options)
    browser.get(url)
    sleep(2)

    title = browser.find_element(By.CLASS_NAME, 'product-name').text

    manufacturer = browser.find_element(By.CSS_SELECTOR, '[itemprop="manufacturer"]').text

    article = browser.find_element(By.CLASS_NAME, 'categories').text

    element_list = browser.find_elements(By.CLASS_NAME, '_referenceRow_1s9a0_47')

    char_table = browser.find_element(By.CLASS_NAME, 'table-bordered')
    char_table_name = char_table.find_elements(By.CSS_SELECTOR, '[style="width: 210px;"]')
    char_table_value = char_table.find_elements(By.TAG_NAME, 'a')

    applications_list = browser.find_elements(By.CLASS_NAME, 'usage-el')

    for item in applications_list:
        # row = []
        item.click()
        sleep(1)
        brand_model = browser.find_element(By.CLASS_NAME, 'table-striped')
        rows = brand_model.find_elements(By.TAG_NAME, 'td')
        for row in rows:
            row_brand_model.append(row.text)

    save_data(title, manufacturer, article, element_list, char_table_name, char_table_value, row_brand_model)
    browser.quit()


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
