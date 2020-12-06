#!/usr/bin/env python3
import cmd
import sys

import cli.reset
import cli.cli_admin
import cli.cli_student
import cli.cli_common
import cli.cli_misc
from classes.exceptions import UnknownPasswordException
from cli.temp_exceptions import ArgumentException, FileNotOwnedException, FileNotFoundException, \
    UnknownUsernameException, ObjectAlreadyExistantException, PasswordNotEqualException, UnknownObjectException, \
    ImpossibleToDeleteUserException


class AdminCli(cmd.Cmd):
    """Cette classe permet de creer une interface en ligne de commande admin personalisee a l'aide du module cmd"""
    intro = "\nBienvenue dans le shell CLI admin du projet python 2TL1_09 :\n\nIntroduire help ou ? pour lister les " \
            "commandes disponibles"

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

        # RAISES
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments
        """

        try:
            if line:
                raise ArgumentException
            all_students, all_admins, all_files, all_courses, id_dict = cli.reset.reset()
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help reset pour plus d'informations sur l'utilisation de reset\n")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\n")
        else:
            cli.cli_misc.pickle_save(all_students, all_admins, all_files, all_courses, id_dict)
            print("La memoire du programme a ete correctement reinitialisee\n")

    @staticmethod
    def do_new(line):
        """
        # NAME
            new  -  creation de nouvelles instances de classes

        # SYNOPSIS
            new {student | admin} <USERNAME> <FULLNAME>
            new {course} <COURSE_NAME> [OPTION]...

        # DESCRIPTION
            Cree une nouvelle instance persistante de la classe specifiee

        # OPTIONS
            --description
                Ajout d'une description au cours

            --teachers
                Ajout d'un ou plusieurs professeurs titulaires au cours

        # AUTHOR
            Ecrit par Nicolas Daxhelet

        # RAISES
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments
        """

        class_to_create = ""
        try:
            class_to_create = line.split()[0]
            if (("student" in class_to_create) ^ ("admin" in class_to_create)) and not ("course" in class_to_create):
                if len(line.split()) == 3:
                    username = line.split()[1]
                    fullname = line.split()[2]
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
                    if "--teachers" in line:
                        teachers_number = int(input("Veuillez entrer le nombre de professeurs titulaires du cours :"))
                        for i in range(teachers_number):
                            teacher_temp = input(f"Veuillez entre le nom du titulaire numero {i} :")
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
            print(f"L'instance {class_to_create} existe deja\n")
        except PasswordNotEqualException:
            print("Les mots de passes entres ne correspondent pas\n")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\n")
        else:
            print(f"L'instance {class_to_create} a correctement ete cree\n")

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
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments

            ImpossibleToDeleteUserException
                L'utilisateur fait partie des utilisateurs initialises par le programme ou
                l'utilisateur correspond a l'utilisateur connecte
        """

        class_to_delete = ""
        try:
            class_to_delete = line.split()[0]
            if (("student" in class_to_delete) ^ ("admin" in class_to_delete)) and not ("course" in class_to_delete):
                if len(line.split()) == 2:
                    username = line.split()[1]
                    if (username in cli.reset.initial_users) or (username == current_user_instance.username):
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
            print(f"L'instance {class_to_delete} n'existe pas\n")
        except ImpossibleToDeleteUserException:
            print(f"Impossible de suprimmer cet utilisateur\n")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\n")
        else:
            print(f"L'instance {class_to_delete} a correctement ete cree\n")

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

        # RAISES
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments
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
            print(f"Une erreur est survenue : {e}\n")

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

        # RAISES
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments
        """

        try:
            course_action = line.split()[0]
            course_name = line.split()[1]
            if "add" in course_action:
                course_attribute = line.split()[2]
                if "teacher" in course_attribute:
                    if len(line.split()) == 3:
                        teacher_name = input("Veuillez entrer le nom du proffesseur a ajouter a la liste des titulaires du "
                                             "cours :")
                        cli.cli_admin.course_add_teacher(course_name, teacher_name)
                    else:
                        raise ArgumentException
                elif "description" in course_attribute:
                    if len(line.split()) == 3:
                        description = input("Veuillez entrer l'intitule du cours :")
                        cli.cli_admin.course_add_description(course_name, description)
                    else:
                        raise ArgumentException
                else:
                    raise ArgumentException
            elif "remove" in course_action:
                course_attribute = line.split()[2]
                if "teacher" in course_attribute:
                    all_teachers = False
                    if (line.split()[3] == "--all") and (len(line.split()) == 4):
                        all_teachers = True
                    if (len(line.split()) == 3) or (line.split()[3] == "--all") and (len(line.split()) == 4):
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
        except Exception as e:
            print(f"Une erreur est survenue : {e}\n")
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

        # RAISES
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments
        """

        try:
            if line != "":
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help exit pour plus d'informations sur l'utilisation de exit\n")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\n")
        else:
            sys.exit("Merci d'avoir utilise la CLI admin du projet python 2TL1_09\n")


class StudentCli(cmd.Cmd):
    """Cette classe permet de creer une interface en ligne de commande personalisee a l'aide du module cmd"""
    intro = "\nBienvenue dans le shell CLI du projet python 2TL1_09 :\n\nIntroduire help ou ? pour lister les " \
            "commandes disponibles"

    @staticmethod
    def do_new():
        pass

    @staticmethod
    def do_del():
        pass

    @staticmethod
    def do_file():
        pass

    @staticmethod
    def do_move():
        pass

    @staticmethod
    def do_open(pathname):
        """
        # NAME
            open  -  ouvre un fichier dans l'editeur de texte de la GUI

        # SYNOPSIS
            open <PATHNAME>

        # DESCRIPTION
            Ouvre le fichier specifie par PATHNAME dans l'editeur de texte de la GUI

        # AUTHOR
            Ecrit par Gregoire Delannoit

        # RAISES
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments
            FileNotOwnedException
                L'utilisateur tente d'acceder a un fichier possede par un autre utilisateur
            FileNotFoundException
                Le programme ne connait pas le fichier specifie par PATHNAME
        """
        try:
            # ### SI L'UTILISATEUR N'A PAS PRECISE DE PATHNAME, pathname = ""
            if not pathname:
                raise ArgumentException
            # ### ICI, C'EST A TOI DE JOUER, J'AI AUCUNE IDEE DE COMMENT FONCTIONNE TA GUI
            # TU DOIS T'ASSURER QUE LE FICHIER QUE L'UTILISATEUR ESSAYE D'OUVRIR APPARTIENT A L'UTILISATEUR !
            #       file_instance = cli.cli_misc.pickle_get_file_if_owned(current_user_instance, pathname)
            # Dans la classe File, il y a une methode open_file(), elle est pas completee mais si tu pense que c'est
            # necessaire, je l'avais creee a vide en me disant que ça te serait peut etre utile pour le cas precis
            # d'une ouverture dans la GUI
        except ArgumentException:
            print("Erreur : les conventions relatives au options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help sort pour plus d'informations sur l'utilisation de sort")
        except FileNotOwnedException:
            print(f"Erreur : le fichier {pathname} appartient a un autre utilisateur\n")
        except FileNotFoundException:
            print(f"Erreur : le fichier {pathname} est introuvable")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\n")

    @staticmethod
    def do_vi():
        pass

    @staticmethod
    def do_sub():
        pass

    @staticmethod
    def do_unsub():
        pass

    @staticmethod
    def do_list():
        pass

    @staticmethod
    def do_sort(line):
        """
        # NAME
            sort  -  trier les fichiers

        # SYNOPSIS
            sort [OPTION]...

        # DESCRIPTION
            Liste les fichiers de l'utilisateur connecte sur base de l'option ou des options specifiees

            Si aucune option n'est specifie, liste l'entierete des fichiers de l'utilisateur

        # OPTIONS
            --tags [TAG]...
                Trie les fichiers de l'utilisateur sur base du ou des tags specifies
                --tags et --course sont mutuellement exclusifs

            --course [COURSE_NAME]
                Trie les fichiers de l'utilisateur sur base du cours specifie
                --course et --tags sont mutuellement exclusifs

        # AUTHOR
            Ecrit par Gregoire Delannoit

        # RAISES
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments
        """

        try:
            # ### Si --tags est dans line (mais pas --course)
            if ("--tags" in line) and not ("--course" in line):
                tags = []
                # OPERATIONS SUR LINE POUR EXTRAIRE TOUS LES TAGS (si il y en a plusieurs)
                # ENREGISTRER CHAQUE TAG COMME UN ELEMENT DE LA VARIABLE LISTE tags
                # PAS OUBLIER QUE SI --tags EST PRECISE MAIS QU'AUCUN TAG NE LE SUIT,
                #       CA DOIT GENERER UNE EXCEPTION ArgumentException
                # PAR EX :
                #       if ([pas d'argument precise a la suite de --tags]):
                #           raise ArgumentException
                content_to_display = cli.cli_student.list_sorted_files_on_tags(tags)

            # ### Si --course est dans line (mais pas --line)
            elif ("--course" in line) and not ("--tags" in line):
                course_name = ""
                # OPERATIONS SUR LINE POUR EXTRAIRE LE NOM DU COURS
                # PAS OUBLIER QUE SI --course EST PRECISE MAIS QU'AUCUN COURSE_NAME NE LE SUIT,
                #       CA DOIT GENERER UNE EXCEPTION ArgumentException
                # PAR EX :
                #       if ([pas d'argument precise a la suite de --course]):
                #           raise ArgumentException
                content_to_display = cli.cli_student.list_sorted_files_on_course(course_name)
            else:
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives au options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help sort pour plus d'informations sur l'utilisation de sort")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\n")
        else:
            # CETTE FONCTION EST PAS ENCORE IMPLEMENTEE AU PROPRE DONC ESSAYE DE VOIR PAR TOI MEME (avec des print).
            # SI content_to_display EST GENERE CORRECTEMENT, ON FERA L'AFFICHAGE AU PROPRE PLUS TARD
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

        # RAISES
            ArgumentException
                L'utilisateur n'a pas respecte les conventions relatives aux options et arguments
        """

        try:
            if line != "":
                raise ArgumentException
        except ArgumentException:
            print("Erreur : les conventions relatives aux options et leurs arguments n'ont pas ete respectees\n",
                  "Entrer la commande help exit pour plus d'informations sur l'utilisation de exit\n")
        except Exception as e:
            print(f"Une erreur est survenue : {e}\n")
        else:
            sys.exit("Merci d'avoir utilise la CLI du projet python 2TL1_09\n")


if __name__ == "__main__":
    try:
        current_user_instance, current_user_is_admin = cli.cli_misc.login()
    except UnknownUsernameException:
        print("Le nom d'utilisateur n'existe pas")
    except UnknownPasswordException:
        print("Le mot de passe est incorrect")
    except Exception as exception:
        print(f"Une erreur est survenue : {exception}\n")
    else:
        if current_user_is_admin:
            AdminCli.prompt = f"({current_user_instance.username}) ##"
            AdminCli().cmdloop()
        else:
            StudentCli.prompt = f"({current_user_instance.username}) >>"
            StudentCli().cmdloop()
