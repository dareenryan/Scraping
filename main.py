# Core librairies
from time import sleep

# System librairies
import sys
import os

# Scraping libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def word_replace(filename, old_word, new_word):
    file = open(filename, 'r', encoding='utf-8')
    filedata = file.read()
    data = filedata.replace(old_word, new_word)
    file = open(filename, 'w', encoding='utf-8')
    file.write(data)


def save_characteristic_html(title, manufacturer, list_char_name, list_char_value):
    directory = title
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, 'caractéristique.html')

    file = open(file_path, 'w', encoding='utf-8')
    file.write('<p><b>Caractéristiques:</b></p>')
    file.write('<ul>')
    file.write('<li>Marque: ' + manufacturer + '</li><li>Qualité Premium</li><li>Neuf</li><li>Garantie 2 ans</li>')
    for i in range(len(list_char_name)):
        file.write('<li>' + str(list_char_name[i]) + ' ' + str(list_char_value[i])+'</li>')
    file.write('</ul>')
    file.close()


def save_description_html(title, manufacturer, article, list_ref, list_producer, list_char_name, list_char_value, list_brand, list_model):
    producer_dict = {}

    directory = title
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, 'description.html')

    file = open(file_path, 'w', encoding='utf-8')

    file.write('<h3>')
    if 'Tention [ V ]' in list_char_name:
        index = list_char_name.index('Tention [ V ]')
        file.write(article + ' ' + str(list_char_value[index]) + 'V ')
    if 'Puissance [ kW ]' in list_char_name:
        index = list_char_name.index('Puissance [ kW ]')
        file.write(str(list_char_value[index]) + 'kW ')
    if 'Nombre de dents [ qty. ]' in list_char_name:
        index = list_char_name.index('Nombre de dents [ qty. ]')
        file.write(str(list_char_value[index]) + ' dents ')

    if len(list_ref) >= 5:
        for i in range(5):
            ref = list_ref[i]
            prod = list_producer[i]
            if prod in producer_dict:
                producer_dict[prod].append(ref)
            else:
                producer_dict[prod] = [ref]
    else:
        for i in range(len(list_ref)):
            ref = list_ref[i]
            prod = list_producer[i]
            if prod in producer_dict:
                producer_dict[prod].append(ref)
            else:
                producer_dict[prod] = [ref]

    combined = [f"{prod} {' '.join(refs)}" for prod, refs in producer_dict.items()]
    result = ", ".join(combined)
    file.write(result)
    file.write('</h3>')

    file.write('<b>Les engagements AutoTruck42:</b><br>')
    file.write('<ul>')
    file.write('<li>Boutique 100% française</li><li>Situé à Mably dans la Loire 42300</li>')
    file.write('<li>Un professionnel au téléphone du Lundi au Vendredi 09h00/16h00</li>')
    file.write('<li>Une livraison en 24/48h (Point relais, Express en 24h)</li>')
    file.write('<li>Traitement de la commande le jour même avant 16 h00</li>')
    file.write('<li>Une réponse à toutes vos en 2h Max de 9h00 à 16h00 et dans la journée 7jrs/7 de 6h00 à 22h00</li>')
    file.write('<li>Des produits de qualité au normes FR & EU</li>')
    file.write('<li>Garantie 2 ans</li>')
    file.write('</ul>')

    file.write('<br><b>Caractéristique</b><br>')
    file.write('<ul>')
    file.write('<li>Marque: ' + manufacturer + '</li><li>Qualité Premium</li>')
    file.write('<li>Neuf</li><li>Garantie 2 ans</li>')
    for j in range(len(list_char_name)):
        file.write('<li>' + str(list_char_name[j]) + ' ' + str(list_char_value[j]) + '</li>')
    file.write('</ul>')

    file.write('<br><b>Référence équivalente</b><br>')
    file.write('<ul>')
    for i in range(len(list_ref)):
        file.write('<li>' + str(list_ref[i]) + ' ' + str(list_producer[i]) + '</li>')
    file.write('</ul>')

    file.write('<br><b>Compatible avec:</b><br>')
    file.write('<ul>')
    for k in range(len(list_brand)):
        file.write('<li>' + str(list_brand[k]) + ' ' + str(list_model[k]) + '</li>')
    file.write('</ul>')

    file.close()
    word_replace(file_path, 'Demarreur', 'Démarreur')
    word_replace(file_path, 'demarreur', 'démarreur')
    word_replace(file_path, 'filetes', 'filetés')
    word_replace(file_path, 'Tention', 'Tension')
    word_replace(file_path, 'qty.', 'qté.')


def save_description_txt(title, manufacturer, article, ref_producer_list, char_table_name, char_table_value, row_brand_model):
    list_ref = []
    list_producer = []
    list_char_name = []
    list_char_value = []
    big_list_brand = []
    big_list_model = []
    producer_dict = {}

    # Nom de référence et numéro de référence
    for element in ref_producer_list:
        list_ref.append(element.find_element(By.TAG_NAME, 'a').text)
        list_producer.append(element.find_element(By.CLASS_NAME, '_producer_1s9a0_56').text)

    # Nom de caractéristique
    for char_name in char_table_name:
        list_char_name.append(char_name.text)

    # Valeur de caractéristique
    for char_value in char_table_value:
        list_char_value.append(char_value.text)

    # Liste de marque et de modèle
    for i in range(0, len(row_brand_model), 5):
        big_list_brand.append(row_brand_model[0+i])
        big_list_model.append(row_brand_model[1+i])

    list_model = []
    list_brand = []
    list_set = set()
    # Suppression des redondances des paires marque et modèle
    for i in range(len(big_list_model)):
        if big_list_model[i] in list_set:
            continue
        else:
            list_brand.append(big_list_brand[i])
            list_model.append(big_list_model[i])
            list_set.add(big_list_model[i])

    directory = title
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f'{title}.txt')
    file = open(file_path, 'w', encoding='utf-8')

    if 'Tention [ V ]' in list_char_name:
        index = list_char_name.index('Tention [ V ]')
        file.write(article + ' ' + str(list_char_value[index]) + 'V ')
    else:
        file.write(article + ' ')
    if 'Puissance [ kW ]' in list_char_name:
        index = list_char_name.index('Puissance [ kW ]')
        file.write(str(list_char_value[index]) + 'kW ')
    else:
        file.write(' ')
    if 'Nombre de dents [ qty. ]' in list_char_name:
        index = list_char_name.index('Nombre de dents [ qty. ]')
        file.write(str(list_char_value[index]) + ' dents ')
    else:
        file.write(' ')

    if len(list_ref) >= 5:
        for i in range(5):
            ref = list_ref[i]
            prod = list_producer[i]
            if prod in producer_dict:
                producer_dict[prod].append(ref)
            else:
                producer_dict[prod] = [ref]
    else:
        for i in range(len(list_ref)):
            ref = list_ref[i]
            prod = list_producer[i]
            if prod in producer_dict:
                producer_dict[prod].append(ref)
            else:
                producer_dict[prod] = [ref]

    combined = [f"{prod} {' '.join(refs)}" for prod, refs in producer_dict.items()]
    result = ", ".join(combined)
    file.write(result)

    file.write('\n\nCaractéristique\n\n')
    file.write('Marque: ' + manufacturer + '\nQualité Premium\nNeuf\nGarantie 2 ans\n')
    for j in range(len(list_char_name)):
        file.write(str(list_char_name[j]) + ' ' + str(list_char_value[j])+'\n')

    file.write('\n\nRéférence équivalente\n\n')
    for i in range(len(list_ref)):
        file.write(str(list_ref[i]) + ' ' + str(list_producer[i])+'\n')

    file.write('\n\nCompatible avec:\n\n')
    for k in range(len(list_brand)):
        file.write(str(list_brand[k]) + ' ' + str(list_model[k]) + '\n')

    file.close()
    word_replace(file_path, 'Demarreur', 'Démarreur')
    word_replace(file_path, 'demarreur', 'démarreur')
    word_replace(file_path, 'filetes', 'filetés')
    word_replace(file_path, 'Tention', 'Tension')
    word_replace(file_path, 'qty.', 'qté.')

    save_characteristic_html(title, manufacturer, list_char_name, list_char_value)
    save_description_html(title, manufacturer, article, list_ref, list_producer, list_char_name, list_char_value, list_brand, list_model)
    word_replace(os.path.join(directory, 'caractéristique.html'), 'demarreur', 'démarreur')
    word_replace(os.path.join(directory, 'caractéristique.html'), 'filetes', 'filetés')
    word_replace(os.path.join(directory, 'caractéristique.html'), 'Tention', 'Tension')
    word_replace(os.path.join(directory, 'caractéristique.html'), 'qty.', 'qté.')


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
        item.click()
        sleep(1)
        brand_model = browser.find_element(By.CLASS_NAME, 'table-striped')
        rows = brand_model.find_elements(By.TAG_NAME, 'td')
        for row in rows:
            row_brand_model.append(row.text)

    save_description_txt(title, manufacturer, article, element_list, char_table_name, char_table_value, row_brand_model)
    browser.quit()


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
