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
#                                       Main script de VoltaireTaMere                                                           #
#################################################################################################################################                                                                                                                           

import json, sys, os
from datetime import datetime
from init import init, auto_login, set_driver, update_driver
from GUI import VTM_gui
from tkinter import *
from tkinter.ttk import Progressbar
from selenium.common.exceptions import SessionNotCreatedException
import requests

def center_root(root):
    """place la fenêtre au centre de l'écran"""
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    root.geometry("+%d+%d" % (x, y))
    
class loading_gui:
    """GUI du chargement"""
    def __init__(self):
        self.root = Tk()
        self.root.title("VoltaireTaMere")
        self.root.geometry("560x300")
        self.root.resizable(False, False)
        self.root.iconbitmap("asset/VoltaireTaMere_icon[ICO].ico")
        self.root.overrideredirect(True)
        self.root.configure(bg='#202020')
        center_root(self.root)
        self.root.lift()

        self.driver_buffer = None
        
        self.loading_fond_image = PhotoImage(file="asset/loading.png")
        Label(self.root, image=self.loading_fond_image).pack()

        
        self.process_bar = Progressbar(self.root, orient = HORIZONTAL,
                        length = 502, mode = 'determinate')
        self.process_bar.place(x=25, y=200)

        self.log = Text(self.root,
                        height=1,
                        width=50,
                        bg="#202020",
                        fg="#ffffff",
                        bd=0,
                        font=('Helvetica', '12'))
        self.log.place(x=25, y=250)

        self.stop = Button(self.root, 
                        text="X",
                        command=sys.exit,
                        bg="#202020",
                        fg="#ffffff",
                        bd=0,
                        font=('Berlin Sans FB', '12'))
        self.stop.place(x=535, y=0)

    def next_process(self, msg, value):
        self.process_bar["value"] = value
        self.log.delete(1.0,"end")
        self.log.insert("end",msg)
        self.root.update_idletasks()

def init_routine():
    """initialise les systèmes"""
    global driver #pas d'autre solution trouvée :/
    try:
        loading_screen.next_process("starting driver...", 10)
        driver = set_driver()
    except Exception as e:
        if SessionNotCreatedException:
            print("[init_routine] wrong version of chrome driver updating...")
            loading_screen.next_process("updating driver...", 20)
            update_driver()
            loading_screen.next_process("re-starting driver...", 30)
            driver = set_driver()
        else:
            sys.stderr.write(str(e))
            print("[init_routine] error while starting driver")
            loading_screen.log["fg"] = "red"
            loading_screen.next_process("ERREUR CRITIQUE: fermez le logiciel et contactez l'assistance.", 0)
            raise e
        
    loading_screen.next_process("driver DONE", 40)

    init(driver, loading_screen)

#transfere les logs dans un fichier
log_file = open("file/log.log", "w", encoding="utf-8")
err_file = open("file/crash_report.log", "a", encoding="utf-8")
sys.stdout = log_file
sys.stderr = err_file
date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
log_file.write(f"###################### SESSION [{date}] ######################\n")
err_file.write(f"\n###################### SESSION [{date}] ######################\n")

driver = None

#Fenêtre de chargement
loading_screen = loading_gui()
loading_screen.root.after(0, init_routine)
loading_screen.root.mainloop()

#Fenêtre principale
gui = VTM_gui(driver)

#login
with open("./file/login.json", "r", encoding="utf-8") as f:
    login = json.loads(f.read())

if login["is_defined"]: #si ce n'est pas le premier lancement
    auto_login(driver)
    gui.load_main_gui_window()
else: #si c'est le premier lancement
    with open("./file/version.json", "r", encoding="utf-8") as f:
        requests.get( json.loads(f.read())["link_to_count"] ) #compteur d'utilisatuer /!\ NE PAS ALLER SUR LE LIEN MERCI !!! /!\  sinon ça fausse le compteur
    os.startfile("file\\Notice.pdf")
    gui.load_login_window()
    
gui.root.mainloop()
try:
    driver.close()
except:
    pass

#fermeture des fichiers log et erreur
log_file.close()
err_file.close()