#!/usr/bin/env python3
import os
import unittest
from cli.cli_misc import pickle_get, pickle_get_instance
from gui.exceptions import UserNameNotFoundException
from classes.exceptions import UnknownPasswordException
from main import LoginWindow


class TestLoginInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre login_window d'un
        utilisateur dans l'interface graphique.
        * connexion()
    """

    def test_recognized_username(self):
        """connexion() avec un nom utilisateurs reconnu"""
        os.chdir("../..")
        username1 = "greg"
        username2 = "dax"
        list_users = pickle_get(students_arg=True)[0]["name_id_dict"].keys()
        self.assertEqual(True, (username1 in list_users))
        self.assertEqual(True, (username2 in list_users))
        os.chdir("gui/unit_testing")


    def test_unknow_username(self):
        """login() avec un nom utilisateurs inconnu"""
        os.chdir("../..")
        self.assertRaises(UserNameNotFoundException, LoginWindow.connexion)
        os.chdir("gui/unit_testing")

    def test_good_password(self):
        """login() avec un mot de passe correspondant au nom utilisateurs reconnu"""
        password1 = "user123"
        username1 = "greg"
        student_instance = pickle_get_instance(username1, student=True)
        self.assertEqual(True, student_instance.verify_pwd(password1))

    def test_wrong_password(self):
        """login() avec un mot de passe ne correspondant pas au nom utilisateurs reconnu"""
        self.assertRaises(UnknownPasswordException, LoginWindow.connexion)


class TestToolInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre tool_window d'un
         utilisateur dans l'interface graphique.
         * open()
         * delete()
         * get_list()
         * sort()
     """


class TestEditorInterface(unittest.TestCase):
    """ Cette classe teste les methodes associees a la fenetre tool_window d'un
             utilisateur dans l'interface graphique.
             * open()
             * delete()
             * get_list()
             * sort()
         """
