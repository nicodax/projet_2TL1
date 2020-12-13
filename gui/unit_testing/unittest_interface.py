#!/usr/bin/env python3
import os
import unittest
import cli.cli_misc
from gui.exceptions import UserNameNotFoundException, WrongExtensionException
from classes.exceptions import UnknownPasswordException
from gui.interface_graphique import connexion, open, verify_extension


class TestLoginInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre login_window d'un
        utilisateur dans l'interface graphique.
        * login()
    """

    def test_recognized_username(self):
        """login() avec un nom utilisateurs reconnu"""
        os.chdir("../..")
        username1 = "greg"
        username2 = "dax"
        all_students = cli.cli_misc.pickle_get(students_arg=True)[0]
        self.assertEqual(True, (username1 in all_students["name_id_dict"]))
        self.assertEqual(True, (username2 in all_students["name_id_dict"]))
        os.chdir("gui/unit_testing")

    def test_unknow_username(self):
        """login() avec un nom utilisateurs inconnu"""
        self.assertRaises(UserNameNotFoundException, connexion)

    def test_good_password(self):
        """login() avec un mot de passe correspondant au nom utilisateurs reconnu"""
        password1 = "user123"
        username1 = "greg"
        student_instance = cli.cli_misc.pickle_get_instance(username1, student=True)
        self.assertEqual(True, student_instance.verify_pwd(password1))

    def test_wrong_password(self):
        """login() avec un mot de passe ne correspondant pas au nom utilisateurs reconnu"""
        self.assertRaises(UnknownPasswordException, connexion)


class TestToolInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre tool_window d'un
         utilisateur dans l'interface graphique.
         * open()
         * delete()
         * get_list()
         * sort()
     """

    def test_good_extension(self):
        """open() avec la bonne extension(.py ou .txt)"""
        file_test1 = "Doctest.py"
        file_test2 = "Doctest.txt"
        self.assertEqual(True, verify_extension(file_test1))
        self.assertEqual(True, verify_extension(file_test2))

    def test_wrong_extension(self):
        """open() avec la bonne extension(.py ou .txt)"""
        self.assertRaises(WrongExtensionException, open)


class TestEditorInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre tool_window d'un
             utilisateur dans l'interface graphique.
             * open()
             * delete()
             * get_list()
             * sort()
         """
