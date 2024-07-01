# Scraping

---

## Description du projet

Script Python pour effectuer du scraping sur des pages web d'articles de mécanique

---

## Procédure d'usage
1. Installer la librairie selenium à l'aide de la commande suivante
>pip install selenium
2. S'assurer d'avoir une version de Chrome compatible avec le [**chromedriver**](https://sites.google.com/chromium.org/driver/downloads) en consultant le lien officiel
3. Changer la valeur de la variable [**profile_name**](main.py) à la ***ligne 272*** avec le nom de votre profile Chrome.
* Pour savoir quel nom mettre, consulter ce dossier 
**C:\Users\ *nom_utilisateur* \AppData\Local\Google\Chrome\User Data** dans votre ordinateur et n'oubliez pas de mettre votre nom d'utilisateur.
4. Pour éxécuter il suffit d'entrer la commande suivante
>py main.py scrape url_page_web1,url_page_web2,url_page_web3
