
#################################################################################################################################                                                                                                                           
#                                        Fichier des fonctionx d'initialisation                                                 #
#################################################################################################################################

import requests
import wget
import zipfile
import os, sys
from seleniumwire.webdriver import Chrome

import json
import tkgen.gengui
import webbrowser

from time import sleep

def download_file(download_url, name_of_file, is_zip):
    """
    ############## description ##############\n
    Télécharge un fichier.

    ######### parametre(s) et resultat(s) #########\n
    :param download_url: [str] Url de téléchargement.
    :param name_of_file: [str] Nom du fichier à téléchargé.
    :param is_zip: [bool] Si le document téléchargé est un zip
    :return: None
    """
    file = wget.download(download_url, name_of_file)

    if is_zip:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall()
        
        os.remove(file)

def set_driver():
    """
    ############## description ##############\n
    Initialise un driver selenium.

    ######### parametre(s) et resultat(s) #########\n
    :return: [class selenium Chrom driver] Driver de la fenêtre Chrome.
    """
    driver= Chrome()
    driver.implicitly_wait(1)
    with open("file/xpath.json", "r", encoding="utf-8") as f:
        json_data = json.loads(f.read())
        driver.scopes = json_data["name_of_package"]
    print("[set_driver] driver ok")
    return driver

def update_driver():
    """
    ############## description ##############\n
    Update le driver en téléchargeant sa nouvelle versions.

    ######### parametre(s) et resultat(s) #########\n
    :return: None
    """
    response = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
    version_number = response.text
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"
    download_file(download_url, "chromedriver.zip", True)




def init(driver, loading_screen):
    """
    ############## description ##############\n
    Se charge de l'initialisation générale:

    -:Vérifie la version et met à jour le logiciel.
    -:Met à jours directement le fichier des xpath (chemin pour le web browsing).
    -:Affiche une pop-up si indiquer dans les données d'initialisation.
    -:Verrouille le programme pour maintenance.

    ######### parametre(s) et resultat(s) #########\n
    :param driver: [class selenium Chrom driver] Driver de la fenêtre Chrome.
    :param loading_screen: [Tkinter widget] Barre de chargement de l'écran de chargement.
    :return: None
    """
    loading_screen.next_process("getting init data...", 50) #affichage du chargement
    init_data = get_init_data(driver) #Récupération des données d'Init

    with open("file/version.json", "r", encoding="utf-8") as f:
        version = json.loads(f.read())

        loading_screen.next_process("looking for update...", 60)
        if version["version"] != init_data["version"]["tag"]: #vérification de la verion
            #Mise à jour
            loading_screen.next_process("downloading new version...", 70)
            driver.close()
            print("[init] wrong versions use updating")
            download_file(init_data["version"]["link"], init_data["version"]["name"], init_data["version"]["zip"])
            loading_screen.next_process("updating...", 100)
            loading_screen.root.destroy()
            try:
                os.startfile(init_data["version"]["name"])
            except:
                pass
            print("[init] quiting...")
            sys.exit()
    
    loading_screen.next_process("updating xpath file...", 80)
    #Mise à jour du fichier xpath
    try:
        with open("file/xpath.json", "w", encoding="utf-8") as f:
            json.dump(init_data["xpath"], f)
    except Exception as e:
        #En cas d'échec chargent les données xpath dans save Json a la place
        print(e)
        print("[init] failed updating xpath.json")
        loading_screen.next_process("failed to update xpath, using re writting data...", 90)
        with open("file/xpath.json", "w", encoding="utf-8") as f:
            with open("file/save.json", "r", encoding="utf-8") as f2:
                save =  json.loads( f2.read() )
            
            json.dump(save["xpath"], f)
    
    loading_screen.next_process("Done", 100)#affichage du chargement
    sleep(0.5)
    loading_screen.root.destroy()

    #affichage de la pop-up si elle est dans les données d'init
    if init_data.get("pop_up"):
        with open("file/buffer.json", "w", encoding="utf-8") as f: #buffering des données json de la pop_up
            json.dump(init_data["pop_up"]["widget"], f)
        
        root = tkgen.gengui.TkJson("file/buffer.json", title=init_data["pop_up"]["title"]) #génération de la pop_up via le json du fichier buffer
        root.geometry(init_data["pop_up"]["size"])
        root.resizable(False, False)
        root.iconbitmap("asset/VoltaireTaMere_icon[ICO].ico")
        root.configure(bg=init_data["pop_up"]["BG"])

        if init_data["pop_up"].get("link"):
            root.button('open_link', lambda: [webbrowser.open_new(init_data["pop_up"]["link"]), root.destroy()])
        if init_data["pop_up"].get("close"):
            root.button(init_data["pop_up"]["close"], root.destroy)
        
        root.mainloop()

    #verrouillage si maintenance
    if init_data.get("lock") == True: 
        sys.exit()
    

def auto_login(driver):
    """
    ############## description ##############\n
    Exécute la connexion automatique au projet Voltaire.

    ######### parametre(s) et resultat(s) #########\n
    :param driver: [class selenium Chrom driver] Driver de la fenêtre Chrome.
    :return: None
    """
    
    #Récupération des informations de connexion
    with open("./file/login.json", "r", encoding="utf-8") as f:
        login_json = json.loads(f.read())
    
    driver.get(login_json["link"])

    if login_json["auto_login"]:
        with open("./file/xpath.json", "r", encoding="utf-8") as f:
            xpath = json.loads(f.read())

        try:
            #remplit les informations de connexion sur le projet Voltaire
            driver.find_element_by_xpath(xpath["mail"]).send_keys(login_json["mail"])
            driver.find_element_by_xpath(xpath["mdp"]).send_keys(login_json["mdp"])
            driver.find_element_by_xpath(xpath["connect_button"]).click()
        except Exception as e:
            print(e)
            pass