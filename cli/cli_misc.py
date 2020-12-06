#!/usr/bin/env python3
import getpass
import pickle

from cli.temp_exceptions import UnknownUsernameException, FileNotOwnedException, FileNotFoundException, \
    IncorrectUseOfArgumentsException


def users_terminal_display(content_to_display):
    id_max_len = 3
    username_max_len = 25
    print(" id   username                         fullname")
    print("-----------------------------------------------------------------------")
    for i in content_to_display:
        add_to_id = ""
        spaces_to_add_to_id = id_max_len - len(str(i["user_id"]))
        for j in range(spaces_to_add_to_id):
            add_to_id += " "

        add_to_username = ""
        spaces_to_add_to_username = username_max_len - len(i["username"])
        for j in range(spaces_to_add_to_username):
            add_to_username += " "
        print(f" {i['user_id']}{add_to_id}  {i['username']}{add_to_username}        {i['fullname']}")
    print("\n")


def files_terminal_display(content_to_display):
    pass


def courses_terminal_display(content_to_display):
    id_max_len = 3
    name_max_len = 5
    description_max_len = 50
    print(" id   code   intitule                                           professeurs")
    print("---------------------------------------------------------------------------------------------" +
          "-----------------------------------")
    for i in content_to_display:
        add_to_id = ""
        spaces_to_add_to_id = id_max_len - len(str(i["course_id"]))
        for j in range(spaces_to_add_to_id):
            add_to_id += " "
        add_to_name = ""
        spaces_to_add_to_name = name_max_len - len(str(i["course_name"]))
        for j in range(spaces_to_add_to_name):
            add_to_name += " "
        add_to_description = ""
        spaces_to_add_to_description = description_max_len - len(str(i["description"]))
        for j in range(spaces_to_add_to_description):
            add_to_description += " "
        print(f" { i['course_id']}{add_to_id}  {i['course_name']}{add_to_name}  {i['description']}{add_to_description}",
              f"{i['teachers']}")
    print("\n")


def pickle_get_file_if_owned(user_instance, pathname):
    """Methode renvoyant l'instance de la classe File associee a un fichier si l'utilisateur connecte le possede"""

    persistent_data = pickle_get(files_arg=True)
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


def pickle_get(students_arg=False, admins_arg=False, files_arg=False, courses_arg=False, id_dict_arg=False):
    """Fonction permettant de recuperer les classes persistantes du programme
            Seules les classes specifies dans les parametres sont recuperees
    """

    all_students = {}
    all_admins = {}
    all_files = {}
    all_courses = {}
    id_dict = {}

    if students_arg:
        with open("pickle_saves/students.pkl", 'rb') as students_file:
            all_students = pickle.load(students_file)
    if admins_arg:
        with open("pickle_saves/admins.pkl", 'rb') as admins_file:
            all_admins = pickle.load(admins_file)
    if files_arg:
        with open("pickle_saves/files.pkl", 'rb') as files_file:
            all_files = pickle.load(files_file)
    if courses_arg:
        with open("pickle_saves/courses.pkl", 'rb') as courses_file:
            all_courses = pickle.load(courses_file)
    if id_dict_arg:
        with open("pickle_saves/id_dict.pkl", 'rb') as id_dict_file:
            id_dict = pickle.load(id_dict_file)

    return [all_students, all_admins, all_files, all_courses, id_dict]


def pickle_get_instance(name, student=False, admin=False, file=False, course=False):
    """Fonction permettant de recuperer une instance persistante specifique"""

    if student and not admin and not file and not course:
        with open("pickle_saves/students.pkl", 'rb') as students_file:
            all_students = pickle.load(students_file)
            student_instance_id = all_students["name_id_dict"][name]
            student_instance = all_students["objects_dict"][student_instance_id]
            return student_instance
    elif admin and not student and not file and not course:
        with open("pickle_saves/admins.pkl", 'rb') as admin_file:
            all_admins = pickle.load(admin_file)
            admin_instance_id = all_admins["name_id_dict"][name]
            admin_instance = all_admins["objects_dict"][admin_instance_id]
            return admin_instance
    elif file and not student and not admin and not course:
        with open("pickle_saves/files.pkl", 'rb') as file_file:
            all_files = pickle.load(file_file)
            file_instance_id = all_files["name_id_dict"][name]
            file_instance = all_files["objects_dict"][file_instance_id]
            return file_instance
    elif course and not student and not admin and not file:
        with open("pickle_saves/courses.pkl", 'rb') as course_file:
            all_courses = pickle.load(course_file)
            course_instance_id = all_courses["name_id_dict"][name]
            course_instance = all_courses["objects_dict"][course_instance_id]
            return course_instance
    else:
        raise IncorrectUseOfArgumentsException


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
    persistent_data = pickle_get(students_arg=True, admins_arg=True)
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
