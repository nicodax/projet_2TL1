#!/usr/bin/env python3
import getpass
import pickle

from cli.exceptions import UnknownUsernameException, FileNotOwnedException, FileNotFoundException, \
    IncorrectUseOfArgumentsException


def users_terminal_display(content_to_display):
    """
    PRE: content_to_display est de type dict
    POST: affiche et met en forme les informations contenues dans content_to_display (relatif a des utilisateurs)
    """
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
    """
    PRE: content_to_display est de type dict
    POST: affiche et met en forme les informations contenues dans content_to_display (relatif a des fichiers)
    """
    id_max_len = 3
    course_name_max_len = 5
    script_max_len = 5
    pathname_max_len = 100
    print("id    cours  script  pathname                                                                              "
          "                etiquettes")
    print("---------------------------------------------------------------------------------------------------------"
          "--------------------------------------------------------------------")
    for i in content_to_display:
        add_to_id = ""
        spaces_to_add_to_id = id_max_len - len(str(i["file_id"]))
        for j in range(spaces_to_add_to_id):
            add_to_id += " "
        add_to_course_name = ""
        spaces_to_add_to_course_name = course_name_max_len - len(str(i["course_name"]))
        for j in range(spaces_to_add_to_course_name):
            add_to_course_name += " "
        add_to_script = ""
        spaces_to_add_to_script = script_max_len - len(str(i["script"]))
        for j in range(spaces_to_add_to_script):
            add_to_script += " "
        add_to_pathname = ""
        spaces_to_add_to_pathname = pathname_max_len - len(str(i["pathname"]))
        for j in range(spaces_to_add_to_pathname):
            add_to_pathname += " "
        print(f" {i['file_id']}{add_to_id}  {i['course_name']}{add_to_course_name}  {i['script']}{add_to_script}  ",
              f"{i['pathname']}{add_to_pathname}  {i['tags']}")
    print("\n")


def courses_terminal_display(content_to_display):
    """
    PRE: content_to_display est de type dict
    POST: affiche et met en forme les informations contenues dans content_to_display (relatif a des cours)
    """
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
    """
    PRE:    - user_instance est l'instance de Student correspondant a l'utilisateur connecte
            - pathname est de type str
    POST: retourne l'instance de la classe File identifie a pathname ssi elle appartient a user_instance
    RAISES:     - FileNotOwnedException si l'instance de File existe mais n'appartient pas a user_instance
                - FileNotFoundException si l'instance de File n'existe pas
    """

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
    PRE: students_arg, admins_arg, files_arg, courses_arg et id_dict_arg sont de type bool
    POST: retourne une liste contenant des dictionnaires a des index precis
                - si students_arg == True, all_students se trouve a l'index 0
                - si admins_arg == True, all_admins se trouve a l'index 1
                - si files_arg == True, all_files se trouve a l'index 2
                - si courses_arg == True, all_courses se trouve a l'index 3
                - si id_dict_arg == True, id_dict se trouve a l'index 4
            Plusieurs arguments peuvent valoir True en même temps
            chaque dictionnaire correspond a l'entierete des instances persistantes du programme d'une classe specifique
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
    """
    PRE:    - name est de type str
            - student, admin, file et course sont de type bool
    POST: retourne l'instance de la classe specifie par l'unique argument valant True et identifie par name
    RAISES: IncorrectUseOfArgumentsException si plusieurs arguments ont la valeur True
    """

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
    """
    PRE: all_students, all_admins, all_files, all_courses et id_dict sont soit de type dict soit None
    POST: enregistre chaque dictionnaire passe en argument
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
    """
    PRE:
    POST: permet de se connecter a un compte utilisateur
    """

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
