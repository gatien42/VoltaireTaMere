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
#                            Fichier des fonctions de vérification des fichiers internes                                        #
################################################################################################################################# 

import json
from tkinter import *
from tkinter.ttk import Progressbar

def center_root(root):
    """place la fenêtre au centre de l'écran"""
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    root.geometry("+%d+%d" % (x, y))
    
class vr_file_root:
    def __init__(self, parent):
        self.root = Toplevel(parent)
        self.root.title("vérification des fichiers...")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        self.root.iconbitmap("asset/VoltaireTaMere_icon[ICO].ico")
        self.root.configure(bg='#202020')
        center_root(self.root)
        self.root.lift()
        
        self.process_bar = Progressbar(self.root, orient = HORIZONTAL,
                        length = 250, mode = 'determinate')
        self.process_bar.place(x=25, y=25)

        self.log = Text(self.root,
                        height=1,
                        width=30,
                        bg="#202020",
                        fg="#ffffff",
                        bd=0,
                        font=('Helvetica', '10'))
        self.log.place(x=25, y=75)

        self.ok = Button(self.root,
                        text="Terminé",
                        command=self.root.destroy,
                        bg="#282828",
                        fg="#ffffff",
                        bd=0,
                        font=('Helvetica', '10'))

    def next_process(self, msg, value):
        self.process_bar["value"] += value
        self.log.delete(1.0,"end")
        self.log.insert("end",msg)
        self.root.update_idletasks()
    
    def end(self):
        self.ok.place(x=122.5, y=100)

    def vr_file(self):
        """parcours les fichiers Json internes et essaye de transformer en objet et d'accéder à leur contenu, en cas d'échec les réparent via save.json"""
        #ouvre save.json pour savoir quels fichiers vérifier
        with open("file/save.json", "r", encoding="utf-8") as f:
            save =  json.loads( f.read() )

        for x in save:
            try:
                #essaye d'accéder au données
                print(f"\n$$$$$$$$$$$$$$$ {x}.json $$$$$$$$$$$$$$$")
                self.next_process(f"récuperation des données de {x}.json...",5)#affichage barre de chargement
                #hcrage l'objet json
                with open("file/"+x+".json", "r", encoding="utf-8") as ftv:
                    json_ftv = json.loads(ftv.read())
                
                self.next_process(f"test des données de {x}.json...",5)
                #affiche sont contenu
                if type(json_ftv) == dict:
                    for y in json_ftv:
                        print(f"name:[{y}] value:[{json_ftv[y]}]")
                else:
                    print(f"value:[{json_ftv}]")
                
                self.next_process(f"{x}.json... vérifier",10)
            except Exception as e:
                #affiche l'erreur et répare le fichier a son état par défaut
                print("########################################")
                print(e)
                print("########################################")
                print(f"repairing {x}.json...")
                self.next_process(f"réparation de {x}.json...",5)
                with open("file/"+x+".json", "w", encoding="utf-8") as ftr:
                    json.dump(save[x],ftr)
                self.next_process(f"{x}.json... réparé",5)

        self.next_process(f"vérification des fichiers terminé",0)
        self.end()


