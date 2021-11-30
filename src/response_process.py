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
#                                  Fichier contenant les algorithmes de détection de faute                                      #
#################################################################################################################################

import difflib
from auto_learning import get_response_of_list_in_memory, get_data_in_memory

def locate_err_in_sentence(sentence, match_of_sentence): #aka "ImGonnaFuckYourMomVoltaire"
    """
    ############## description ##############\n
    Compare la phrase et un match, si à la fin de la comparaison le seul mot qui reste dans le match sont les mots entre "<>" 
    alors renvoie le mot considéré comme l'erreur et la liste dans laquelle il a été sélectionné.

    ######### parametre(s) et resultat(s) #########\n
    :param sentence: [str] Phrase affichée à l'écran.
    :param match_of_sentence: [str] le/un match de la phrase.
    :return: [tuple(str, list)] Erreur de la phrase et liste de laquelle il provient.
    """

    if match_of_sentence == "":
        return None, None
    ################### phase de traitement de la phrase et du match pour formater leurs écritures ###################
    sentence = sentence.replace(":", ": ").replace("‑","-").replace("-","- ").replace("'","' ").replace("(","( ").replace(")"," )").replace("."," .").replace(","," , ").split()
    match_of_sentence = match_of_sentence.replace(":", ": ").replace("‑","-").replace("-","- ").replace("'","' ").replace("(","( ").replace(")"," )").replace("."," .").replace(","," , ")
    match_of_sentence = match_of_sentence.replace("' >", "'>  ").split()

    ###################### phase de récuperation des mots corrigés dans le match (ceux encadrés par les balise "<" et ">") ######################
    mot_corriger = []
    save_word = False
    for x in range(0, len(match_of_sentence)):
        if "<" in match_of_sentence[x]: #ouvre la récupération des mots erreurs
            save_word = True
        
        if save_word and match_of_sentence[x] != "":
            mot_corriger += [match_of_sentence[x].replace("<","").replace(">","")]
        
        if ">" in match_of_sentence[x]: #ferme la récupération des mots erreurs
            save_word = False
        
        match_of_sentence[x] = match_of_sentence[x].replace("<","").replace(">","") #fini le formatage

    print("[locate_err_in_sentence] sentence = ", sentence, "\n                 match_of_sentence = ",match_of_sentence,"\n                 mot_corriger = ", mot_corriger)

    ######################## phase de trie seule les mots différents entre les phrases sont gardé ########################
    for i in range(0, len(match_of_sentence)):
        if match_of_sentence[i] in sentence:
            sentence[ sentence.index(match_of_sentence[i]) ] = ""
            match_of_sentence[i] = ""
    
    #suppresion des "" dans les listes
    sentence = [sentence[i] for i in range(0,len(sentence)) if sentence[i] != ""]
    match_of_sentence =  [match_of_sentence[i] for i in range(0,len(match_of_sentence)) if match_of_sentence[i] != ""]

    print("[locate_err_in_sentence] sentence = ", sentence, "\n                 match_of_sentence = ",match_of_sentence,"\n                 mot_corriger = ", mot_corriger)

    ####################### test des resultats avant recuperation de l'erreur #######################
    if sentence == []:
        print("[locate_err_in_sentence] reajustement de sentence à", mot_corriger)
        sentence = mot_corriger
    
    ######################## verifiaction ########################
    for i in range(0, len(match_of_sentence)):
        if match_of_sentence[i] not in mot_corriger:
            print("[locate_err_in_sentence] match incorrect")
            return None, None
    print("[locate_err_in_sentence] match correcte")
    
    ######################## traitement de la reponse final ########################
    error_in_sentence  = get_response_of_list_in_memory(sentence)
    error_in_sentence = error_in_sentence.replace("'","").replace("-","").replace("…","").replace("@","").replace("!", "").replace("?", "").replace(";","").replace(":","")
    if "." in error_in_sentence and error_in_sentence != ".":
        error_in_sentence.replace(".","")
    print("[locate_err_in_sentence] error_in_sentence =", error_in_sentence)
    return error_in_sentence, sentence


def locate_good_one(sentence, match_of_sentence, error_in_sentence):
    """
    ############## description ##############\n
    Renvoie la position du mot sur lequel on doit cliquer dans le cas ou le mot est présent en plusieurs exemplaires.

    exemple:

    :sentence = "je suis une phrase phrase exemple"
    :match_of_sentence = "je suis une phrase <phrase> exemple"
    :error_in_sentence = "phrase"

    la fonction va donc return 1. Dans le cas ou le match aurait été "je suis une phrase exemple" on aurait eu 0.

    ######### parametre(s) et resultat(s) #########\n
    :param sentence: [str] Phrase affichée à l'écran.
    :param match_of_sentence: [str] Le/un match de la phrase.
    :param error_in_sentence: [str] Erreur dans la phrase.
    :return: [int] Sa position dans la phrase.
    """
    #si il n'y a pas de match ca sert à rien de compter
    if match_of_sentence == None:
        return 0

    match_of_sentence = match_of_sentence.replace(":", ": ").replace("‑","-").replace("-","- ").replace("'","' ").replace("(","( ").replace(")"," )").replace("."," . ").replace(","," , ").replace(";", " ; ").split()
    if  sentence.count(error_in_sentence) > 1: #si le mot existe en plusieurs exemplaires
        i = 0
        j = 0
        #compte les occurrences jusqu'à tomber sur l'erreur
        while "<" not in match_of_sentence[i] and i < len(match_of_sentence):
            if match_of_sentence[i].replace("'","").replace("-","").replace("…","").replace("!", "") == error_in_sentence:
                j += 1
            i += 1
        return j
    else:
        return 0

#pronominal uniquement
def get_verbe_in_sentence(data_of_type, sentence):
    """
    ############## description ##############\n
    Parcours les verbes de la base de données jusqu'à en trouver un qui est dans la phrase.

    ######### parametre(s) et resultat(s) #########\n
    :param data_of_type: [list] Base de données utilisée.
    :param sentence: [str] Phrase affichée à l'écran.
    :return: [str] Verbe trouver dans la base de données.
    """
    i = 0
    for i in range(0, len(data_of_type)):
        if data_of_type[i] in sentence:
            print("[get_verbe_in_sentence] verbe found:"+data_of_type[i])
            return data_of_type[i]

    print("[get_verbe_in_sentence] None")
    return None


def get_error(type, DATA, consigne, sentence):
    """
    ############## description ##############\n
    Test tous les matchs pour une phrase affichée à l'écran et renvoie un dictionnaire avec tous les informations à la fin des tests.

    ######### parametre(s) et resultat(s) #########\n
    :param type: [str] Indique le type d'exercice d'où proviens la phrase ("point_on_error" ou "pronominal").
    :param DATA: [class DATA] classe qui regroupe tous les données charger.
    :param consigne: [str] Consigne affichér a l'écran (uniquement pour le type pronominal).
    :param sentence: [str] Phrase affichée à l'écran.
    :return: [dict] 
                    {"error": [str] erreur localisée
                    "list_from_error": [list] liste de la détection d'erreurs (point_on_error et catégorie "prnm" de pronominal uniquement)
                    "matche": [str] matche trouvé (point_on_error et catégorie "prnm" de pronominal uniquement)
                    "type": [str] type de verbe pronominal trouvé (pronominal uniquement) }
    """
    return_values = {"error": None, #erreur localiser
                    "list_from_error": None, #liste de la detetction d'erreur (point_on_error et categorie "prnm" de pronominal uniquement)
                    "matche": None, #matche trouver (point_on_error et categorie "prnm" de pronominal uniquement)
                    "type": None} #type de verbe pronominal trouver (pronominal uniquement)

    if type == "point_on_error":
        matches = difflib.get_close_matches(sentence, DATA.data_level + get_data_in_memory())
        print("[get_error] matches = ", matches)
        if matches != []:

            for i in range(0, len(matches)):
                if "<" in matches[i]:
                    return_values["error"], return_values["list_from_error"] = locate_err_in_sentence(sentence, matches[i])
                    return_values["matche"] = matches[i]

                    if return_values["error"] != None:
                        print("[get_error] matche found ERROR: "+ return_values["error"])
                        return return_values
                    
                #reinitialisation en cas d'echec
                return_values["error"] = None
                return_values["list_from_error"] = None
                return_values["matche"] = None


        print("[get_error] matche not found: NO ERROR")
        return return_values

    #c'est moche mais c'est simple à comprendre et ça marche
    elif type == "pronominal":
        sentence_split = sentence.replace("‑","-").replace("-","- ").replace(",","").replace(".","").replace("'","' ").split()
        if "essentiellement" in consigne:
            return_values["matche"] = sentence
            return_values["type"] = "ess"
            return_values["error"] = get_verbe_in_sentence(DATA.data_verbe_ess, sentence_split)
            return return_values
        elif "autonome" in consigne:
            return_values["matche"] = sentence
            return_values["type"] = "atnm"
            return_values["error"] = get_verbe_in_sentence(DATA.data_verbe_atnm, sentence_split)
            return return_values
        elif "passif" in consigne:
            return_values["matche"] = sentence
            return_values["type"] = "pass"
            return_values["error"] = get_verbe_in_sentence(DATA.data_verbe_pass, sentence_split)
            return return_values
        elif "accidentellement" in consigne:
            return_values["matche"] = sentence
            return_values["type"] = "acc"
            return_values["error"] = get_verbe_in_sentence(DATA.data_verbe_acc, sentence_split)
            return return_values
        else:
            matches = difflib.get_close_matches(sentence, DATA.data_verbe_prnm)
            print("[get_error] matches = ", matches)
            if matches != []:

                for i in range(0, len(matches)):
                    if "<" in matches[i]:
                        return_values["error"], return_values["list_from_error"] = locate_err_in_sentence(sentence, matches[i])
                        return_values["matche"] = matches[i]

                        if return_values["error"] != None:
                            print("[get_error] matche found ERROR: "+ return_values["error"])
                            return return_values
                        
                    #reinitialisation en cas d'echec
                    return_values["error"] = None
                    return_values["list_from_error"] = None
                    return_values["matche"] = None

            print("[get_error] matche not found: NO ERROR")
            return return_values
