#!/usr/bin/env python3
import getpass

from classes.course import Course
from classes.exceptions import AlreadyInListException, NotInListException, CommandHasNoArgumentsException, \
    ObjectAlreadyExistantException, PasswordNotEqualException, NumberOfArgumentsException, CannotDeleteUserException, \
    UnknownObjectNameException
from classes.user import Admin, Student
from cli.temp_cli_misc import pickle_get_courses, pickle_save, pickle_save_ids, pickle_get_students, pickle_get_admins, \
    pickle_get_ids, pickle_get_files
from cli.reset import reset


def do_add_teacher(line):
    """
    add_teacher [COURSE_NAME] [TEACHER]

    PRE : line est de type str et correspond a deux sequences de caracteres separees par un espace
                - la premiere sequence (course_name) correspond a l'intitule du cours concerne
                - la deuxieme sequence (teacher) correspond au nom complet du professeur que l'on
                    desire ajouter comme titulaire au cours
    POST : le nom du professeur est indique comme titulaire du cours ssi course_name correspond au nom d'un cours
        connu du programme

    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_mv dans l'interface
            en ligne de commande cree par le module cmd
    """

    course_name = line.split()[0]
    teacher = line.split(f"{course_name}", 1)[1]
    all_courses = pickle_get_courses()
    try:
        course_instance_id = all_courses["name_id_dict"][course_name]
        course_instance = all_courses["objects_dict"][course_instance_id]
        course_instance.add_teacher(teacher)
    except AlreadyInListException:
        print(f"Le professeur {teacher} est deja titulaire du cours {course_name}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        pickle_save(courses=all_courses)
        print(f"Le proffesseur {teacher} est maintenant titulaire du cours {course_name}")


def do_remove_teacher(line):
    """
    remove_teacher [COURSE_NAME] [TEACHER]

    PRE : line est de type str et correspond a deux sequences de caracteres separees par un espace
                - la premiere sequence (course_name) correspond a l'intitule du cours concerne
                - la deuxieme sequence (teacher) correspond au nom complet du professeur que l'on
                    desire retirer de la liste des titulaires
    POST : le nom du professeur est retire de la liste des titulaires du cours ssi course_name correspond
        au nom d'un cours connu du programme

    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_mv dans l'interface
            en ligne de commande cree par le module cmd
    """

    course_name = line.split()[0]
    teacher = line.split()[1:]
    all_courses = pickle_get_courses()
    try:
        course_instance_id = all_courses["name_id_dict"][course_name]
        course_instance = all_courses["objects_dict"][course_instance_id]
        course_instance.remove_teacher(teacher)
    except NotInListException:
        print(f"Le professeur {teacher} n'est pas titulaire du cours {course_name}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        pickle_save(courses=all_courses)
        print(f"Le proffesseur {teacher} n'est maintenant plus titulaire du cours {course_name}")


def do_reset(line):
    """
    reset

    PRE : line est une chaine de caractere vide
    RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

    Methode permettant de reinitialiser la memoire du programme (elle ne contient plus que les root_users)

    :param line: str
        chaine vide car la fonction reset ne demande pas de parametres
    """

    try:
        if line != "":
            raise CommandHasNoArgumentsException
    except CommandHasNoArgumentsException:
        print("La fonction n'accepte aucun argument\nVeuillez reesayer :\n")
    try:
        all_students, all_admins, all_files, all_courses, id_dict = reset()
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        pickle_save_ids(id_dict)
        pickle_save(all_students, all_admins, all_files, all_courses)
        print("La memoire du programme a ete correctement reinitialisee")


def do_new(line):
    """
    new [OPTION=student, admin] [USERNAME] [FULLNAME]
    new [OPTION=course] [NAME] [TEACHER]...

    Methode permettant de creer une nouvelle instance d'une classe. La classe en question est specifiee par l'option

    PRE :   - option est de type str et vaut "student" ou "admin" :
                    * username est de type str et correspond au nom d'utilisateur du futur utilisateur
                    * fullname est de type str et correspond au nom complet du futur utilisateur
                    * il sera demande a l'utilisateur d'entrer deux fois un meme mot de passe de type str
                        avant creation de l'instance
            - option est de type str et vaut "course" :
                    * teacher est de type str et correspond a la liste des noms des professeurs separes par des
                        underscores
    POST : cree l'instance de la classe specifie ssi elle n'existe pas deja
        si option correspond a un utilisateur, le mot de passe doit etre identique les deux fois
    RAISES :    - PasswordNotEqualException si les deux mots de passe entre ne correspondent pas
                - ObjectAlreadyExistantException si le nom de l'objet existe deja

    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_mv dans l'interface
            en ligne de commande cree par le module cmd
    """

    all_students = pickle_get_students()
    all_admins = pickle_get_admins()
    all_courses = pickle_get_courses()
    if (("student" in line) ^ ("admin" in line)) and not ("course" in line):
        try:
            user_name = line.split()[1]
            fullname_list = line.split()[2:]
            fullname = ""
            for i in fullname_list:
                fullname += i + " "
            fullname = fullname[:-1]
            if "student" in line:
                pwd1 = getpass.getpass("Veuillez creer un mot de passe :")
                pwd2 = getpass.getpass("Veuillez confirmer le mot de passe :")
                if pwd1 == pwd2:
                    id_dict = pickle_get_ids()
                    student_instance = Student(user_name, fullname, pwd1, id_dict["user"])
                    id_dict["user"] += 1
                    pickle_save_ids(id_dict)
                    if user_name in all_students["name_id_dict"]:
                        raise ObjectAlreadyExistantException
                    all_students["objects_dict"][student_instance.user_id] = student_instance
                    all_students["name_id_dict"][user_name] = student_instance.user_id
                else:
                    raise PasswordNotEqualException
            if "admin" in line:
                pwd1 = getpass.getpass("Veuillez creer un mot de passe :")
                pwd2 = getpass.getpass("Veuillez confirmer le mot de passe :")
                if pwd1 == pwd2:
                    id_dict = pickle_get_ids()
                    admin_instance = Admin(user_name, fullname, pwd1, id_dict["user"])
                    id_dict["user"] += 1
                    pickle_save_ids(id_dict)
                    if user_name in all_admins["name_id_dict"]:
                        raise ObjectAlreadyExistantException
                    all_admins["objects_dict"][admin_instance.user_id] = admin_instance
                    all_admins["name_id_dict"][user_name] = admin_instance.user_id
                else:
                    raise PasswordNotEqualException
        except ObjectAlreadyExistantException:
            print("Un utilisateur du meme nom existe deja\nVeuillez reessayer avec un autre username :\n")
        except PasswordNotEqualException:
            print("Les mots de passe entres ne correspondent pas\nVeuillez reessayer :\n")
        except NumberOfArgumentsException:
            print("La commande mv demande deux arguments : [CURRENT_PATHNAME] [NEW_PATHNAME]\n")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
        else:
            pickle_save(all_students=all_students, all_admins=all_admins)
            print("L'utilisateur a ete correctement cree\n")
    elif "course" in line and not (("student" in line) or ("admin" in line)):
        try:
            name = line.split()[1]
            teachers = line.split(name + " ", 1)[1]
            teachers = teachers.split("_")
            id_dict = pickle_get_ids()
            course_instance = Course(name, teachers, id_dict["course"])
            id_dict["course"] += 1
            pickle_save_ids(id_dict)
            if name in all_courses["name_id_dict"]:
                raise ObjectAlreadyExistantException
            all_courses["objects_dict"][course_instance.course_id] = course_instance
            all_courses["name_id_dict"][name] = course_instance.course_id
        except ObjectAlreadyExistantException:
            print("Un cours avec le meme intitule existe deja\nVeuillez reessayer avec un autre nom :\n")
        except NumberOfArgumentsException:
            print("La commande mv demande deux arguments : [CURRENT_PATHNAME] [NEW_PATHNAME]\n")
        # except Exception as e:
        # print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
        else:
            pickle_save(courses=all_courses)
            print("Le cours a ete correctement cree\n")
    else:
        str1 = "Les arguments entres sont incorrects : [OPTION] a trois valeurs possibles :"
        str2 = "\nstudent\nadmin\ncourse\nVeuillez reessayer :\n"
        print(str1, str2)


def do_del_admin(line, user_instance):
    """
    del [OPTION=student, admin] [USERNAME]
    del [OPTION=course] [NAME]

    Methode permettant de creer une nouvelle instance d'une classe. La classe en question est specifiee par l'option

    PRE :   - option est de type str et vaut "student" ou "admin" :
                    * username est de type str et correspond au nom d'utilisateur du futur utilisateur
                    * fullname est de type str et correspond au nom complet du futur utilisateur
            - option est de type str et vaut "course" :
                    * teacher est de type str et correspond a la liste des noms des professeurs separes par des
                        underscores
    POST : cree l'instance de la classe specifie ssi elle n'existe pas deja
            - si l'instance est un utilisateur, toutes les instances des fichiers qu'il possede sont supprimees
                et il est desinscrit de tous ses cours
            - si l'instance est un cours, toutes les instances des fichiers qui lui sont associes voient leur
                attribut prive course_id devenir None et tous les etudiants inscrits a ce cours en sont desinscrits

    :param user_instance: object
        utilisateur connecte
    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_mv dans l'interface
            en ligne de commande cree par le module cmd
    """
    all_students = pickle_get_students()
    all_courses = pickle_get_courses()
    all_files = pickle_get_files()
    all_admins = pickle_get_admins()
    if (("student" in line) ^ ("admin" in line)) and not ("course" in line):
        try:
            user_name = line.split()[1]
            if user_name in ["dax", "greg", "daxxra", "TheGregouze", user_instance.username]:
                raise CannotDeleteUserException
            if "student" in line:
                if user_name not in all_students["name_id_dict"]:
                    raise UnknownObjectNameException
                student_instance_id = all_students["name_id_dict"][user_name]
                student_instance = all_students["objects_dict"][student_instance_id]
                file_ids = student_instance.files
                course_ids = student_instance.courses
                if file_ids:
                    for i in file_ids:
                        course_id = all_files["objects_dict"][i].course_id
                        if course_id:
                            course_instance = all_courses["objects_dict"][course_id]
                            course_instance.remove_file(i)
                            all_courses["name_id_dict"][course_id] = course_instance
                        file_pathname = all_files["objects_dict"][i].pathname
                        del all_files["objects_dict"][i]
                        del all_files["name_id_dict"][file_pathname]
                if course_ids:
                    for i in course_ids:
                        course_instance = all_courses["objects_dict"][i]
                        course_instance.remove_student(student_instance_id)
                        all_courses["name_id_dict"][i] = course_instance
                del all_students["objects_dict"][student_instance_id]
                del all_students["name_id_dict"][user_name]
            if "admin" in line:
                if user_name not in all_admins["name_id_dict"]:
                    raise UnknownObjectNameException
                admin_instance_id = all_admins["name_id_dict"][user_name]
                del all_admins["objects_dict"][admin_instance_id]
                del all_admins["name_id_dict"][user_name]
        except UnknownObjectNameException:
            print("Impossible de supprimmer l'utilisateur : le username est inconnu\n")
        except CannotDeleteUserException:
            print("Impossible de supprimmer l'utilisateur : il s'agit soit d'un root_user, soit de l'utilisateur "
                  "connecte\n")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
        else:
            pickle_save(all_students=all_students, all_admins=all_admins, files=all_files, courses=all_courses)
            print("L'utilisateur a ete correctement suprimme\n")
    elif "course" in line and not ("student" in line) or ("admin" in line):
        try:
            name = line.split()[1]
            if name not in all_courses["name_id_dict"]:
                raise UnknownObjectNameException
            course_instance_id = all_courses["name_id_dict"][name]
            course_instance = all_courses["objects_dict"][course_instance_id]
            file_ids = course_instance.files
            student_ids = course_instance.students
            if file_ids:
                for i in file_ids:
                    file_instance = all_files["objects_dict"][i]
                    file_instance.course_id = None
                    all_files["name_id_dict"][i] = file_instance
            if student_ids:
                for i in student_ids:
                    student_instance = all_students["objects_dict"][i]
                    student_instance.remove_course(course_instance_id)
                    all_students["name_id_dict"][i] = student_instance
            del all_courses["objects_dict"][course_instance_id]
            del all_courses["name_id_dict"][name]
        except UnknownObjectNameException:
            print("Impossible de supprimmer le cours : l'intitule est inconnu\n")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
        else:
            pickle_save(all_students=all_students, files=all_files, courses=all_courses)
            print("Le cours a ete correctement supprimme\n")
    else:
        str1 = "Les arguments entres sont incorrects : [OPTION] a trois valeurs possibles :"
        str2 = "\nstudent\nadmin\ncourse\nVeuillez reessayer :\n"
        print(str1, str2)
