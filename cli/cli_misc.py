#!/usr/bin/env python3
import getpass
import pickle

from cli.temp_exceptions import UnknownUsernameException, FileNotOwnedException, FileNotFoundException


def users_terminal_display(content_to_display):
    pass


def files_terminal_display(content_to_display):
    pass


def courses_terminal_display(content_to_display):
    pass


def pickle_get_file_if_owned(user_instance, pathname):
    """Methode renvoyant l'instance de la classe File associee a un fichier si l'utilisateur connecte le possede"""

    persistent_data = pickle_get(files=True)
    all_files = persistent_data[2]

    if pathname in all_files["name_id_dict"]:
        file_id = all_files["name_id_dict"][pathname]
        file_instance = all_files["objects_dict"][file_id]
        if file_id in user_instance.files:
            return file_instance
        else:
            raise FileNotOwnedException
    else:
        raise FileNotFoundException


def pickle_get(students=False, admins=False, files=False, courses=False, id_dict=None):
    """Fonction permettant de recuperer les classes persistantes du programme
            Seules les classes specifies dans les parametres sont recuperees
    """

    all_students = {}
    all_admins = {}
    all_files = {}
    all_courses = {}
    id_dict = {}

    if students:
        with open("pickle_saves/students.pkl", 'rb') as students_file:
            all_students = pickle.load(students_file)
    if admins:
        with open("pickle_saves/admins.pkl", 'rb') as admins_file:
            all_admins = pickle.load(admins_file)
    if files:
        with open("pickle_saves/files.pkl", 'rb') as files_file:
            all_files = pickle.load(files_file)
    if courses:
        with open("pickle_saves/courses.pkl", 'rb') as courses_file:
            all_courses = pickle.load(courses_file)
    if id_dict:
        with open("pickle_saves/id_dict.pkl", 'rb') as id_dict_file:
            id_dict = pickle.load(id_dict_file)

    return [all_students, all_admins, all_files, all_courses, id_dict]


def pickle_save(all_students=None, all_admins=None, all_files=None, all_courses=None, id_dict=None):
    """Fonction permettant d'enregistrer les modifications sur les classes persistantes du programme
            Seules les classes specfiees dans les parametres sont sauvegardees
    """

    if all_students is not None:
        with open("pickle_saves/students.pkl", 'wb') as students_file:
            pickle.dump(all_students, students_file)
    if all_admins is not None:
        with open("pickle_saves/admins.pkl", 'wb') as admins_file:
            pickle.dump(all_admins, admins_file)
    if all_files is not None:
        with open("pickle_saves/files.pkl", 'wb') as files_file:
            pickle.dump(all_files, files_file)
    if all_courses is not None:
        with open("pickle_saves/courses.pkl", 'wb') as courses_file:
            pickle.dump(all_courses, courses_file)
    if id_dict is not None:
        with open("pickle_saves/id_dict.pkl", 'wb') as id_dict_file:
            pickle.dump(id_dict, id_dict_file)


def login():
    """Fonction permettant de se connecter a un compte utilisateur"""

    username = input("Veuillez entrer votre nom d'utilisateur :")
    persistent_data = pickle_get(students=True, admins=True)
    all_students = persistent_data[0]
    all_admins = persistent_data[1]

    if username in all_students["name_id_dict"]:
        pwd = getpass.getpass("Veuillez entrer votre mot de passe :")
        user_id = all_students["name_id_dict"][username]
        user_instance = all_students["objects_dict"][user_id]
        user_instance.verify_pwd(pwd)
        return user_instance, False
    elif username in all_admins["name_id_dict"]:
        pwd = getpass.getpass("Veuillez entrer votre mot de passe :")
        user_id = all_admins["name_id_dict"][username]
        user_instance = all_admins["objects_dict"][user_id]
        user_instance.verify_pwd(pwd)
        return user_instance, True
    else:
        raise UnknownUsernameException
