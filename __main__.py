#!/usr/bin/env python3
import cmd
import os
import sys

import cli.cli_admin
import cli.cli_common
import cli.cli_misc
import cli.cli_student
import cli.reset
from classes.exceptions import UnknownPasswordException, AlreadyInListException, NotInListException
from cli.exceptions import ArgumentException, FileNotOwnedException, FileNotFoundException, \
    UnknownUsernameException, ObjectAlreadyExistantException, PasswordNotEqualException, UnknownObjectException, \
    ImpossibleToDeleteUserException, InexistantDirectoryException


class AdminCli(cmd.Cmd):
    """Cette classe permet de creer une interface en ligne de commande admin personalisee a l'aide du module cmd"""
    intro = "\nBienvenue dans le shell CLI admin du projet python 2TL1_09 :\n\nIntroduire help ou ? pour lister les " \
            "commandes disponibles\n"

    @staticmethod
    def do_reset(line):
        """
        # NAME
            reset  -  reinitialise la memoire du programme

        # SYNOPSIS
            reset

        # DESCRIPTION
            Reinitialise la memoire du programme.
                Elle ne contiendra plus que les utilisateurs et les cours d'origine

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            if line:
                raise ArgumentException
            all_students, all_admins, all_files, all_courses, id_dict = cli.reset.reset()
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help reset pour plus d'informations sur l'utilisation de reset\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            cli.cli_misc.pickle_save(all_students, all_admins, all_files, all_courses, id_dict)
            print("La memoire du programme a ete correctement reinitialisee")
            sys.exit("Merci d'avoir utilise la CLI admin du projet python 2TL1_09\n")

    @staticmethod
    def do_new(line):
        """
        # NAME
            new  -  creation de nouvelles instances de classes

        # SYNOPSIS
            new {student | admin} <USERNAME> <FULLNAME>
            new {course} <COURSE_NAME> [OPTION]...

            username ne peut pas comporter d'espaces

        # DESCRIPTION
            Cree une nouvelle instance persistante de la classe specifiee

        # OPTIONS
            --description
                Ajout d'une description au cours

            --teachers
                Ajout d'un ou plusieurs professeurs titulaires au cours

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            class_to_create = line.split()[0]
            if (("student" in class_to_create) ^ ("admin" in class_to_create)) and not ("course" in class_to_create):
                if len(line.split()) >= 3:
                    username = line.split()[1]
                    fullname_list = line.split()[2:]
                    fullname = ""
                    for i in fullname_list:
                        fullname += i + " "
                    fullname = fullname[:-1]
                    if "student" in class_to_create:
                        cli.cli_admin.new_student(username, fullname)
                    else:
                        cli.cli_admin.new_admin(username, fullname)
                else:
                    raise ArgumentException
            elif "course" in class_to_create and not (("student" in class_to_create) or ("admin" in class_to_create)):
                course_name = line.split()[1]
                number_of_arguments = 2
                description = ""
                teachers = []
                if "--description" in line:
                    number_of_arguments += 1
                if "--teachers" in line:
                    number_of_arguments += 1
                if len(line.split()) == number_of_arguments:
                    if "--description" in line:
                        description = input(f"Veuillez entrer une description pour le cours {course_name} :")
                        if description == "":
                            raise ArgumentException
                    if "--teachers" in line:
                        teachers_number = input("Veuillez entrer le nombre de professeurs titulaires du cours :")
                        if not teachers_number.isnumeric():
                            raise ArgumentException
                        for i in range(int(teachers_number)):
                            teacher_temp = input(f"Veuillez entrer le nom du titulaire numero {i + 1} :")
                            if teacher_temp == "":
                                raise ArgumentException
                            teachers.append(teacher_temp)
                    cli.cli_admin.new_course(course_name, teachers, description)
                else:
                    raise ArgumentException
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help new pour plus d'informations sur l'utilisation de new\n")
        except ObjectAlreadyExistantException:
            print("Erreur : L'instance de classe existe deja\n")
        except PasswordNotEqualException:
            print("Erreur : Les mots de passes entres ne correspondent pas\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            print("L'instance de classe a correctement ete cree\n")

    @staticmethod
    def do_del(line):
        """
        # NAME
            del  -  suppression d'instances de classes

        # SYNOPSIS
            del {student | admin} <USERNAME>
            del {course} <COURSE_NAME>

        # DESCRIPTION
            Supprime l'instance de classe persistante specifiee

        # AUTHOR
            Ecrit par Nicolas Daxhelet

        # RAISES
            ImpossibleToDeleteUserException
                L'utilisateur fait partie des utilisateurs initialises par le programme ou
                l'utilisateur correspond a l'utilisateur connecte
        """

        try:
            class_to_delete = line.split()[0]
            if (("student" in class_to_delete) ^ ("admin" in class_to_delete)) and not ("course" in class_to_delete):
                if len(line.split()) == 2:
                    username = line.split()[1]
                    if (username in cli.reset.initial_students) or (username in cli.reset.initial_admins) or \
                            (username == current_user_instance.username):
                        raise ImpossibleToDeleteUserException
                    if "student" in class_to_delete:
                        cli.cli_admin.delete_student(username)
                    else:
                        cli.cli_admin.delete_admin(username)
                else:
                    raise ArgumentException
            elif "course" in class_to_delete and not (("student" in class_to_delete) or ("admin" in class_to_delete)):
                course_name = line.split()[1]
                if len(line.split()) == 2:
                    cli.cli_admin.delete_course(course_name)
                else:
                    raise ArgumentException
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help del pour plus d'informations sur l'utilisation de del\n")
        except UnknownObjectException:
            print("Erreur : L'instance de classe n'existe pas\n")
        except ImpossibleToDeleteUserException:
            print("Erreur : Impossible de suprimmer cet utilisateur\n")
        except Exception as e:
            print(f"Erreur : Une erreur est survenue : {e}\n")
        else:
            print("L'instance de classe a correctement ete supprimee\n")

    @staticmethod
    def do_list(line):
        """
        # NAME
            list  -  liste des instances de classes persistantes

        # SYNOPSIS
            list {users} [OPTION]...
            list {courses}

        # DESCRIPTION
            Liste les instances persistantes de la classe specifiee

            list users
                Sans preciser d'option, list affiche les utilisateurs etudiants

        # OPTIONS
            --all
                Liste l'entierete des utilisateurs
                --all et --admins sont mutuellement exclusifs

            --admins
                Liste les utilisateurs administrateurs
                --admins et --all sont mutuellement exclusifs

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            class_to_list = line.split()[0]
            if "users" in class_to_list and not ("courses" in class_to_list):
                if "--all" in line and not ("--admins" in line):
                    if len(line.split()) == 2:
                        cli.cli_common.list_all_students()
                        cli.cli_admin.list_all_admins()
                    else:
                        raise ArgumentException
                elif "--admins" in line and not ("--all" in line):
                    if len(line.split()) == 2:
                        cli.cli_admin.list_all_admins()
                    else:
                        raise ArgumentException
                elif len(line.split()) == 1:
                    cli.cli_common.list_all_students()
                else:
                    raise ArgumentException
            elif "courses" in class_to_list and not ("users" in class_to_list) and (len(line.split()) == 1):
                cli.cli_common.list_all_courses()
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help list pour plus d'informations sur l'utilisation de list\n")
        except Exception as e:
            print(f"Erreur : {e}\n")

    @staticmethod
    def do_course(line):
        """
        # NAME
            course  -  Ajoute ou supprime des proffesseurs titulaires ou l'intitule du cours

        # SYNOPSIS
            course <COURSE_NAME> {add} {teacher | description}
            course <COURSE_NAME> {remove} {teacher | description} [OPTION]

        # DESCRIPTION
            Liste les instances persistantes de la classe specifiee

            list users
                Sans preciser d'option, list affiche les utilisateurs etudiants

        # OPTIONS
            --all
                Supprime l'entierete des proffesseurs titulaires
                --all ne peut s'emplyer qu'avec course remove teacher

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            course_action = line.split()[1]
            course_name = line.split()[0]
            if "add" in course_action:
                course_attribute = line.split()[2]
                if "teacher" in course_attribute:
                    if len(line.split()) == 3:
                        teacher_name = input("Veuillez entrer le nom du proffesseur a ajouter a la liste des"
                                             "titulaires du cours :")
                        if teacher_name == "":
                            raise ArgumentException
                        cli.cli_admin.course_add_teacher(course_name, teacher_name)
                    else:
                        raise ArgumentException
                elif "description" in course_attribute:
                    if len(line.split()) == 3:
                        description = input("Veuillez entrer l'intitule du cours :")
                        if description == "":
                            raise ArgumentException
                        cli.cli_admin.course_add_description(course_name, description)
                    else:
                        raise ArgumentException
                else:
                    raise ArgumentException
            elif "remove" in course_action:
                course_attribute = line.split()[2]
                if "teacher" in course_attribute:
                    all_teachers = False
                    if (len(line.split()) == 4) and (line.split()[3] == "--all"):
                        all_teachers = True
                        teacher_name = None
                        cli.cli_admin.course_remove_teacher(course_name, teacher_name, all_teachers)
                    elif (len(line.split()) == 3) or ((line.split()[3] == "--all") and (len(line.split()) == 4)):
                        teacher_name = input("Veuillez entrer le nom du proffesseur a retirer de la liste des "
                                             "titulaires du cours :")
                        cli.cli_admin.course_remove_teacher(course_name, teacher_name, all_teachers)
                    else:
                        raise ArgumentException
                elif "description" in course_attribute:
                    if len(line.split()) == 3:
                        cli.cli_admin.course_remove_description(course_name)
                    else:
                        raise ArgumentException
                else:
                    raise ArgumentException
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help course pour plus d'informations sur l'utilisation de course\n")
        except AlreadyInListException:
            print("Le cours possede deja un des attributs specifies\n")
        except NotInListException:
            print("Le cours ne possede pas un des attributs specifies\n")
        except UnknownObjectException:
            print("Erreur : L'instance de classe n'existe pas\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            print("L'operation a ete effectuee avec succes\n")

    @staticmethod
    def do_exit(line):
        """
        # NAME
            exit  -  Deconnection de l'utilisateur

        # SYNOPSIS
            exit

        # DESCRIPTION
            Termine la session de l'utilisateur et ferme le programme

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            if line != "":
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help exit pour plus d'informations sur l'utilisation de exit\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            sys.exit("Merci d'avoir utilise la CLI admin du projet python 2TL1_09\n")


class StudentCli(cmd.Cmd):
    """Cette classe permet de creer une interface en ligne de commande personalisee a l'aide du module cmd"""
    intro = "\nBienvenue dans le shell CLI du projet python 2TL1_09 :\n\nIntroduire help ou ? pour lister les " \
            "commandes disponibles"

    @staticmethod
    def do_new(line):
        """
        # NAME
            new  -  cree un fichier

        # SYNOPSIS
            new <file> <PATHNAME> [OPTION]...

        # DESCRIPTION
            Cree un fichier et ajoute ce fichier a la liste des fichiers connus du programme
                Si ce fichier existe deja sur la memoire, il est simplement ajoute a la liste des fichiers connus
                du programme

        #OPTIONS
            --script
                Precise que le fichier est un script

            --no_course
                Precise que le fichier ne traite d'aucun cours

            --tags
                Ajoute une (ou plusieurs) etiquettes au fichier

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            if line.split()[0] != "file":
                raise ArgumentException
            number_of_args = 2
            if "--script" in line:
                number_of_args += 1
            if "--no_course" in line:
                number_of_args += 1
            if "--tags" in line:
                number_of_args += 1
            if len(line.split()) == number_of_args:
                persistent_data = cli.cli_misc.pickle_get(files_arg=True, courses_arg=True)
                all_files = persistent_data[2]
                all_courses = persistent_data[3]
                pathname = line.split()[1]
                if pathname in all_files["name_id_dict"]:
                    raise ObjectAlreadyExistantException
                course_id = None
                script = False
                tags = None
                directory_pathname = os.path.dirname(pathname)
                if os.path.isdir(directory_pathname):
                    if "--no_course" not in line:
                        course_name = input("Veuillez entrer le code du cours a associer au fichier:")
                        if course_name in all_courses["name_id_dict"]:
                            course_id = all_courses["name_id_dict"][course_name]
                        else:
                            raise UnknownObjectException
                    if "--script" in line:
                        script = True
                    if "--tags" in line:
                        number_of_tags = input("Veuillez entrer le nombre d'etiquettes a coller au fichier :")
                        if not number_of_tags.isnumeric():
                            raise ArgumentException
                        tags = []
                        for i in range(int(number_of_tags)):
                            tag = input(f"Veuillez entrer l'etiquette numero {i + 1} :")
                            if tag == "":
                                raise ArgumentException
                            tags.append(tag)
                    cli.cli_student.new_file(pathname, script, course_id, tags, current_user_instance)
                else:
                    raise InexistantDirectoryException
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help new pour plus d'informations sur l'utilisation de new\n")
        except InexistantDirectoryException:
            print("Erreur : Le chemin specifie pour le fichier a creer n'existe pas\n")
        except UnknownObjectException:
            print("Erreur : Le cours n'existe pas\n")
        except ObjectAlreadyExistantException:
            print("Erreur : Le fichier est deja connu du programme:\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            print("Le fichier est maintenant connu du programme\n")

    @staticmethod
    def do_del(line):
        """
        # NAME
            del  -  suprimme un fichier

        # SYNOPSIS
            del <file> <PATHNAME>

        # DESCRIPTION
            Suprimme un fichier de la liste des fichiers connus du programme et de la memoire

        # AUTHOR
            Ecrit par Nicolas Daxhelet

        # RAISES
            FileNotOwnedException
                L'utilisateur tente d'acceder a un fichier possede par un autre utilisateur
            FileNotFoundException
                Le programme ne connait pas le fichier specifie par PATHNAME
        """

        try:
            if line.split()[0] != "file":
                raise ArgumentException
            if len(line.split()) == 2:
                pathname = line.split()[1]
                file_instance = cli.cli_misc.pickle_get_file_if_owned(current_user_instance, pathname)
                cli.cli_student.delete_file(file_instance, current_user_instance)
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help del pour plus d'informations sur l'utilisation de del\n")
        except FileNotOwnedException:
            print("Erreur : Le fichier ne vous appartient pas\n")
        except FileNotFoundException:
            print("Erreur : Le fichier n'existe pas\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            print("Le fichier a correctement ete suprimme\n")

    @staticmethod
    def do_file(line):
        """
        # NAME
            file  -  effectue des modifications sur les proprietes d'un fichier

        # SYNOPSIS
            file <PATHNAME> {script} {True | False}
            file <PATHNAME> {add} {course | tag}
            file <PATHNAME> {remove} {course | tag} [OPTION]

        # DESCRIPTION
            Effectues des modifications sur les proprietes d'un fichier connu du programme

        # OPTIONS
            --all
                Supprime l'entierete des etiquettes du fichier
                --all ne peut s'emplyer qu'avec file remove tag

        # AUTHOR
            Ecrit par Nicolas Daxhelet

        # RAISES
            FileNotOwnedException
                L'utilisateur tente d'acceder a un fichier possede par un autre utilisateur
            FileNotFoundException
                Le programme ne connait pas le fichier specifie par PATHNAME
        """

        try:
            pathname = line.split()[0]
            cli.cli_misc.pickle_get_file_if_owned(current_user_instance, pathname)
            if "script" in line.split()[1]:
                if len(line.split()) == 3:
                    script = line.split()[2]
                    if script == 'True':
                        script = True
                    elif script == 'False':
                        script = False
                    else:
                        raise ArgumentException
                    cli.cli_student.file_change_script_attribute(pathname, script)
                else:
                    raise ArgumentException
            elif "add" in line.split()[1]:
                if len(line.split()) == 3:
                    if "course" in line.split()[2]:
                        course_name = input("Veuillez entrer le cours a associer au fichier :")
                        cli.cli_student.file_add_course(pathname, course_name)
                    elif "tag" in line.split()[2]:
                        tag_number = input("Veuillez entrer le nombre d'etiquettes a associer au fichier :")
                        if not tag_number.isnumeric():
                            raise ArgumentException
                        tags = []
                        for i in range(int(tag_number)):
                            tag = input(f"Veuillez entrer l'etiquette numero {i + 1} :")
                            if tag == "":
                                raise ArgumentException
                            tags.append(tag)
                        cli.cli_student.file_add_tag(pathname, tags)
                    else:
                        raise ArgumentException
                else:
                    raise ArgumentException
            elif "remove" in line.split()[1]:
                if "course" in line.split()[2]:
                    cli.cli_student.file_remove_course(pathname)
                elif "tag" in line.split()[2]:
                    all_tags = False
                    if (len(line.split()) == 4) and (line.split()[3] == "--all"):
                        all_tags = True
                    if (len(line.split()) == 3) or ((line.split()[3] == "--all") and (len(line.split()) == 4)):
                        tag = []
                        if not all_tags:
                            tag = input("Veuillez entrer l'etiquette a retirer du fichier :")
                            if tag == "":
                                raise ArgumentException
                        cli.cli_student.file_remove_tag(pathname, tag)
                    else:
                        raise ArgumentException
                else:
                    raise ArgumentException
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives au options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help file pour plus d'informations sur l'utilisation de file\n")
        except FileNotOwnedException:
            print("Erreur : le fichier appartient a un autre utilisateur\n")
        except FileNotFoundException:
            print("Erreur : le fichier est introuvable\n")
        except AlreadyInListException:
            print("Erreur : le fichier possede deja au moins un des attributs specifies\n")
        except NotInListException:
            print("Erreur : le fichier ne possede pas au moins un des attributs specifies\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            print("L'operation a ete effectuee avec succes\n")

    @staticmethod
    def do_move(line):
        """
        # NAME
            move  -  deplace un fichier

        # SYNOPSIS
            move <CURRENT_PATHNAME> <NEW_PATHNAME>

        # DESCRIPTION
            Deplace un fichier sur la memoire

        # AUTHOR
            Ecrit par Nicolas Daxhelet

        # RAISES
            FileNotOwnedException
                L'utilisateur tente d'acceder a un fichier possede par un autre utilisateur
            FileNotFoundException
                Le programme ne connait pas le fichier specifie par PATHNAME
        """

        try:
            if len(line.split()) == 2:
                current_pathname = line.split()[0]
                new_pathname = line.split()[1]
                cli.cli_misc.pickle_get_file_if_owned(current_user_instance, current_pathname)
                cli.cli_student.move_file(current_pathname, new_pathname)
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives au options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help sort pour plus d'informations sur l'utilisation de sort\n")
        except FileNotOwnedException:
            print(f"Erreur : le fichier appartient a un autre utilisateur\n")
        except FileNotFoundException:
            print(f"Erreur : le fichier est introuvable\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            os.rename(current_pathname, new_pathname)
            print("Le fichier a correctement ete deplace\n")

    @staticmethod
    def do_vi(pathname):
        """
        # NAME
            vi  -  ouvre un fichier dans l'editeur de texte vi

        # SYNOPSIS
            vi <PATHNAME>

        # DESCRIPTION
            Ouvre le fichier specifie par PATHNAME dans l'editeur de texte vi

        # AUTHOR
            Ecrit par Nicolas Daxhelet

        # RAISES
            FileNotOwnedException
                L'utilisateur tente d'acceder a un fichier possede par un autre utilisateur
            FileNotFoundException
                Le programme ne connait pas le fichier specifie par PATHNAME
        """

        try:
            if not pathname:
                raise ArgumentException
            cli.cli_misc.pickle_get_file_if_owned(current_user_instance, pathname)
            cli.cli_student.open_file_in_vi(pathname)
        except ArgumentException:
            print("Erreur : les conventions relatives au options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help vi pour plus d'informations sur l'utilisation de vi\n")
        except FileNotOwnedException:
            print(f"Erreur : le fichier appartient a un autre utilisateur\n")
        except FileNotFoundException:
            print(f"Erreur : le fichier est introuvable\n")
        except FileExistsError:
            print(f"Erreur : Le fichier n'existe pas")
        except IOError:
            print('Erreur : IO')
        except Exception as e:
            print(f"Erreur : {e}\n")

    @staticmethod
    def do_sub(course_name):
        """
        # NAME
            sub  -  inscrit l'utilisateur a un cours

        # SYNOPSIS
            sub <COURSE_NAME>

        # DESCRIPTION
            Inscrit l'utilisateur au cours specifie

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            if not course_name:
                raise ArgumentException
            cli.cli_student.subscribe_user_to_course(course_name, current_user_instance)
        except ArgumentException:
            print("Erreur : les conventions relatives au options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help sub pour plus d'informations sur l'utilisation de sub\n")
        except AlreadyInListException:
            print("Erreur : Vous etes deja inscrit a ce cours\n")
        except UnknownObjectException:
            print("Erreur : le cours spécifié n'existe pas\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            print("Vous avez ete correctement inscrit au cours")

    @staticmethod
    def do_unsub(course_name):
        """
        # NAME
            unsub  -  desinscrit l'utilisateur d'un cours

        # SYNOPSIS
            unsub <COURSE_NAME>

        # DESCRIPTION
            Desinscrit l'utilisateur du cours specifie

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            if not course_name:
                raise ArgumentException
            cli.cli_student.unsubscribe_user_from_course(course_name, current_user_instance)
        except ArgumentException:
            print("Erreur : les conventions relatives au options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help sub pour plus d'informations sur l'utilisation de sub\n")
        except UnknownObjectException:
            print("Erreur : le cours spécifié n'existe pas\n")
        except NotInListException:
            print("Vous n'etes pas inscrit a ce cours\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            print("Vous avez ete correctement desinscrit du cours")

    @staticmethod
    def do_list(line):
        """
        # NAME
            list  -  liste des instances de classes persistantes

        # SYNOPSIS
            list {users}
            list {courses} [OPTION]
            list {files}

        # DESCRIPTION
            Liste les instances persistantes de la classe specifiee

            list courses
                Sans preciser d'option, list affiche tous les cours

        # OPTIONS
            --subbed
                Liste les cours auxquels l'utilisateur est inscrit
                --subbed ne peut s'utiliser qu'avec list courses

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            class_to_list = line.split()[0]
            if "users" in class_to_list and not ("courses" in class_to_list) and not ("files" in class_to_list):
                if len(line.split()) == 1:
                    cli.cli_common.list_all_students()
                else:
                    raise ArgumentException
            elif "courses" in class_to_list and not ("users" in class_to_list) and not ("files" in class_to_list):
                if "--subbed" in line:
                    if len(line.split()) == 2:
                        cli.cli_student.list_subbed_courses(current_user_instance)
                else:
                    if len(line.split()) == 1:
                        cli.cli_common.list_all_courses()
            elif "files" in class_to_list and not ("users" in class_to_list) and not ("courses" in class_to_list):
                if len(line.split()) == 1:
                    content_to_display = cli.cli_student.list_owned_files(current_user_instance)
                    cli.cli_misc.files_terminal_display(content_to_display)
                else:
                    raise ArgumentException
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help list pour plus d'informations sur l'utilisation de list\n")
        except Exception as e:
            print(f"Erreur : {e}\n")

    @staticmethod
    def do_sort(line):
        """
        # NAME
            sort  -  trier les fichiers

        # SYNOPSIS
            sort {on_tags | on_courses}

        # DESCRIPTION
            Liste les fichiers de l'utilisateur connecte sur base de l'option ou des options specifiees

            Si le parametre on_tags est declare, les fichiers de l'utilisateur connecte sont tries sur base
                des etiquettes specifiees.

            Si le parametre on_courses est declare, les fichiers de l'utilisateur connecte sont tries sur base
                des cours specifies.


        # AUTHOR
            Ecrit par Gregoire Delannoit
        """

        try:
            if ("on_tags" in line) and not ("on_course" in line) and (len(line.split()) == 1):
                number_of_tags = int(input("Veuillez entrer le nombre d'etiquettes recherchees :"))
                tags_research = []
                for i in range(number_of_tags):
                    course_name = input("Veuillez entrer l'etiquette :")
                    tags_research.append(course_name)
                content_to_display = cli.cli_student.list_sorted_files_on_tags(tags_research, current_user_instance)
            elif ("on_course" in line) and not ("on_tags" in line) and (len(line.split()) == 1):
                number_of_courses = int(input("Veuillez entrer le nombre de cours recherches :"))
                courses_research = []
                for i in range(number_of_courses):
                    course_name = input("Veuillez entrer le code du cours :")
                    courses_research.append(course_name)
                content_to_display = cli.cli_student.list_sorted_files_on_course(courses_research,
                                                                                 current_user_instance)
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives au options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help sort pour plus d'informations sur l'utilisation de sort\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            cli.cli_misc.files_terminal_display(content_to_display)

    @staticmethod
    def do_exit(line):
        """
        # NAME
            exit  -  Deconnection de l'utilisateur

        # SYNOPSIS
            exit

        # DESCRIPTION
            Termine la session de l'utilisateur et ferme le programme

        # AUTHOR
            Ecrit par Nicolas Daxhelet
        """

        try:
            if line != "":
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help exit pour plus d'informations sur l'utilisation de exit\n")
        except Exception as e:
            print(f"Erreur : {e}\n")
        else:
            sys.exit("Merci d'avoir utilise la CLI du projet python 2TL1_09\n")


if __name__ == "__main__":
    try:
        current_user_instance, current_user_is_admin = cli.cli_misc.login()
    except UnknownUsernameException:
        print("Le nom d'utilisateur n'existe pas\n")
    except UnknownPasswordException:
        print("Le mot de passe est incorrect\n")
    except Exception as exception:
        print(f"Une erreur est survenue : {exception}\n")
    else:
        if current_user_is_admin:
            AdminCli.prompt = f"({current_user_instance.username}) ##"
            AdminCli().cmdloop()
        else:
            StudentCli.prompt = f"({current_user_instance.username}) >>"
            StudentCli().cmdloop()
