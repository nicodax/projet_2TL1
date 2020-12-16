#!/usr/bin/env python3
import os
from tkinter import filedialog

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from classes.exceptions import UnknownPasswordException, AlreadyInListException, NotInListException
from cli.cli_misc import pickle_get, pickle_get_instance, pickle_get_file_if_owned
from cli.cli_student import list_sorted_files_on_tags, list_sorted_files_on_course, new_file, file_add_tag, \
    file_add_course, file_remove_tag, file_remove_course, delete_file, move_file, file_change_script_attribute
from cli.exceptions import UnknownObjectException, ArgumentException
from gui.exceptions import UserNameNotFoundException, SamePathnameException


########################################################################################################
# LOGIN WINDOW
########################################################################################################

class LoginWindow(Screen):
    """Cette classe permet de creer une fenetre pour le login de l'utilisateur"""

    def connexion(self):
        """
        PRE:
        POST: Lance tool.window si le nom utilisateur existe et que le mot de passe correspond.
        RAISES:     -UserNameNotFoundException si le nom utilisateur n'existe pas.
                    -UnknownPasswordException si le mot de passe ne correspond pas au nom utilisateur reconnu.
        """
        try:
            list_users = pickle_get(students_arg=True)[0]["name_id_dict"].keys()
            if self.ids.Usrname.text in list_users:
                student_instance = pickle_get_instance(self.ids.Usrname.text, student=True)
                if not student_instance.verify_pwd(self.ids.Psw.text):
                    raise UnknownPasswordException
                ToolWindow.student_instance = student_instance
                EditorWindow.student_instance = student_instance
            else:
                raise UserNameNotFoundException
        except UnknownPasswordException:
            self.ids.Error.text = "Mauvais mot de passe !"
        except UserNameNotFoundException:
            self.ids.Error.text = "Mauvais nom d'utilisateurs !"
        except Exception as e:
            self.ids.Error.text = f"Erreur : {e}\n"
        else:
            self.ids.Error.text = "Connexion en cours..."
            return True


########################################################################################################
# TOOL WINDOW
########################################################################################################
class HListBox(Widget):
    """Cette classe permet de creer une ligne au sein de l'interface pour l'utilisation de list"""
    def __init__(self, **kwargs):
        super(HListBox, self).__init__(**kwargs)


class HSortBox(Widget):
    """Cette classe permet de creer une ligne au sein de l'interface pour l'utilisation de sort"""
    def __init__(self, **kwargs):
        super(HSortBox, self).__init__(**kwargs)


class ToolWindow(Screen):
    """
    Cette classe permet de creer une fenetre rassemblant tous les outils disponibles a l'utilisateur connecte

    Variables de classe:
        student_instance:   instance de classe de l'utilisateur connecté
        sort_choice:        lors de l'utilisation de sort(), doit avoir une de ces deux valeurs ("course" ou "tag")
        list_choice:        lors de l'utilisation de sort(), doit avoir une de ces trois valeurs ("students",
                                "courses" ou "files")
    """
    student_instance = None
    sort_choice = None
    list_choice = None

    def new(self):
        """
        PRE:
        POST: Ouvre le fenetre EditorWindow.
        RAISES:
        """
        self.ids.Affichage.text = "Lancemement d'un nouveau fichier."

    @staticmethod
    def list_to_string(liste):
        """
        PRE:
        POST: Recoit une liste et la transforme en string.
        RAISES:
        """
        resultat = ""
        for x in liste:
            resultat += x + ', '
        resultat = resultat[:-2]
        return resultat

    def open_list_choices(self):
        """
        PRE:
        POST: ouvre la liste deroulante des choix de listage
        RAISES:
        """
        dropdown = CustomDropDown()
        self.ids.HListBox.ids.List.bind(on_release=dropdown.open)

    def open_sort_choices(self):
        """
        PRE:
        POST: ouvre la liste deroulante des choix de triage
        RAISES:
        """
        dropdown = CustomDropDown2()
        self.ids.HSortBox.ids.SortList.bind(on_release=dropdown.open)

    def list(self):
        """
        PRE: list_choice doit avoir la valeur "students", "courses" ou "files"
        POST: Affiche la liste des fichiers, des cours ou des utilisateurs recenses
                dans Affichage(Label) en fonction de la valeur de Recherche(TextInput).
        RAISES: UnknownObjectException se lance si la valeur de Recherche(TextInput) n'est pas
                    un argument reconnu.
        """
        list_users = pickle_get(students_arg=True)[0]["name_id_dict"].keys()
        list_courses = pickle_get(courses_arg=True)[3]["name_id_dict"].keys()
        list_files = pickle_get(files_arg=True)[2]["name_id_dict"].keys()
        list_owned_files = []
        for pathname in list_files:
            file_instance_id = pickle_get_instance(pathname, file=True).file_id
            if file_instance_id in self.student_instance.files:
                list_owned_files.append(pathname)
        if self.list_choice == "students":
            self.ids.Affichage.text = self.list_to_string(list_users)
        elif self.list_choice == "courses":
            self.ids.Affichage.text = self.list_to_string(list_courses)
        elif self.list_choice == "files":
            self.ids.Affichage.text = self.list_to_string(list_owned_files)

    def sort_launcher(self):
        """
        PRE: sort_choice doit avoir la valeur "course" ou "tag"
        POST: en fonction de la valeur de sort_choice, lance la methode adequate
        RAISES:
        """
        if self.sort_choice == "course":
            self.sort_on_course()
        elif self.sort_choice == "tag":
            self.sort_on_tag()

    def sort_on_course(self):
        """
        PRE:
        POST: Affiche la liste des fichiers tries dans Affichage(Label) en fonction du
                cours defini dans Recherche(TextInput).
        RAISES: UnknownObjectException si la valeur de Recherche(TextInput) n'est pas
                    un argument reconnu.
        """
        try:
            valid_course_name = False
            list_courses = pickle_get(courses_arg=True)[3]["name_id_dict"].keys()
            for x in list_courses:
                if self.ids.HSortBox.ids.Recherche.text == x:
                    valid_course_name = True
            if not valid_course_name:
                raise UnknownObjectException
        except UnknownObjectException:
            self.ids.Affichage.text = "Le cours entre n'existe pas."
        except Exception as e:
            self.ids.Affichage.text = f"Erreur : {e}\n"
        else:
            list_dict = list_sorted_files_on_course([self.ids.HSortBox.ids.Recherche.text], self.student_instance)
            all_pathname = []
            for x in list_dict:
                all_pathname.append(x["pathname"])
            self.ids.Affichage.text = self.list_to_string(all_pathname)

    def sort_on_tag(self):
        """
        PRE:
        POST: Affiche la liste des fichiers tries dans Affichage(Label) en fonction de
                l'etiquette definie dans Recherche(TextInput).
        RAISES:
        """
        list_dict = list_sorted_files_on_tags([self.ids.HSortBox.ids.Recherche.text], self.student_instance)
        all_pathname = []
        for x in list_dict:
            all_pathname.append(x["pathname"] + "  [" + x["tags"] + "]")
        self.ids.Affichage.text = self.list_to_string(all_pathname)


########################################################################################################
# EDITOR WINDOW
########################################################################################################

class EditorWindow(Screen):
    """
    Cette classe permet de creer une fenetre avec un editeur de texte pour le fichier ouvert et differents outils
    specifiques a la gestion de fichier


    Variables de classe:
        student_instance:   instance de classe de l'utilisateur connecté
        pathname:           pathname du fichier ouvert dans l'editeur
    """
    student_instance = None
    pathname = ""

    def open(self):
        """
        PRE:
        POST: Ouvre un navigateur de fichier, puis après avoir choisis un fichier,
                  implemente son contenu dans TextArea(textInput).
        RAISES:
        """
        self.pathname = filedialog.askopenfilename(initialdir="/", title="Choisir le fichier",
                                                   filetype=[("Text File", "*.txt"), ("Python File", "*.py")])
        list_files = pickle_get(files_arg=True)[2]["name_id_dict"].keys()
        if self.pathname not in list_files:
            new_file(self.pathname, True, None, None, self.student_instance)

        resultat = ""
        with open(self.pathname, 'r') as filin:
            lignes = filin.readlines()
            for ligne in lignes:
                resultat += ligne
        self.ids.TextArea.text = resultat
        self.ids.Affichage.text = "Le fichier  '"+self.pathname.split('/')[-1]+"' a été ouvert"

    def enregistrer_sous(self):
        """
        PRE:
        POST: Ouvre le navigateur de fichier apres avoir cliquer sur l'onglet
                  enregistrer et sauvegarde le fichier a l endroit choisi.
        RAISES:
        """
        self.pathname = filedialog.asksaveasfilename(defaultextension='.*', initialdir="/", title='Enregistrer sous',
                                                     filetype=(
                                                         ("Text File", "*.txt"), ("xls file", "*.xls"),
                                                         ("All File", "*.*")))
        list_files = pickle_get(files_arg=True)[2]["name_id_dict"].keys()
        if self.pathname not in list_files:
            new_file(self.pathname, True, None, None, self.student_instance)
        f = open(self.pathname, 'w')
        s = self.ids.TextArea.text
        f.write(s)
        f.close()
        self.ids.Affichage.text = "Le fichier '" + self.pathname.split('/')[-1] + "' a été enregistré"

    def file_add_tag_gui(self):
        """
        PRE:
        POST: ajoute l'etiquette specifiee si elle n'est pas deja referencee
        RAISES: AlreadyInListException si l'etiquette specifiee est deja referencee
        """
        try:
            tag = [self.ids.Recherche.text]
            file_add_tag(self.pathname, tag)
        except AlreadyInListException:
            self.ids.Error.text = "Erreur : l'etiquette specifiee existe deja"
        except Exception as e:
            self.ids.Error.text = f"Erreur : {e}"
        else:
            self.ids.Error.text = f"L'etiquette a correctement ete assignee au fichier"

    def file_add_course_gui(self):
        """
        PRE:
        POST: associe le fichier au cours specifie
        RAISES:
        """
        try:
            course_name = self.ids.Recherche.text
            file_add_course(self.pathname, course_name)
        except UnknownObjectException:
            self.ids.Error.text = "Erreur : le cours spécifié n'existe pas"
        except AlreadyInListException:
            self.ids.Error.text = "Erreur : le fichier est deja associe a ce cours"
        except Exception as e:
            self.ids.Error.text = f"Erreur : {e}"
        else:
            self.ids.Error.text = f"Le fichier a correctement ete assigne au cours"

    def file_remove_tag_gui(self):
        """
        PRE:
        POST: retire l'etiquette specifiee si elle est deja referencee
        RAISES: NotInListException si l'etiquette specifiee n'est pas deja referencee
        """
        try:
            tag = self.ids.Recherche.text
            file_remove_tag(self.pathname, tag)
        except NotInListException:
            self.ids.Error.text = "Erreur : l'etiquette specifiee n'existe pas"
        except Exception as e:
            self.ids.Error.text = f"Erreur : {e}"
        else:
            self.ids.Error.text = f"L'etiquette a correctement ete retiree du fichier"

    def file_remove_course_gui(self):
        """
        PRE:
        POST: dissocie le fichier de tout cours
        RAISES:
        """
        try:
            file_remove_course(self.pathname)
        except Exception as e:
            self.ids.Error.text = f"Erreur : {e}"
        else:
            self.ids.Error.text = f"Le fichier a correctement ete assigne au cours"

    def file_change_script_attribute_gui(self):
        """
        PRE:
        POST: indique si le fichier est un script ou non
        RAISES:
        """
        try:
            script_string = self.ids.Recherche.text
            if script_string == "True" or script_string == "true":
                script = True
            elif script_string == "False" or script_string == "false":
                script = False
            else:
                raise ArgumentException
            file_change_script_attribute(self.pathname, script)
        except ArgumentException:
            self.ids.Error.text = "Erreur : la valeur de script peut être True, False, true, false"
        except Exception as e:
            self.ids.Error.text = f"Erreur : {e}"
        else:
            self.ids.Error.text = f"L'attribut file.script a correctement ete modifie"

    def deplacer(self):
        """
        PRE:
        POST: Ouvre le navigateur de fichier apres avoir cliquer sur le bouton deplacer
                et deplace le fichier a l endroit choisi.
        RAISES: SamePathnameException est appele si l'ancien pathname correspond a l'endroit choisi.
        """
        try:
            new_pathname = filedialog.asksaveasfilename(defaultextension='.*', initialdir="/", title='Enregistrer sous',
                                                        filetype=(
                                                            ("Text File", "*.txt"), ("xls file", "*.xls"),
                                                            ("All File", "*.*")))
            list_files = pickle_get(files_arg=True)[2]["name_id_dict"].keys()
            if new_pathname not in list_files:
                new_file(new_pathname, True, None, None, self.student_instance)
            if self.pathname != new_pathname:
                f = open(new_pathname, 'w')
                s = self.ids.TextArea.text
                f.write(s)
                move_file(self.pathname, new_pathname)
                os.remove(self.pathname)
                self.pathname = new_pathname
                f.close()
            else:
                raise SamePathnameException
        except SamePathnameException:
            self.ids.Affichage.text = "Le nouvel emplacement est le meme que le precedent."
        except Exception as e:
            self.ids.Affichage.text = f"Erreur : {e}"
        else:
            self.ids.Affichage.text = "Le fichier a ete deplace."

        new_pathname = filedialog.asksaveasfilename(defaultextension='.*', initialdir="/", title='Enregistrer sous',
                                                    filetype=[
                                                        ("Text File", "*.txt"), ("xls file", "*.xls"),
                                                        ("All File", "*.*")])
        list_files = pickle_get(files_arg=True)[2]["name_id_dict"].keys()
        if new_pathname not in list_files:
            new_file(new_pathname, True, None, None, self.student_instance)
        f = open(new_pathname, 'w')
        s = self.ids.TextArea.text
        f.write(s)
        move_file(self.pathname, new_pathname)
        os.remove(self.pathname)
        self.pathname = new_pathname
        f.close()

    def delete(self):
        """
        PRE:
        POST: Supprime le fichier ouvert actuellement.
        RAISES:
        """
        try:
            file_instance = pickle_get_file_if_owned(self.student_instance, self.pathname)
            delete_file(file_instance, self.student_instance)
        except Exception as e:
            self.ids.Affichage.text = f"Erreur : {e}"
        else:
            self.ids.TextArea.text = ""
            self.ids.Affichage.text = "Le fichier '"+self.pathname.split('/')[-1]+"' a été supprimé"


########################################################################################################
# WINDOW MANAGER
########################################################################################################


class WindowManager(ScreenManager):
    """
    Correspond a la fenetre mere de LoginWindow, ToolWindow et EditorWindow. C'est la
    classe qui permet de passer d un ecran a l autre (module ScreenManager).
    """
    pass


class CustomDropDown(DropDown):
    """Cette classe permet la construction de la dropdown list associee aux choix de listage"""
    pass


class CustomDropDown2(DropDown):
    """Cette classe permet la construction de la dropdown list associee aux choix de triage"""
    pass


buildWindow = Builder.load_file("gui/buildWindow.kv")


class projet_2TL1_09(App):
    """
    Il s'agit du corps de l'application.
    """
    def build(self):
        return buildWindow


if __name__ == '__main__':
    projet_2TL1_09().run()
