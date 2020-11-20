# coding: utf-8
from tkinter import *
import os
from tkinter import filedialog

class textEditor:
    def __init__(self, master, content):
        self.master = master
        self.content = content

#---------------------------------------------------------------------------------------------------
#CREATION DE LA FENETRE PRINCIPALE
#---------------------------------------------------------------------------------------------------

    #Créer la fenetre avec les dimensions et le titre attribué.   
    def create(self):
        self.master = Tk()
        self.master.title("Editeur de texte")
        self.master.geometry("700x400")
    
    #creer la zone de texte
    def add_Text(self):
        self.content = Text(self.master)
        self.content.pack(expand=True, fill='both')
     
    #genere la fenetre
    def generate(self):
        self.master.mainloop()

#---------------------------------------------------------------------------------------------------
#CREATION DU MENU
#---------------------------------------------------------------------------------------------------

    #Quitte le programme
    def quitter(self):
        self.master.quit()

    #Ouvrir
    def ouvrir(self):
        file = filedialog.askopenfilename(initialdir="/", title="Choisir le fichier", filetype=(("Text File", "*.txt"),("All Files", "*.*")))
        f = open(file, 'r')
        r = f.read()
        f.close()
        self.content.insert("1.0", r)

    #Creer un nouveau fichier
    def nouveau(self):
        os.popen("python main.py")

    #Enregistrer un document
    def enregistrer_sous(self):
        fichier = filedialog.asksaveasfilename(defaultextension ='.*', initialdir="/", title='Enregistrer sous', filetype= (("Text File", "*.txt"), ("xls file", "*.xls"), ("All File", "*.*")))
        f = open(fichier, 'w')
        s = self.content.get("1.0", END)
        f.write(s)
        f.close()

    def add_menu(self):
        menuBar = Menu(self.master)
        menuFichier = Menu(menuBar, tearoff=False)
        menuBar.add_cascade(label="Fichier", menu=menuFichier)
        menuFichier.add_command(label="Quitter", command=self.quitter)
        menuFichier.add_command(label="Ouvrir", command=self.ouvrir)
        menuFichier.add_command(label="Enregistrer sous", command=self.enregistrer_sous)
        menuFichier.add_command(label="Nouveau", command=self.nouveau)
        self.master.config(menu=menuBar)
