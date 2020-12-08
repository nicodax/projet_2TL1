from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginApp(App):
    def build(self):
        self.title = 'login_window'
        box = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text='Veuillez entrer le user et le mdp'))
        box.add_widget(TextInput())
        box.add_widget(TextInput())
        box.add_widget(Button(text='Se connecter'))

        return box



Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '50')

LoginApp().run()


def test():
    print('yo ca va')
