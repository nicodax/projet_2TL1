import pickle
import re

from classes.exceptions import FileNotOwnedException, FileNotFoundException


def specified_options(line, options):
    """Methode permettant d'isoler les options d'une ligne d'argument du module cmd

    PRE :   - line est de type str
            - options est une liste comportant deux elements :
                    * le premier annonce si l'option se trouve dans line et est de type bool
                    * le deuxieme est la sequence de caractere marquant l'option dans line

    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_write dans l'interface
            en ligne de commande cree par le module cmd
    :param options: list
        liste des options possiblement presente dans line
    :return specified_options_dict: dict
        dictionnaire {option : argument}
    """

    specified_options_dict = {}
    for i in options:
        if i[0]:
            try:
                found = re.search(i[1] + "(.+?)" + " --", line).group(1)
                specified_options_dict[i[1]] = found
            except AttributeError:
                found = line.split(i[1])[1]
                specified_options_dict[i[1]] = found
    print(specified_options_dict)
    return specified_options_dict


def if_proprietor_get_file(pathname, user_instance):
    """Methode renvoyant l'instance de la classe File associee a un fichier

    PRE : pathname est de type str
    POST : retourne l'instance de la classe File associee au fichier ssi le fichier
        existe et qu'il appartient a l'utilisateur connecte
    RAISES :    - FileNotFoundException si le fichier n'existe pas sur la memoire locale ou distante
                - FileNotOwnedException si le fichier existe mais n'apartient pas a l'utilisateur connecte

    :param user_instance: object
        utilisateur connecte
    :param pathname: str
        Le chemin d'acces vers le fichier sur la memoire locale ou distante
    :return: object
        L'instance de la classe File associee au fichier
    """

    files = pickle_get_files()
    if pathname in files["name_id_dict"]:
        file_id = files["name_id_dict"][pathname]
        file_instance = files["objects_dict"][file_id]
        if file_id in user_instance.files:
            return file_instance
        else:
            raise FileNotOwnedException
    else:
        raise FileNotFoundException


def pickle_save(all_students=None, all_admins=None, files=None, courses=None):
    """Methode statique permettant d'enregistrer les modifications sur les classes persistantes du programme
            Seules les classes specfiees dans les parametres sont sauvegardees
    """

    if all_students is not None:
        with open("pickle_saves/students.pkl", 'wb') as students_file:
            pickle.dump(all_students, students_file)
    if all_admins is not None:
        with open("pickle_saves/admins.pkl", 'wb') as admins_file:
            pickle.dump(all_admins, admins_file)
    if files is not None:
        with open("pickle_saves/files.pkl", 'wb') as files_file:
            pickle.dump(files, files_file)
    if courses is not None:
        with open("pickle_saves/courses.pkl", 'wb') as courses_file:
            pickle.dump(courses, courses_file)


def pickle_get_students():
    """Methode statique permettant de recuperer les instances persistantes de la classe Student

    :return students : dict
        dictionnaire contenant les instances persistantes de la classe Student
    """

    with open("pickle_saves/students.pkl", 'rb') as students_file:
        all_students = pickle.load(students_file)

    return all_students


def pickle_get_admins():
    """Methode statique permettant de recuperer les instances persistantes de la classe Admin

    :return admins : dict
        dictionnaire contenant les instances persistantes de la classe Admin
    """

    with open("pickle_saves/admins.pkl", 'rb') as admins_file:
        all_admins = pickle.load(admins_file)

    return all_admins


def pickle_get_files():
    """Methode statique permettant de recuperer les instances persistantes de la classe File

    :return files : dict
        dictionnaire contenant les instances persistantes de la classe File
    """

    with open("pickle_saves/files.pkl", 'rb') as files_file:
        files = pickle.load(files_file)

    return files


def pickle_get_courses():
    """Methode statique permettant de recuperer les instances persistantes de la classe Course

    :return courses : dict
        dictionnaire contenant les instances persistantes de la classe Course
    """

    with open("pickle_saves/courses.pkl", 'rb') as courses_file:
        courses = pickle.load(courses_file)

    return courses


def pickle_get_ids():
    """Methode statique permettant de recuperer les valeurs persistantes des identifiants uniques pour
        les classes utilisateurs, File et Course

        :return id_dict : dict
            dictionnaire contenant les valeurs persistantes des identifiants uniques pour
                les classes utilisateurs, File et Course
        """

    with open("pickle_saves/id_dict.pkl", 'rb') as ids_file:
        id_dict = pickle.load(ids_file)

    return id_dict


def pickle_save_ids(id_dict):
    """Methode statique permettant d'enregistrer les modifications sur les identifiants uniques des classes utilisateur
        File et Course
    """

    with open("pickle_saves/id_dict.pkl", 'wb') as ids_file:
        pickle.dump(id_dict, ids_file)
