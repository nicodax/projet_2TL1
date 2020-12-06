from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Label
import os

def recupTexte(file):
    resultat = ""
    with open(file , 'r') as filin:
        lignes = filin.readlines()
        for ligne in lignes:
            resultat += ligne
    return resultat

def ouvrirConsole3(file):
    class HelloApp(App):
        def build(self):
            self.title = 'Hello World!'
            return Label(text=recupTexte(file))
    Config.set('graphics', 'width', '300')
    Config.set('graphics', 'height', '150')

    HelloApp().run()

ouvrirConsole3('C:/Users/delan/Downloads/aventure.txt')

