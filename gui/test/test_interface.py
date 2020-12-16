#!/usr/bin/env python3
import os

from cli.cli_student import new_file, delete_file

os.chdir("../..")
import unittest
from cli.cli_misc import pickle_get, pickle_get_instance
from classes.exceptions import UnknownPasswordException
from main import ToolWindow, EditorWindow


class TestLoginInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre login_window d'un
        utilisateur dans l'interface graphique.
        * connexion()
    """

    def test_recognized_username(self):
        """connexion() avec un nom utilisateurs reconnu"""
        username1 = "greg"
        username2 = "dax"
        list_users = pickle_get(students_arg=True)[0]["name_id_dict"].keys()
        self.assertEqual(True, (username1 in list_users))
        self.assertEqual(True, (username2 in list_users))

    def test_unknow_username(self):
        """connexion() avec un nom utilisateurs inconnu"""
        username1 = "prof1"
        username2 = "prof2"
        list_users = pickle_get(students_arg=True)[0]["name_id_dict"].keys()
        self.assertEqual(True, (username1 not in list_users))
        self.assertEqual(True, (username2 not in list_users))

    def test_good_password(self):
        """connexion() avec un mot de passe correspondant au nom utilisateurs reconnu"""
        password1 = "user123"
        username1 = "greg"
        student_instance = pickle_get_instance(username1, student=True)
        self.assertEqual(True, student_instance.verify_pwd(password1))

    def test_wrong_password(self):
        """connexion() avec un mot de passe ne correspondant pas au nom utilisateurs reconnu"""
        password1 = "user987"
        username1 = "greg"
        student_instance = pickle_get_instance(username1, student=True)
        self.assertRaises(UnknownPasswordException, student_instance.verify_pwd, password1)


class TestToolInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre tool_window d'un
         utilisateur dans l'interface graphique.
         * list_to_string(liste)
     """

    def test_list_to_string(self):
        resultat_test = 'test1, test2, test3'
        liste_test = ['test1', 'test2', 'test3']
        self.assertEqual(resultat_test, ToolWindow.list_to_string(liste_test))

        resultat_test = 'test, test, test'
        liste_test = ['test', 'test', 'test']
        self.assertEqual(resultat_test, ToolWindow.list_to_string(liste_test))

        resultat_test = 'testA, testB, testC'
        liste_test = ['testA', 'testB', 'testC']
        self.assertEqual(resultat_test, ToolWindow.list_to_string(liste_test))


class TestEditorInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre tool_window d'un
             utilisateur dans l'interface graphique.
             * delete()
             * deplacer()
         """

    # def test_deplacer(self):
    #    """Deplacer()"""
    #    old_pathname = "files/test.txt"
    #    new_pathname = "files1/test.txt"

    def test_delete(self):
        """Cette fonction test le fait que le fichier est bel et bien supprimé."""
        EditorWindow.pathname = "files/test.txt"
        EditorWindow.student_instance = pickle_get_instance("greg", student=True)
        new_file(EditorWindow.pathname, False, None, None, EditorWindow.student_instance)
        file_instance = pickle_get_instance(EditorWindow.pathname, file=True)
        self.assertEqual(True, os.path.isfile(EditorWindow.pathname))
        delete_file(file_instance, EditorWindow.student_instance)
        self.assertEqual(False, os.path.isfile(EditorWindow.pathname))
