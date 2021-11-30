#################################################################################################################################                                                                                                                           
#                                              Fichier contenant le GUI                                                         #
#################################################################################################################################                                                                                                                           

from tkinter import Entry, StringVar, IntVar, Tk, PhotoImage, Button, Text, Label, Scrollbar
import json
from data import DATA, extract_str_reponses_from_driver
from init import auto_login
from routine import auto_mode_routine, manuel_mode_routine
from threading import Thread
from time import sleep
import os
import webbrowser

from vr_file_prcs import vr_file_root
    
class VTM_gui:
    """
    ############## description ##############\n
    Classe qui contient les différents GUI (Login et Main) et rassemble les données générées et requises par les scripts

    ######### parametre(s) et resultat(s) #########\n
    :param driver: [class selenium Chrom driver] Driver de la fenêtre Chrome.
    """
    ###################################################################################################
    #                                        Constructeur                                             #
    ###################################################################################################
    def __init__(self, driver):

        #tkinter window basic set-up
        self.root = Tk()
        self.root.title("S1G2")
        self.root.resizable(False, False)
        self.root.iconbitmap("asset/VoltaireTaMere_icon[ICO].ico")
        self.root.configure(bg='#202020')
        
        #driver
        self.driver = driver

        #contient les données extraitent par les algorithme
        self.data_base = None

        #variable lier au robot
        self.bot_state = False

        ###################################################################################################
        #                                       Login window                                              #
        ###################################################################################################

        self.Login_fond_image = PhotoImage(file= "asset/Login_Menu.png")
        self.btn_connect_idt_image = PhotoImage(file= "asset/Connect_idt_boutton.png")
        self.btn_connect_link_image = PhotoImage(file= "asset/Connect_link_boutton.png")
        self.btn_no_connect_image = PhotoImage(file= "asset/No_connect_boutton.png")
        self.btn_enregistrer_image = PhotoImage(file= "asset/Enregistrer_boutton.png")
        self.text_login_image = PhotoImage(file= "asset/text_login.png")

        #tkinter variables login window
        self.user_mail = StringVar()
        self.user_mdp = StringVar()
        self.user_link = StringVar()

        #initialise les variables Tkinter contenant les informations de connexion
        with  open("./file/login.json", "r", encoding="utf-8") as f:    
            json_data = json.loads(f.read())
            self.user_mail.set(json_data["mail"])
            self.user_mdp.set(json_data["mdp"])
            self.user_link.set(json_data["link"])

        self.Login_fond = Label(self.root, image=self.Login_fond_image)

        #text
        self.text_login = Label(self.root, image=self.text_login_image, bg="#202020")

        #retour à l'écran de choix du type de connexion
        self.btn_go_back_select_connect_mode = Button(self.root,
            text="< retour",
            bd=0,
            highlightthickness=0,
            activebackground="#282828",
            command=lambda: [self.unload_connect_with_login(), self.unload_connect_with_link(), self.load_login_window()],
            bg="#282828",
            fg="#ffffff",
            font=('Helvetica', '10'))

        #désactive la connexion automatique
        self.no_login = Button(self.root,
            image=self.btn_no_connect_image,
            height=38,
            width=306,
            command=lambda: [self.save_json_login("https://www.projet-voltaire.fr/voltaire/com.woonoz.gwt.woonoz.Voltaire/Voltaire.html?returnUrl=www.projet-voltaire.fr/choix-parcours/&applicationCode=pv",
                            0, "e-mail/identifiant", "Mot de passe"), self.unload_login_window(), self.load_main_gui_window()],
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))

        ############################# login connexion widget #############################

        #connexion au projet Voltaire via des identifiants (classique)
        self.btn_connect_with_login = Button(self.root,
            image=self.btn_connect_idt_image,
            height=38,
            width=306,
            command=self.load_connect_with_login,
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))
        
        #champs d'entrer du mail
        self.user_mail_input = Entry(self.root, 
            textvariable=self.user_mail,
            width=28,
            bg="#282828",
            fg="#ffffff",
            bd=0,
            font=('Helvetica', '15'))
        
        #champs denter du mot de passe
        self.user_mdp_input = Entry(self.root, 
            textvariable=self.user_mdp,
            width=28,
            bg="#282828",
            fg="#ffffff",
            bd=0,
            font=('Helvetica', '15'))
        
        ############################# link connexion widget #############################

        #connexion au projet Voltaire via un lien
        self.btn_connect_with_link = Button(self.root, 
            image=self.btn_connect_link_image,
            height=38,
            width=306,
            command=self.load_connect_with_link,
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))

        #champs d'entrer du lien de connexion
        self.user_link_input = Entry(self.root, 
            textvariable=self.user_link,
            width=50,
            bg="#282828",
            fg="#ffffff",
            bd=0,
            font=('Helvetica', '10'))

        ################################# save json data #################################

        #bouton d'enregistrement des données de connexion
        self.btn_save_json = Button(self.root,
            image=self.btn_enregistrer_image,
            height=38,
            width=197,
            command=None,
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))

        ###################################################################################################
        #                                 VoltaireTaMere window                                           #
        ###################################################################################################

        self.VoltaireTaMere_fond_image = PhotoImage(file= "asset/VoltaireTaMere_Menu.png")
        self.Auto_on_image = PhotoImage(file= "asset/Auto_on_boutton.png")
        self.Auto_off_image = PhotoImage(file= "asset/Auto_off_boutton.png")
        self.Manuel_image = PhotoImage(file= "asset/Manuel_boutton.png")

        self.accuracy = IntVar()
        self.time_to_wait = IntVar()

        #initialise les variables Tkinter contenant les options
        with  open("./file/options.json", "r", encoding="utf-8") as f:    
            options = json.loads(f.read())
            self.accuracy.set(options.get("accuracy"))
            self.time_to_wait.set(options.get("time"))

        self.VoltaireTaMere_fond = Label(self.root, image=self.VoltaireTaMere_fond_image)

        #démarre la routine Automatique
        self.btn_auto_mode = Button(self.root,
            image=self.Auto_off_image,
            height=42,
            width=159,
            command=lambda: [self.set_data(), self.switch_auto_routine()],
            bg="#282828",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#282828",
            font=('Helvetica', '10'))
            
        #démarre la routine Manuel
        self.btn_manual_mode = Button(self.root,
            image=self.Manuel_image,
            height=42,
            width=159,
            command=lambda: [self.set_data(), Thread(target=self.MANUAL_ROUTINE).start()],
            bg="#282828",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#282828",
            font=('Helvetica', '10'))


        #entrée pour changer la précision du robot
        self.entry_accuracy = Entry(self.root, 
            textvariable=self.accuracy,
            width=10,
            bg="#282828",
            fg="#ffffff",
            bd=0,
            font=('Helvetica', '10'))
        
        #entrée pour changer le temps d'attente du robot
        self.entry_time = Entry(self.root, 
            textvariable=self.time_to_wait,
            width=10,
            bg="#282828",
            fg="#ffffff",
            bd=0,
            font=('Helvetica', '10'))

        #zone d'affichage des logs sur l'interface graphique
        self.text_on_screen = Text(self.root,
                        undo = True,
                        height = 11,
                        width=76,
                        bg="#282828",
                        fg="#ffffff",
                        bd=0,
                        font=('Helvetica', '10'))

        self.text_on_screen.tag_config("green",foreground = "#a2d417")
        self.text_on_screen.tag_config("red",foreground = "#ff4040")
        self.text_on_screen.tag_config("yellow", foreground = "#f5ff40")
        self.text_on_screen.tag_config("cyan", foreground = "#00ffff")
        self.text_on_screen.tag_config("magenta", foreground = "#ff00ff")
        self.text_on_screen.tag_config("white", foreground = "#ffffff")

        ###################################################################################################
        #                                       Aide window                                               #
        ###################################################################################################
        self.Aide_fond_image = PhotoImage(file="asset/Aide_Menu.png")
        self.btn_change_connexion_image = PhotoImage(file="asset/Change_connexion_boutton.png")
        self.btn_notice_image = PhotoImage(file="asset/Ouvrir_notice_boutton.png")
        self.btn_FAQ_image = PhotoImage(file="asset/Lien_FAQ_boutton.png")
        self.btn_vr_file_image = PhotoImage(file="asset/vr_file_boutton.png")

        self.Aide_fond = Label(self.root, image=self.Aide_fond_image)

        #Boutton de changement de paramètre de connexion
        self.btn_change_connexion = Button(self.root,
            image=self.btn_change_connexion_image,
            height=41,
            width=376,
            command= lambda: [ self.deconnect(), self.unload_aide_window(), self.load_login_window() ],
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))
        
        #boutton qui ouvre la notice
        self.btn_notice = Button(self.root,
            image=self.btn_notice_image,
            command= lambda: os.startfile("file\\Notice.pdf"),
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))

        #boutton qui ouvre la FAQ
        self.btn_FAQ = Button(self.root,
            image=self.btn_FAQ_image,
            height=41,
            width=376,
            command= lambda: webbrowser.open_new("https://sites.google.com/view/voltairetamere/faq"),
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))
        
        #boutton qui lance la vérification des fichiers
        self.btn_vr_file = Button(self.root,
            image=self.btn_vr_file_image,
            height=41,
            width=376,
            command= lambda: vr_file_root(self.root).vr_file(),
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))

        

        #boutton qui ouvre le site
        self.btn_site = Button(self.root,
            image=self.btn_site_image,
            height=38,
            width=241,
            command= lambda: webbrowser.open_new("https://sites.google.com/view/voltairetamere/voltairetamere"),
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))

        ###################################################################################################
        #                              VoltaireTaMere top navigation rod                                  #
        ###################################################################################################
        self.VoltaireTaMere_select_image = PhotoImage(file= "asset/VoltaireTaMere_select_boutton.png")
        self.VoltaireTaMere_unselect_image = PhotoImage(file= "asset/VoltaireTaMere_unselect_boutton.png")
        self.Aide_select_image = PhotoImage(file= "asset/Aide_select_boutton.png")
        self.Aide_unselect_image = PhotoImage(file= "asset/Aide_unselect_boutton.png")
        self.Contact_select_image = PhotoImage(file= "asset/Contact_select_boutton.png")
        self.Contact_unselect_image = PhotoImage(file= "asset/Contact_unselect_boutton.png")

        #Boutton qui affiche la fenêtre VoltaireTaMere
        self.btn_go_to_VoltaireTaMere = Button(self.root,
            image= self.VoltaireTaMere_select_image,
            height=25,
            width=129,
            command= lambda: [self.unload_aide_window(), self.unload_contact_window(), self.load_main_gui_window()],
            bg="#202020",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            activebackground="#202020",
            font=('Helvetica', '10'))


    ###################################################################################################
    #                                       Login fonction                                            #
    ###################################################################################################

    def load_login_window(self):
        """
        ############## description ##############\n
        Charge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.root.geometry('400x500')
        self.Login_fond.pack()
        self.text_login.place(x=41, y=229)
        self.btn_connect_with_login.place(x=47, y=267)
        self.btn_connect_with_link.place(x=47, y=345)
        self.no_login.place(x=47, y=423)

    def unload_login_window(self):
        """
        ############## description ##############\n
        Decharge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.Login_fond.pack_forget()
        self.text_login.place_forget()
        self.btn_connect_with_login.place_forget()
        self.btn_connect_with_link.place_forget()
        self.no_login.place_forget()
    
    def load_connect_with_login(self):
        """
        ############## description ##############\n
        Charge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.unload_login_window()
        self.Login_fond.pack()
        self.btn_save_json["command"] = lambda: [self.save_json_login("https://www.projet-voltaire.fr/voltaire/com.woonoz.gwt.woonoz.Voltaire/Voltaire.html?returnUrl=www.projet-voltaire.fr/choix-parcours/&applicationCode=pv",
                                        1, self.user_mail.get(), self.user_mdp.get()), self.unload_connect_with_login(), self.load_main_gui_window()]
        self.user_mail_input.place(x=47, y=250)
        self.user_mdp_input.place(x=47, y=310)
        self.btn_save_json.place(x=103, y=383)
        self.btn_go_back_select_connect_mode.place(x=10, y=10)
    
    def unload_connect_with_login(self):
        """
        ############## description ##############\n
        Decharge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.Login_fond.pack_forget()
        self.user_mail_input.place_forget()
        self.user_mdp_input.place_forget()
        self.btn_save_json.place_forget()
        self.btn_go_back_select_connect_mode.place_forget()
    
    def load_connect_with_link(self):
        """
        ############## description ##############\n
        Charge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.unload_login_window()
        self.Login_fond.pack()
        self.btn_save_json["command"] = lambda: [self.save_json_login(self.user_link.get(), 0, None, None), self.unload_connect_with_link(), self.load_main_gui_window()]
        self.user_link_input.place(x=22, y=240)
        self.btn_save_json.place(x=103, y=300)
        self.btn_go_back_select_connect_mode.place(x=10, y=10)
    
    def unload_connect_with_link(self):
        """
        ############## description ##############\n
        Decharge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.Login_fond.pack_forget()
        self.user_link_input.place_forget()
        self.btn_save_json.place_forget()
        self.btn_go_back_select_connect_mode.place_forget()

    def save_json_login(self, link, auto_login_value, mail, mdp):
        """
        ############## description ##############\n
        Enregistre les données entrer par l'utilisateur.

        ######### parametre(s) et resultat(s) #########\n
        :param link: [str] lien utilisé pour la connexion.
        :param auto_login_value: [str] vrai si l'auto-login est activé.
        :param mail: [str] identifiant de l'utilisateur.
        :param mdp: [str] mot de passe de l'utilisateur.
        :return: None
        """
        f_login = open("./file/login.json", "r", encoding="utf-8")
        json_data = json.loads(f_login.read())
        f_login.close()
        json_data["link"] = link
        json_data["auto_login"] = auto_login_value
        json_data["mail"] = mail
        json_data["mdp"] = mdp
        json_data["is_defined"] = 1
        f_login = open("./file/login.json", "w", encoding="utf-8")
        json.dump(json_data, f_login)
        f_login.close()
        auto_login(self.driver) #reconnexion

    ###################################################################################################
    #                                  VoltaireTaMere fonction                                        #
    ###################################################################################################
    
    def load_main_gui_window(self):
        """
        ############## description ##############\n
        Charge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.root.geometry('600x490')
        self.VoltaireTaMere_fond.pack()
        self.btn_go_to_VoltaireTaMere["height"] = 25
        self.btn_go_to_VoltaireTaMere["image"] = self.VoltaireTaMere_select_image
        self.btn_go_to_VoltaireTaMere.place(x=27, y=20)
        self.btn_go_to_Aide["height"] = 15
        self.btn_go_to_Aide["image"] =  self.Aide_unselect_image
        self.btn_go_to_Aide.place(x=174, y=20)
        self.btn_go_to_Contact["height"] = 14
        self.btn_go_to_Contact["image"] = self.Contact_unselect_image
        self.btn_go_to_Contact.place(x=232, y=21)
        self.btn_auto_mode.place(x=26, y=99)
        self.btn_manual_mode.place(x=26, y=144)
        self.entry_accuracy.place(x=381,y=110)
        self.entry_time.place(x=381,y=160)
        self.text_on_screen.place(x=29, y=277)
    
    def unload_main_gui_window(self):
        """
        ############## description ##############\n
        Decharge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.VoltaireTaMere_fond.pack_forget()
        self.btn_go_to_VoltaireTaMere.place_forget()
        self.btn_go_to_Aide.place_forget()
        self.btn_go_to_Contact.place_forget()
        self.btn_auto_mode.place_forget()
        self.btn_manual_mode.place_forget()
        self.entry_accuracy.place_forget()
        self.entry_time.place_forget()
        self.text_on_screen.place_forget()

    def set_data(self):
        """
        ############## description ##############\n
        Initialise les variables avant le lancement d'une routine. Update data_base uniquement si de nouvelles données sont chargées.
        """
        print("\n")
        brut_data= extract_str_reponses_from_driver(self.driver) #recuperation des données "brute" installer par le driver
        if brut_data != "":
            new_data_base = DATA(brut_data)  #construit la nouvelle base de données
            if new_data_base.extracted_data != []: #Mets à jour uniquement si de données ont été chargées
                print("[set_data] new DATA set\n")
                self.data_base = new_data_base
            else:
                print("[set_data] No new DATA\n")
        
        #Mets à jours tous les valeurs des options dans les fichiers
        with  open("./file/options.json", "r", encoding="utf-8") as f: 
            options = json.loads(f.read())
        
        if self.accuracy.get() < 0:
            self.accuracy.set(0)
        if self.accuracy.get() >100:
            self.accuracy.set(100)
        
        if self.time_to_wait.get() < 1:
            self.time_to_wait.set(1)

        options["accuracy"] = self.accuracy.get()
        options["time"] = self.time_to_wait.get()

        with  open("./file/options.json", "w", encoding="utf-8") as f:    #sauvegarder les options
            json.dump(options, f)
    
    def switch_auto_routine(self):
        """
        ############## description ##############\n
        S'occupe d'être un interrupteur on/off
        
        ON: Lance la routine automatique sur un second thread
        """
        if self.bot_state:
            self.bot_state = False
            self.btn_auto_mode["image"] = self.Auto_off_image
        else:
            self.bot_state = True
            self.btn_auto_mode["image"] = self.Auto_on_image
            Thread(target=self.AUTO_ROUTINE).start()

        print("[switch_auto_routine] bot set as", self.bot_state)

    def AUTO_ROUTINE(self):
        """
        ############## description ##############\n
        Routine du robot, tourne en boucle tant que bot_state == True
        """
        self.driver.implicitly_wait(0)
        with  open("./file/options.json", "r", encoding="utf-8") as f:    #recupere les options
            options = json.loads(f.read())

        print("[AUTO_ROUTINE] started with accuracy=",options.get("accuracy"),", and time=", options.get("time"))

        #tant que le bot est en fonctionnement
        while self.bot_state:
            self.text_on_screen.delete(1.0,"end")
            self.text_on_screen.insert("end","Localisation de l'erreur en cours...\n","green")

            try:
                result = auto_mode_routine(self.data_base, self.driver, options.get("accuracy")) #Réponds à une question
            except Exception as e:
                #Erreur non prévue
                print("################# EXCEPTION RAISE #################")
                print(e)
                print("###################################################")
                result = -1

            if result == -1: #signale une erreur
                print("[AUTO_ROUTINE] ^^^ crash happend ^^^\n")
                self.text_on_screen.delete(1.0,"end")
                self.text_on_screen.insert("end","Oups quelque chose est arrivé.\n","red")
                self.switch_auto_routine()
                self.driver.implicitly_wait(1)
                return None
            elif result == -2: #souvent associer à un niveau terminé
                self.switch_auto_routine()
                self.driver.implicitly_wait(1)
                break
            
            self.text_on_screen.insert("end","Clique fait !!\nEn attente...\n","green")

            i = 0
            #enchaine des sleep(1) pour s'arrêter au plus vite si l'utilisateur désactive le robot
            while i < options["time"] and self.bot_state:
                self.text_on_screen.edit_separator()
                self.text_on_screen.insert("end","temps restant: "+str(options["time"]-i),"green")
                sleep(1)
                i += 1
                self.text_on_screen.edit_undo()
        
        self.text_on_screen.delete(1.0,"end")
        self.text_on_screen.insert("end","I am a bot, and this action was performed automatically.\n","green")
        self.driver.implicitly_wait(1)

    def MANUAL_ROUTINE(self):
        """
        ############## description ##############\n
        Routine Manuel donne une réponse ponctuelle, lorsque l'on appuie sur le bouton.
        """
        self.driver.implicitly_wait(0)
        self.text_on_screen.delete(1.0,"end")
        self.text_on_screen.insert("end","Localisation de l'erreur en cours...\n","green")
        result = manuel_mode_routine(self.data_base, self.driver) #Récupère la réponse à une question
        if result == -1:
            print("[ROUTINE_BOT] crash happend or working terminated\n")
            self.text_on_screen.delete(1.0,"end")
            self.text_on_screen.insert("end","Oups quelque chose est arrivé.\n","red")
        elif result == -2:
            self.text_on_screen.insert("end","Ya rien à faire ici.\n","green")
        else:
            self.text_on_screen.insert("end",result+"\n","green")
        self.driver.implicitly_wait(1)

    ###################################################################################################
    #                                     Aide fonction                                               #
    ###################################################################################################

    def load_aide_window(self):
        """
        ############## description ##############\n
        Charge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.Aide_fond.pack()
        self.btn_go_to_VoltaireTaMere["height"] = 15
        self.btn_go_to_VoltaireTaMere["image"] = self.VoltaireTaMere_unselect_image
        self.btn_go_to_VoltaireTaMere.place(x=27, y=20)
        self.btn_go_to_Aide["height"] = 25
        self.btn_go_to_Aide["image"] =  self.Aide_select_image
        self.btn_go_to_Aide.place(x=174, y=20)
        self.btn_go_to_Contact["height"] = 14
        self.btn_go_to_Contact["image"] = self.Contact_unselect_image
        self.btn_go_to_Contact.place(x=232, y=21)
        self.btn_change_connexion.place(x=112, y=87)
        self.btn_notice.place(x=112, y=170)
        self.btn_FAQ.place(x=112, y=253)
        self.btn_vr_file.place(x=112, y=336)
    
    def unload_aide_window(self):
        """
        ############## description ##############\n
        Decharge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.Aide_fond.pack_forget()
        self.btn_go_to_VoltaireTaMere.place_forget()
        self.btn_go_to_Aide.place_forget()
        self.btn_go_to_Contact.place_forget()
        self.btn_change_connexion.place_forget()
        self.btn_notice.place_forget()
        self.btn_FAQ.place_forget()
        self.btn_vr_file.place_forget()

    def deconnect(self):
        """
        ############## description ##############\n
        Clique sur le boutton "deconnexion" si il peut. ça aussi c'est tres con comme fonction.
        """
        with open("./file/xpath.json", "r", encoding="utf-8") as f:
            xpath = json.loads(f.read())
        try:
            self.driver.find_element_by_xpath(xpath["deconnect"]).click()
        except:
            pass
    
    ###################################################################################################
    #                                    Contact fonction                                             #
    ###################################################################################################

    def load_contact_window(self):
        """
        ############## description ##############\n
        Charge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.Contact_fond.pack()
        self.btn_go_to_VoltaireTaMere["height"] = 15
        self.btn_go_to_VoltaireTaMere["image"] = self.VoltaireTaMere_unselect_image
        self.btn_go_to_VoltaireTaMere.place(x=27, y=20)
        self.btn_go_to_Aide["height"] = 15
        self.btn_go_to_Aide["image"] =  self.Aide_unselect_image
        self.btn_go_to_Aide.place(x=174, y=20)
        self.btn_go_to_Contact["height"] = 24
        self.btn_go_to_Contact["image"] = self.Contact_select_image
        self.btn_go_to_Contact.place(x=232, y=21)
        self.btn_discord.place(x=148, y=147)
        self.btn_paypal.place(x=214, y=252)
        self.btn_site.place(x=180, y=361)
    
    def unload_contact_window(self):
        """
        ############## description ##############\n
        Decharge et configure des widgets. Voila. C'est tout. La fonction est tellement conne que je suis pas sur que ya vrm besoin de commentaire.
        """
        self.Contact_fond.pack_forget()
        self.btn_go_to_VoltaireTaMere.place_forget()
        self.btn_go_to_Aide.place_forget()
        self.btn_go_to_Contact.place_forget()
        self.btn_discord.place_forget()
        self.btn_paypal.place_forget()
        self.btn_site.place_forget()