#################################################################################################################################                                                                                                                           
#                            Fichier de récupération et extraction des données de module                                        #
#################################################################################################################################
import brotli
import json
from auto_learning import get_data_in_memory

class DATA:
    """
    ############## description ##############\n
    Classe regroupant toute les données pour la detetction d'erreur.

    ######### parametre(s) et resultat(s) #########\n
    :param str_data_base: [str] Contenu des requêtes (données brutes).
    """

    def __init__(self, str_data_base):
        #données d'un niveau classique

        self.extracted_data = extract_data(str_data_base) #sert de verification a l'exctraction de données
        self.data_level = self.extracted_data + get_data_in_memory()

        #données du niveau verbes pronominaux I
        with open("./file/verb_pron_II.json", "r", encoding="utf-8") as f:
            dict_of_json =json.loads(f.read())
        self.data_verbe_atnm = dict_of_json["atnm"]
        self.data_verbe_ess = dict_of_json["ess"]
        self.data_verbe_acc = dict_of_json["acc"]
        self.data_verbe_pass = dict_of_json["pass"]
        self.data_verbe_prnm = dict_of_json["prnm"]

def extract_str_reponses_from_driver(driver):
    """
    ############## description ##############\n
    Récupère le contenu des requêtes XHR et les converties en string avant de les supprimer.

    ######### parametre(s) et resultat(s) #########\n
    :param driver: [class selenium Chrom driver] Driver de la fenêtre Chrome.
    :return: [str] Contenu des requêtes à la chaine.
    """

    str_data_base = ""
    for request in driver.requests:  
        print("[extract_str_reponses_from_driver] ", request.url, "loaded")
        try:
            str_data_base += brotli.decompress(request.response._body).decode("utf-8", "replace") #decryptage des donnée
        except:
            pass
    
    if str_data_base == "":
        print("[WARNING] [extract_str_reponses_from_driver] no data collected [WARNING]")
    else:
        print("[extract_str_reponses_from_driver] data collected")
    del driver.requests
    return str_data_base


def extract_data(str_data_base):
    """
    ############## description ##############\n
    Extrait les phrases qui donne des informations sur les réponses aux questions du projet Voltaire et les formates.

    ######### parametre(s) et resultat(s) #########\n
    :param str_data_base: [str] Contenu des requêtes (données brutes).
    :return: [list] Liste avec toutes les phrases extraite et formatée des données brutes.
    """
    str_data_base = str_data_base[str_data_base.index("[\"java.util.ArrayList"):].replace("\\x3Cbr/\\x3E","\",\"") #suppresions de la merde au debut
    data_from_str = []       #liste qui stocke les phrases avec une correction
    i = 0                    #itérateur de la chaine
    extrt = " "              #buffer
        
    while extrt != "":
        extrt = str_data_base[ str_data_base.find("\"",i) : str_data_base.find("\"", i+str_data_base.find("\"")+1) ] #extrait une phrase 
        i += len(extrt)
        
        if "\\x3C" in extrt:      #si elle contient la balise de correction on la stocke et la traite
            data_from_str += [extrt.replace("\"","")
                                .replace("\\x3CB\\x3E", "<")
                                .replace("\\x3C/B\\x3E", ">")
                                .replace("\\x27","'")
                                .replace("\\xA0"," ")
                                .replace("\\x26#x2011;","-")
                                .replace("‑","-")
                                .replace("\\x3Cspan class\\x3Dsmallcaps\\x3E","")
                                .replace("\\x3C!-- smallcaps end --\\x3E\\x3C/span\\x3E","")
                                .replace("\\x3CSUP\\x3E","")
                                .replace("\\x3C/SUP\\x3E","")
                                .replace("a) ","")
                                .replace("b) ","")
                                .replace("\\x3CI\\x3E","")
                                .replace("\\x3C/I\\x3E","")
                                .replace("\\x3Cbr/\\x3E","")
                                .replace("\\x26nbsp;"," ")
                                .replace("°", "o ")] 

    if data_from_str == []:
        print("[WARNING] extract_data_from_str: no data extracted")
    else:
        print("extract_data_from_str: data extracted")
        print(data_from_str)

    return data_from_str