#  __     __            __    __                __                   ________          __       __                               
# |  \   |  \          |  \  |  \              |  \                 |        \        |  \     /  \                              
# | $$   | $$  ______  | $$ _| $$_     ______   \$$  ______    ______\$$$$$$$$______  | $$\   /  $$  ______    ______    ______  
# | $$   | $$ /      \ | $$|   $$ \   |      \ |  \ /      \  /      \ | $$  |      \ | $$$\ /  $$$ /      \  /      \  /      \ 
#  \$$\ /  $$|  $$$$$$\| $$ \$$$$$$    \$$$$$$\| $$|  $$$$$$\|  $$$$$$\| $$   \$$$$$$\| $$$$\  $$$$|  $$$$$$\|  $$$$$$\|  $$$$$$\
#   \$$\  $$ | $$  | $$| $$  | $$ __  /      $$| $$| $$   \$$| $$    $$| $$  /      $$| $$\$$ $$ $$| $$    $$| $$   \$$| $$    $$
#    \$$ $$  | $$__/ $$| $$  | $$|  \|  $$$$$$$| $$| $$      | $$$$$$$$| $$ |  $$$$$$$| $$ \$$$| $$| $$$$$$$$| $$      | $$$$$$$$
#     \$$$    \$$    $$| $$   \$$  $$ \$$    $$| $$| $$       \$$     \| $$  \$$    $$| $$  \$ | $$ \$$     \| $$       \$$     \
#      \$      \$$$$$$  \$$    \$$$$   \$$$$$$$ \$$ \$$        \$$$$$$$ \$$   \$$$$$$$ \$$      \$$  \$$$$$$$ \$$        \$$$$$$$

#################################################################################################################################                                                                                                                           
#                                Fichier contenant les routines automatiques et manuelles                                       #
#################################################################################################################################

import json
from random import randint
from auto_learning import add_sentence_in_memory, add_response_of_list_in_memory
from response_process import get_error, locate_good_one
from time import sleep

def test_Feature(Feature, driver):
    """
    ############## description ##############\n
    Test la presence du feature a l'écran.

    ######### parametre(s) et resultat(s) #########\n
    :param driver: [class selenium Chrom driver] Driver de la fenêtre Chrome.
    :param Feature: [str] Nom de classe html de la feature à tester.
    :return: [bool] 
    """
    try:
        driver.find_element_by_class_name(Feature)
        return True
    except:
        return False

def auto_mode_routine(DATA, driver, accuracy): #aka "ImAFuckingRobotDumbAss"
    """
    ############## description ##############\n
    Fonction qui va répondre automatiquement à une question afficher à l'écran.

    ######### parametre(s) et resultat(s) #########\n
    :param DATA: [class DATA] Classe qui regroupe tous les données charger.
    :param driver: [class selenium Chrom driver] Driver de la fenêtre Chrome.
    :param accuracy: [int] pourcentage de précision.
    :return: [int] code resultat, 0: RAS, -1: crash, -2: fin de niveau
    """

    print("\n[auto_mode_routine] ############# WORKING... #############")
    with open("./file/xpath.json", "r", encoding="utf-8") as f:
        xpath = json.loads(f.read())

    ############################################## INITIALISATION ##############################################
    #Désactive les fonctions audio
    print("[auto_mode_routine] test pour les fonctions audio...")
    if test_Feature("sentenceAudioReader", driver):
        print("[auto_mode_routine] audio disable")
        driver.find_element_by_xpath(xpath["audio_icon"]).click()
        driver.find_element_by_xpath(xpath["audio_close"]).click()

    #Vérifie si une pop-up est présente
    print("[auto_mode_routine] test pour une pop-up...")
    if test_Feature("popupContent", driver):
        try:
            driver.find_element_by_xpath(xpath["close_pop_up"]).click()
        except:
            sleep(1)
            if test_Feature("popupContent", driver):
                print("[auto_mode_routine] FAILED TO EXECUTE FEATURE IN")
                return -1
            else:
                return -2
    
    #identification du type de question
    print("[auto_mode_routine] identification de la question...")
    try:
        consigne = driver.find_element_by_xpath(xpath["consigne"]).text
        type_of_exercise = "pronominal"
    except:
        consigne = None
        type_of_exercise = "point_on_error"
    print("[auto_mode_routine] type =", type_of_exercise)
    
    #Récupération de la phrase a l'écran
    print("[auto_mode_routine] recuperation de la phrase...")
    try:
        sentence =  driver.find_element_by_xpath(xpath["sentence"]).text
        print("[auto_mode_routine] sentence =",sentence)
    except:
        print("[auto_mode_routine] FAILED TO EXECUTE NO SENTENCE")
        return -2   

    #Récupération de l'erreur
    print("[auto_mode_routine] identification de l'erreur...")
    error_information = get_error(type_of_exercise, DATA, consigne, sentence)

    ################################ phase d'auto-fail si demandé ################################

    if randint(1,100) > accuracy and type_of_exercise != "pronominal":
        if error_information["error"] != None: #si il y a une erreur clique sur "pas d'erreur"
            driver.find_elements_by_xpath(xpath["no_error"])[0].click()
            print("[auto_mode_routine] AUTO FAIL")
        else: #si n'il y a pas d'erreur clique sur le premier mot de phrase
            list_sentence = sentence.replace(":", ": ").replace("‑","-").replace("-","- ").replace("'","' ").replace("(","( ").replace(")"," )").replace("."," .").replace(","," , ").split()
            driver.find_elements_by_xpath("//span[.='"+ list_sentence[0].replace("‑","-").replace("-"," ").replace("'"," ") +"']")[0].click()
            print("[auto_mode_routine] AUTO FAIL")
            
        try:
            driver.find_elements_by_xpath(xpath["next"])[0].click()
        except:
            pass
        return 0

    ################################ Phase de clique sur l'erreur ou sur "aucune faute" ################################
    if error_information["error"] != None:
        #clique sur l'erreur
        try:
            driver.find_elements_by_xpath("//span[.='"+ error_information["error"]+"']")[ locate_good_one(sentence, error_information["matche"], error_information["error"]) ].click()
            print("[auto_mode_routine] EXECUTION CLICK DONE")
        except:
            try:
                driver.find_elements_by_xpath("//span[.='"+ error_information["error"]+"…"+"']")[ locate_good_one(sentence, error_information["matche"], error_information["error"]) ].click()
                print("[auto_mode_routine] EXECUTION CLICK DONE")
            except:
                print("[auto_mode_routine] FAILED TO TOUCHE ERROR")
                return -1
    else:
        try:
            driver.find_elements_by_xpath(xpath["no_error"])[0].click()
            print("[auto_mode_routine] EXECUTION CLICK DONE")
        except:
            try:
                #si échoue à toucher le bouton "il n'y a pas de faute" touche le premier mot de la phrase
                list_sentence = sentence.replace("‑","-").replace("-"," ").replace("'"," ").split()
                driver.find_elements_by_xpath("//span[.='"+ list_sentence[0] +"']")[0].click()
                print("[auto_mode_routine] FAILED TO TOUCHE NO ERROR")
                if type_of_exercise == "point_on_error":
                    return -1
            except Exception as e:
                print("####################################################")
                print(e)
                print("[auto_mode_routine] ^^^ FAILED EXCEPTION TOUCHE NO ERROR ^^^")
                return -1
    
    ################################ Phase de vérification de l'action et d'apprentissage si erreur ################################

    if driver.find_elements_by_xpath(xpath["wrong_answer_title"]) != []:
        print("[auto_mode_routine] failed, learning...")
        asnwer =driver.find_elements_by_xpath(xpath["answer_word"])[0].text
        print("[auto_mode_routine] asnwer =", asnwer)
        if error_information["matche"] == None or ("réfléchi" in consigne and "accidentellement" not in consigne): #dans le cas ou le l'algorithme a échoué à trouver un match l'apprend
            add_sentence_in_memory(type_of_exercise, sentence, asnwer)
        else: #dans le cas ou l'algorithme a échoué à correctement localiser l'erreur l'apprend
            add_response_of_list_in_memory(type_of_exercise, error_information["list_from_error"], asnwer, consigne)

    try:
        driver.find_elements_by_xpath(xpath["next"])[0].click()
    except:
        pass
    return 0


def manuel_mode_routine(DATA, driver):
    """
    ############## description ##############\n
    Donne la réponse à une question.

    ######### parametre(s) et resultat(s) #########\n
    :param DATA: [class DATA] Classe qui regroupe tous les données charger.
    :param driver: [class selenium Chrom driver] Driver de la fenêtre Chrome.
    :return: [str] Phrase qui indique l'erreur et sa position.
    """
    print("\n[manuel_mode_routine] ############# WORKING... #############")
    with open("./file/xpath.json", "r", encoding="utf-8") as f:
        xpath = json.loads(f.read())

    ############################################## INITIALISATION ##############################################
    #Désactive les fonctions audio
    print("[manuel_mode_routine] test pour les fonctions audio...")
    if test_Feature("sentenceAudioReader", driver):
        print("[manuel_mode_routine] audio disable")
        driver.find_element_by_xpath(xpath["audio_icon"]).click()
        driver.find_element_by_xpath(xpath["audio_close"]).click()

    #Vérifie si une pop-up est présente
    print("[manuel_mode_routine] test pour une pop up...")
    if test_Feature("popupContent", driver):
        print("[manuel_mode_routine] FAILED TO EXECUTE FEATURE IN")
        return -1
    
    #identification du type de question
    print("[manuel_mode_routine] identification de la question...")
    try:
        consigne = driver.find_element_by_xpath(xpath["consigne"]).text
        type_of_exercise = "pronominal"
    except:
        consigne = None
        type_of_exercise = "point_on_error"
    print("[manuel_mode_routine] type =", type_of_exercise)
    
    #Récupération de la phrase a l'écran
    print("[manuel_mode_routine] recuperation de la phrase...")
    try:
        sentence =  driver.find_element_by_xpath(xpath["sentence"]).text
        print("[manuel_mode_routine] sentence =",sentence)
    except:
        print("[manuel_mode_routine] FAILED TO EXECUTE NO SENTENCE")
        return -2   

    #Récupération de l'erreur
    print("[manuel_mode_routine] identification de l'erreur...")
    error_information = get_error(type_of_exercise, DATA, consigne, sentence)
    nmb = locate_good_one(sentence, error_information["matche"], error_information["error"])

    ############################################## RETURN ##############################################
    if error_information["error"] == None:
        return "Aucune erreur dans cette phrase"
    else:
        if nmb > 0:
            return "L'erreur dans la phrase est le "+str(nmb+1)+"eme \""+str(error_information["error"])+"\""
        else:
            return "L'erreur dans la phrase est \""+str(error_information["error"])+"\""