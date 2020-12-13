#!/usr/bin/env python3
from cli.cli_misc import pickle_get, pickle_get_instance
from classes.exceptions import UnknownPasswordException
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from cli.exceptions import UnknownObjectException
from gui.exceptions import UserNameNotFoundException
from cli.cli_student import list_sorted_files_on_tags, list_sorted_files_on_course


class LoginWindow(Screen):
    def connexion(self):
        try:
            list_users = pickle_get(students_arg=True)[0]["name_id_dict"].keys()
            if self.ids.Usrname.text in list_users:
                student_instance = pickle_get_instance(self.ids.Usrname.text, student=True)
                if not student_instance.verify_pwd(self.ids.Psw.text):
                    raise UnknownPasswordException
                ToolWindow.student_instance = student_instance
            else:
                raise UserNameNotFoundException
        except UnknownPasswordException:
            self.ids.Error.text = "Mauvais mot de passe !"
        except UserNameNotFoundException:
            self.ids.Error.text = "Mauvais nom d'utilisateurs !"
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            self.ids.Error.text = "Connexion en cours..."
            return True


class ToolWindow(Screen):
    student_instance = None

    def new(self):
        self.ids.Affichage.text = "Lancemement d'un nouveau fichier."

    def open(self):
        file = "C:/Users/delan/Downloads/aventure.txt"
        resultat = ""
        with open(file, 'r') as filin:
            lignes = filin.readlines()
            for ligne in lignes:
                resultat += ligne
        self.ids.TextArea.text = resultat

    def delete(self):
        self.ids.Affichage.text = "Suppression d'un fichier existant."

    @staticmethod
    def list_to_string(liste):
        resultat = ""
        for x in liste:
            resultat += x + ', '
        resultat = resultat[:-2]
        return resultat

    def list(self):
        list_users = pickle_get(students_arg=True)[0]["name_id_dict"].keys()
        list_courses = pickle_get(courses_arg=True)[3]["name_id_dict"].keys()
        list_files = pickle_get(files_arg=True)[2]["name_id_dict"].keys()
        if self.ids.Recherche.text == "etudiants":
            self.ids.Affichage.text = self.list_to_string(list_users)
        elif self.ids.Recherche.text == "cours":
            self.ids.Affichage.text = self.list_to_string(list_courses)
        elif self.ids.Recherche.text == "fichiers":
            self.ids.Affichage.text = self.list_to_string(list_files)
        else:
            self.ids.Affichage.text = 'Veuillez entrer:"etudiants","cours" ou "fichiers"'

    def sort_on_course(self):
        try:
            valid_course_name = False
            list_courses = pickle_get(courses_arg=True)[3]["name_id_dict"].keys()
            for x in list_courses:
                if self.ids.Recherche.text == x:
                    valid_course_name = True
            if not valid_course_name:
                raise UnknownObjectException
        except UnknownObjectException:
            self.ids.Affichage.text = "Le cours entre n'existe pas."
        except Exception as e:
            self.ids.Affichage.text = f"Erreur : {e}\n"
        else:
            list_dict = list_sorted_files_on_course([self.ids.Recherche.text], self.student_instance)
            all_pathname = []
            for x in list_dict:
                all_pathname.append(x["pathname"])
            self.ids.Affichage.text = self.list_to_string(all_pathname)

    def sort_on_tag(self):
        list_dict = list_sorted_files_on_tags([self.ids.Recherche.text], self.student_instance)
        all_pathname = []
        for x in list_dict:
            all_pathname.append(x["pathname"])
        self.ids.Affichage.text = self.list_to_string(all_pathname)


class EditorWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("gui/my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyMainApp().run()
