from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Label


def get_text(pathname):
    resultat = ""
    with open(pathname, 'r') as filin:
        lignes = filin.readlines()
        for ligne in lignes:
            resultat += ligne
    return resultat


def open_file(pathname):
    class HelloApp(App):
        def build(self):
            self.title = 'Hello World!'
            return Label(text=get_text(pathname))

    Config.set('graphics', 'width', '300')
    Config.set('graphics', 'height', '150')

    HelloApp().run()


if __name__ == "__main__":
    open_file('../files/test2.txt')
