#!/usr/bin/env python3
from cli.cli_misc import pickle_get, pickle_get_instance
from classes.exceptions import UnknownPasswordException, AlreadyInListException, NotInListException
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from tkinter import filedialog
from cli.exceptions import UnknownObjectException, ArgumentException
from gui.exceptions import UserNameNotFoundException
from cli.cli_student import list_sorted_files_on_tags, list_sorted_files_on_course, new_file, file_add_tag, \
    file_add_course, file_remove_tag, file_remove_course, file_change_script_attribute


########################################################################################################
# LOGIN WINDOW
########################################################################################################

class LoginWindow(Screen):
    def connexion(self):
        """
        POST: Lance tool.window si le nom utilisateur existe et que le mot de passe correspond.
        RAISES:
            -UserNameNotFoundException si le nom utilisateur n'existe pas.
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

class ToolWindow(Screen):
    student_instance = None

    def new(self):
        """
        POST: Ouvre le fenetre EditorWindow.
        """
        self.ids.Affichage.text = "Lancemement d'un nouveau fichier."

    @staticmethod
    def list_to_string(liste):
        """
        POST: Recoit une liste et la transforme en string.
        """
        resultat = ""
        for x in liste:
            resultat += x + ', '
        resultat = resultat[:-2]
        return resultat

    def list(self):
        """
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
        if self.ids.Recherche.text == "etudiants":
            self.ids.Affichage.text = self.list_to_string(list_users)
        elif self.ids.Recherche.text == "cours":
            self.ids.Affichage.text = self.list_to_string(list_courses)
        elif self.ids.Recherche.text == "fichiers":
            self.ids.Affichage.text = self.list_to_string(list_owned_files)
        else:
            self.ids.Affichage.text = 'Veuillez entrer:"etudiants","cours" ou "fichiers"'

    def sort_on_course(self):
        """
        POST: Affiche la liste des fichiers tries dans Affichage(Label) en fonction du
            cours defini dans Recherche(TextInput).
        RAISES:
              -UnknownObjectException si la valeur de Recherche(TextInput) n'est pas
            un argument reconnu.
        """
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
        """
        POST: Affiche la liste des fichiers tries dans Affichage(Label) en fonction de
             l'etiquette definie dans Recherche(TextInput).
        """
        list_dict = list_sorted_files_on_tags([self.ids.Recherche.text], self.student_instance)
        all_pathname = []
        for x in list_dict:
            all_pathname.append(x["pathname"] + "  [" + x["tags"] + "]")
        self.ids.Affichage.text = self.list_to_string(all_pathname)


########################################################################################################
# EDITOR WINDOW
########################################################################################################

class EditorWindow(Screen):
    student_instance = None
    pathname = ""

    def open(self):
        """
        POST: Ouvre un navigateur de fichier, puis après avoir choisis un fichier,
            implement son contenu dans TextArea(textInput).
        """
        self.pathname = filedialog.askopenfilename(initialdir="/", title="Choisir le fichier",
                                                   filetype=(("Text File", "*.txt"), ("All Files", "*.*")))
        list_files = pickle_get(files_arg=True)[2]["name_id_dict"].keys()
        if self.pathname not in list_files:
            new_file(self.pathname, True, None, None, self.student_instance)

        resultat = ""
        with open(self.pathname, 'r') as filin:
            lignes = filin.readlines()
            for ligne in lignes:
                resultat += ligne
        self.ids.TextArea.text = resultat

    def enregistrer_sous(self):
        """
        POST: Ouvre le navigateur de fichier apres avoir cliquer sur l'onglet
            enregistrer et sauvegarde le fichier a l endroit choisi.
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

    def delete(self):
        """
        POST: Ouvre un navigateur de fichier, puis après avoir choisis un fichier,
            supprime ce dernier.
         RAISES: Affiche un message d erreur si le fichier n'a ni l'extension .txt, ni
            l'extension .py.
        """
        pass

    def file_add_tag_gui(self):
        """
        POST : ajoute l'etiquette specifiee si elle n'est pas deja referencee
        RAISES : AlreadyInListException si l'etiquette specifiee est deja referencee
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
        POST : associe le fichier au cours specifie
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
        POST : retire l'etiquette specifiee si elle est deja referencee
        RAISES : NotInListException si l'etiquette specifiee n'est pas deja referencee
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
        POST : dissocie le fichier de tout cours
        """
        try:
            file_remove_course(self.pathname)
        except Exception as e:
            self.ids.Error.text = f"Erreur : {e}"
        else:
            self.ids.Error.text = f"Le fichier a correctement ete assigne au cours"

    def file_change_script_attribute_gui(self):
        """
        POST : indique si le fichier est un script ou non
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
        POST: Ouvre le navigateur de fichier apres avoir cliquer sur l'onglet
            deplacer et deplace le fichier a l endroit choisi.
        """
        pass


########################################################################################################
# WINDOW MANAGER
########################################################################################################


class WindowManager(ScreenManager):
    pass


buildWindow = Builder.load_file("gui/buildWindow.kv")


class MyMainApp(App):
    def build(self):
        return buildWindow


if __name__ == '__main__':
    MyMainApp().run()
