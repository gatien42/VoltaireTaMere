#################################################################################################################################                                                                                                                           
#                                    Fichier contenant les fonctions d'auto-apprentissage                                       #
#################################################################################################################################
import json

def get_data_in_memory():
    """
    ############## description ##############\n
    Charge la liste json avec les phrases de la mémoire.

    ######### parametre(s) et resultat(s) #########\n
    :return: [list] Liste contenant les phrases enregistrées
    """
    with open("./file/match_memory.json", "r", encoding="utf-8") as f:
        data_in_memory = json.loads(f.read())
    
    return data_in_memory

def add_sentence_in_memory(type, sentence, error_in_sentence):
    """
    ############## description ##############\n
    Ajoute un match avec l'indication de l'erreur dans le fichier mémoire.

    Plus précisément insère "@" avant le mot qui est considéré comme la bonne réponse et enregistre le match.

    :exemple:\n
    "phrase de testz" avec pour erreur "testz" --> "phrase de <@testz>"

    ######### parametre(s) et resultat(s) #########\n
    :param type: [str] Indique le type d'exercice d'où proviens la phrase ("point_on_error" ou "pronominal").
    :param sentence: [str] Phrase affichée à l'écran.
    :param error_in_sentence: [str] Erreur dans la phrase.
    :return: None
    """
    match = sentence[ : sentence.index(error_in_sentence) ] + "<@" + error_in_sentence + ">" + sentence[ sentence.index(error_in_sentence)+len(error_in_sentence) :]
    if type == "point_on_error":
        #enregistrement
        with open("./file/match_memory.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        with open("./file/match_memory.json", "w", encoding="utf-8") as f:
            data += [match]
            json.dump(data, f)

    elif type == "pronominal":
        #traitement pour formalisation
        match = match.replace("‑","-").replace("-","- ").replace("'","' ").replace("(","( ").replace(")"," )").replace("."," . ").replace(","," , ").replace(";", " ; ").split()
        match = ' '.join(match)

        #enregistrement
        with open("./file/verb_pron_II.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        with open("./file/verb_pron_II.json", "w", encoding="utf-8") as f:
            
            #dans le cas ou le match est déjà enregistré, le supprime de la mémoire va l'envoyer dans une fonction pour le modifier avant d'enregistrer cette nouvelle version
            if match in data["prnm"]:
                data["prnm"].remove(match)
                print("[add_sentence_in_memory] match already in memory, correction...")
                match = correction_of_match(match, error_in_sentence)
                print("[add_sentence_in_memory] New match =", match)

            data["prnm"] += [match]
            json.dump(data, f)

def correction_of_match(match, err):
    """
    ############## description ##############\n
    Renvoie le match en décallant l'indication d'erreur au mot (err) suivant.

    Dans le cas des exercices où l'on doit trouver le bon pronom il arrive souvent 
    que le mot erreur se trouve en plusieurs exemplaires et que ça soit celui en 2,3... 
    position le bon. Or il est impossible de le savoir lors de la récupération de 
    l'erreur a l'écran, c'est pour ça qu'a chaque fois que cette fonction décaille au mot suivant.

    :exemple:\n
    Ici le robot s'est fier à sa mémoire et à cliquer sur le premier, malheureusement mauvaise réponse, 
    il va donc corriger la phrase de sa mémoire. l'erreur était "nous":\n
    "<@Nous> nous attaquerons au toit quand nous aurons fini les murs ." --> "Nous <@nous> attaquerons au toit quand nous aurons fini les murs .",

    ######### parametre(s) et resultat(s) #########\n
    :param match: [str] Match à modifier.
    :param err: [str] Erreur.
    :return: [str] Match modifié.
    """
    match = match.split()
    try:
        last_pos_err = match.index("<@"+err+">")
    except:
        last_pos_err = 0

    new_pos_err = match.index(err, last_pos_err)
    match[ new_pos_err ] = "<@"+err+">"
    if new_pos_err != match.index("<@"+err+">"):
        match[ match.index("<@"+err+">") ] = err
    
    return ' '.join(match)

def add_response_of_list_in_memory(type, list, response, consigne):
    """
    ############## description ##############\n
    Associe la vraie bonne réponse à une liste d'erreur rencontrer.

    ######### parametre(s) et resultat(s) #########\n
    :param type: [str] Indique le type d'exercice d'où proviens la phrase ("point_on_error" ou "pronominal").
    :param list: [list] Liste contenant le/les mot(s) restant après l'algorithme de détection d'erreurs.
    :param response: [str] Véritable bonne réponse.
    :param consigne: [str] Consigne affichér a l'écran (uniquement pour le type pronominal).
    :return: None
    """
    if type == "point_on_error":
        with open("./file/list_memory.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        with open("./file/list_memory.json", "w", encoding="utf-8") as f:
            data[str(list)] = response.split()[0]
            json.dump(data, f)

    elif type == "pronominal":
        with open("./file/verb_pron_II.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        with open("./file/verb_pron_II.json", "w", encoding="utf-8") as f:
            if "essentiellement" in consigne:
                data["ess"] += [response]
            elif "autonome" in consigne:
                data["atnm"] += [response]
            elif "passif" in consigne:
                data["pass"] += [response]
            elif "accidentellement" in consigne:
                data["acc"] += [response]
            json.dump(data, f)

def get_response_of_list_in_memory(list):
    """
    ############## description ##############\n
    Renvoie le mot qui sera considéré comme l'erreur de la phrase.

    La fonction vérifiera si la liste est enregistrée en mémoire. On a donc deux cas de figure:

    -La liste est en mémoire: le mot renvoyer sera donc celui qui a été sauvegarder (processus d'auto-correction).
    -La liste n'est pas en mémoire: le mot renvoyer sera le premier de la liste.

    ######### parametre(s) et resultat(s) #########\n
    :param list: [list] Liste contenant le/les mot(s) restant après l'algorithme de détection d'erreurs.
    :return: [str] Erreur de la phrase.
    """
    with open("./file/list_memory.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    response = data.get(str(list))
    if response != None:
        print("[get_response_of_list_in_memory] correction from memory done:", list[0],"->", response)
        return response
    else:
        return list[0]