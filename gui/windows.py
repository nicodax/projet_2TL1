#!/usr/bin/env python3
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


def testhello(hello):
    print(hello)


class LoginApp(App):
    def build(self):
        self.title = 'login_window'
        box = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text='Veuillez entrer le user et le mdp'))
        box.add_widget(TextInput())
        box.add_widget(TextInput())
        box.add_widget(Button(text='Se connecter', on_press=testhello('hello')))


        return box


class ToolApp(App):
    def build(self):
        self.title = 'tool_window'
        box = BoxLayout(orientation='horizontal')
        box.add_widget(Button(text='Nouveau'))
        box.add_widget(Button(text='Ouvrir'))
        box.add_widget(Button(text='Supprimer'))
        box.add_widget(Button(text='Afficher'))
        box.add_widget(Button(text='Trier'))

        return box


class EditorApp(App):
    def build(self):
        self.title = 'editor_window'
        box = BoxLayout(orientation='horizontal')
        box.add_widget(TextInput())

        return box


Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '50')

LoginApp().run()
