#!/usr/bin/env python3
import cmd
import getpass

from classes.exceptions import UnknownPasswordException
from cli.temp_cli_admin import do_add_teacher, do_remove_teacher, do_reset, do_new, do_del_admin
from cli.temp_cli_misc import pickle_get_students, pickle_get_admins
from cli.temp_cli_student import do_del_student, do_mv, do_touch, do_cat, do_write, do_append, do_vi, \
    do_my_files, do_list_courses, do_my_courses, do_sub, do_unsub, do_specify_course, do_unspecify_course, do_list_users


class AdminCli(cmd.Cmd):
    """Cette classe permet de creer une interface en ligne de commande admin personalisee a l'aide du module cmd"""
    intro = "Bienvenue dans le shell CLI admin du projet python 2TL1_09 :\n\nIntroduire help ou ? pour lister les " \
            "commandes disponibles\n\n"

    @staticmethod
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
        do_add_teacher(line)

    @staticmethod
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
        do_remove_teacher(line)

    @staticmethod
    def do_reset(line):
        """
        reset

        PRE : line est une chaine de caractere vide
        RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

        Methode permettant de reinitialiser la memoire du programme (elle ne contient plus que les root_users)

        :param line: str
            chaine vide car la fonction reset ne demande pas de parametres
        """
        do_reset(line)

    @staticmethod
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
        do_new(line)

    @staticmethod
    def do_del(line):
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

        :param line: str
            La ligne d'arguments introduite a la suite de l'appel de la fonction do_mv dans l'interface
                en ligne de commande cree par le module cmd
        """
        do_del_admin(line, user_instance)

    @staticmethod
    def do_list_users(usertype):
        """
        list_users [USERTYPE=all, students, admins]

        Methode permettant de lister les utilisateurs connus du programme

        PRE : usertype est de type str et peut correspondre a trois valeurs differentes (all, students, admins)
        POST : liste en console la liste des utilisateurs demandes
            ssi usertype correspond a une des trois valeurs admises

        :param usertype: str
            correspond au type d'utilisateur a lister : all, students, admins
        """
        do_list_users(usertype)

    @staticmethod
    def do_list_courses(line):
        """
        courses

        PRE : line est une chaine de caractere vide
        RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

        Methode permettant de lister les cours connus du programme

        :param line: str
            chaine vide car la fonction reset ne demande pas de parametres
        """

        do_list_courses(line)


class Cli(cmd.Cmd):
    """Cette classe permet de creer une interface en ligne de commande personalisee a l'aide du module cmd"""
    intro = "Bienvenue dans le shell CLI du projet python 2TL1_09 :\n\nIntroduire help ou ? pour lister les " \
            "commandes disponibles\n\n"

    @staticmethod
    def do_del(pathname):
        """
        del [PATHNAME]

        Methode permettant de supprimer un fichier a la fois des donnes de fonctionnement du programme et
            de la memoire locale ou distante

        PRE : pathname est de type str et correspond au pathname du fichier a supprimer
        POST :  - le fichier est suprimme du programme et de la memoire locale ou distante ssi pathname correspond
                    au pathname d'un fichier existant et connu du programme et ssi l'utilisateur connecte possede
                    ce fichier
                - le file_id du fichier est retiré des listes files des instances des classes Student et Course
                    appropriees ssi elles existent

        :param pathname: str
            Correspond au pathname du fichier a supprimer sur la memoire locale ou distante
        """
        do_del_student(pathname, user_instance)

    @staticmethod
    def do_mv(line):
        """
        mv [CURRENT_PATHNAME] [NEW_PATHNAME]

        Methode permettant de deplacer et/ou de renommer un fichier sur la memoire locale ou distante
            et de mettre a jour les donnees de fonctionnoment du programme en consequence

        PRE : line est de type str et correspond a deux sequences de caracteres separees par un espace
                    - la premiere sequence (current_pathname) correspond au pathname
                        actuel du fichier a deplacer/renommer
                    - la deuxieme sequence (new_pathname) correspond au pathname
                        desire pour le fichier a deplacer/renommer
        POST : le fichier est deplace/renomme sur la memoire locale ou distante ssi :
                    - current_pathname correspond au pathname d'un fichier existant et connu du programme
                    - le chemin d'acces specifie par pathname correspond a un chemin existant sur la memoire
                        locale ou distante
        RAISES : NumberOfArgumentsException si l'utilisateur n'entre pas exactement deux arguments apres l'appel
            de la commande

        :param line: str
            La ligne d'arguments introduite a la suite de l'appel de la fonction do_mv dans l'interface
                en ligne de commande cree par le module cmd
        """
        do_mv(line, user_instance)

    @staticmethod
    def do_sort():
        pass

    @staticmethod
    def do_open(pathname):
        pass

    @staticmethod
    def do_touch(line):
        """
        touch [PATHNAME] [OPTION]...

        OPTIONS :
                --course [COURSENAME]
                    permet d'assigner le fichier a un cours
                --tag [TAG]...
                    permet d'assigner un ou plusieurs tags au fichier
                --script [BOOL]
                    permet de signifier que le contenu du fichier est un script


        Methode permettant de creer un fichier vide a la fois pour le programme et sur la memoire locale ou distante

        PRE :   - pathname est de type str et correspond au pathname du fichier a creer
                - (--course) coursename est de type str et correspond au nom du cours auquel on veut associer le fichier
                - (--tag) chaque tag est de type str
                - (--script) bool est de type bool
        POST : le fichier est cree dans le programme et sur la memoire locale ou distante ssi pathname ne correspond
            au pathname d'aucun fichier existant sur la memoire locale ou distante ou a un fichier connu du programme
            si une option est specifiee :
                --course : l'identifiant unique du cours precise est inscrit dans l'attribut prive course du fichier et
                        l'identifiant unique du fichier est inscrit dans la liste files du cours specifie
                        Si cette option n'est pas specifie, la valeur None est enregistree a la place
                --tag : chaque tag specifie est inscrit comme un element de la liste tags du fichier
                        Si cette option n'est pas specifiee, la valeur None est enregistree a la place
                --script : la valeur de l'attribut prive script du fichier est passe a bool
                        Si cette option n'est pas specifiee, la valeur False est enregistree a la place

        :param line: str
            La ligne d'arguments introduite a la suite de l'appel de la fonction do_touch dans l'interface
                en ligne de commande cree par le module cmd
        """
        do_touch(line, user_instance)

    @staticmethod
    def do_cat(pathname):
        """
        cat [PATHNAME]

        Methode permettant d'afficher en console le contenu d'un fichier

        PRE : pathname est de type str et correspond au pathname d'un fichier existant et connu du programme
        POST : le contenu du fichier est affiche en console ssi pathname correspond au pathname d'un fichier
            existant sur la memoire locale ou distante et connu du programme
        RAISES :

        :param pathname: str
            Correspond au pathname sur la memoire locale ou distante du fichier dont on desire afficher
                le contenu en console
        """
        do_cat(pathname)

    @staticmethod
    def do_write(line):
        """
        write [PATHNAME] [CONTENT]

        Methode permettant d'ecrire du contenu dans un fichier

        PRE : line est de type str et correspond a deux sequences de caracteres separees par un espace
                    - la premiere sequence (pathname) correspond au pathname
                        d'un fichier existant et connu du programme
                    - la deuxieme sequence (content) correspond au contenu
                        que l'on desire ecrire sur le fichier
        POST : content est ecrit sur le fichier ssi pathname correspond au pathname d'un fichier existant sur la
            memoire locale ou distante et connu du programme

        :param line: str
            La ligne d'arguments introduite a la suite de l'appel de la fonction do_write dans l'interface
                en ligne de commande cree par le module cmd
        """
        do_write(line, user_instance)

    @staticmethod
    def do_append(line):
        """
        append [PATHNAME] [CONTENT]

        Methode permettant d'ecrire du contenu a la fin d'un fichier

        PRE : line est de type str et correspond a deux sequences de caracteres separees par un espace
                    - la premiere sequence (pathname) correspond au pathname
                        d'un fichier existant et connu du programme
                    - la deuxieme sequence (content) correspond au contenu
                        que l'on desire ecrire a la fin du fichier
        POST : content est ecrit dans le fichier ssi pathname correspond au pathname d'un fichier existant sur la
            memoire locale ou distante et connu du programme

        :param line: str
            La ligne d'arguments introduite a la suite de l'appel de la fonction do_write dans l'interface
                en ligne de commande cree par le module cmd
        """
        do_append(line, user_instance)

    @staticmethod
    def do_vi(pathname):
        """
        vi [PATHNAME]

        Methode permettant d'ouvrir un fichier dans l'editeur de texte vi

        PRE : pathname est de type str et correspond au pathname d'un fichier existant et connu du programme
        POST : le fichier est ouvert dans vi en console ssi pathname correspond au pathname d'un fichier
            existant sur la memoire locale ou distante et connu du programme

        :param pathname: str
            Correspond au pathname sur la memoire locale ou distante du fichier que l'on desire editer avec vi
        """
        do_vi(pathname, user_instance)

    @staticmethod
    def do_my_files(line):
        """
        my_files

        PRE : line est une chaine de caractere vide
        RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

        Methode permettant de lister les fichiers appartenant a l'utilisateur connecte

        :param line: str
            chaine vide car la fonction reset ne demande pas de parametres
        """
        do_my_files(line, user_instance)

    @staticmethod
    def do_list_courses(line):
        """
        courses

        PRE : line est une chaine de caractere vide
        RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

        Methode permettant de lister les cours connus du programme

        :param line: str
            chaine vide car la fonction reset ne demande pas de parametres
        """
        do_list_courses(line)

    @staticmethod
    def do_my_courses(line):
        """
        my_courses

        PRE : line est une chaine de caractere vide
        RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

        Methode permettant de lister les cours auxquels l'utilisateur connecte est inscrit

        :param line: str
            chaine vide car la fonction reset ne demande pas de parametres
        """
        do_my_courses(line, user_instance)

    @staticmethod
    def do_sub(course_name):
        """
        sub [COURSE_NAME]

        PRE : course_name est de type str et correspond au nom d'un cours connu du programme
        POST : inscrit l'utilisateur connecte au cours ssi le cours est connu du programme
        RAISES : UnknownObjectNameException si le cours n'existe pas

        :param course_name: str
            Le nom du cours auquel l'utilisateur connecte desire s'inscrire
        """
        do_sub(course_name, user_instance)

    @staticmethod
    def do_unsub(course_name):
        """
        unsub [COURSE_NAME]

        PRE : course_name est de type str et correspond au nom d'un cours connu du programme
        POST : desinscrit l'utilisateur connecte du cours ssi le cours est connu du programme
        RAISES : UnknownObjectNameException si le cours n'existe pas

        :param course_name: str
            Le nom du cours auquel l'utilisateur connecte desire s'inscrire
        """
        do_unsub(course_name, user_instance)

    @staticmethod
    def do_specify_course(line):
        """
        specify_course [PATHNAME] [COURSE_NAME]

        PRE : line est de type str et correspond a deux sequences de caracteres separees par un espace
                    - la premiere sequence (pathname) correspond au pathname
                        d'un fichier existant et connu du programme
                    - la deuxieme sequence (course_name) correspond au nom d'un cours existant
        POST : specifie que le fichier traite du cours precise ssi le fichier et le cours existent
        RAISES : UnknownObjectNameException si le cours et/ou le fichier n'existe pas

        :param line: str
            La ligne d'arguments introduite a la suite de l'appel de la fonction do_write dans l'interface
                en ligne de commande cree par le module cmd
        """
        do_specify_course(line)

    @staticmethod
    def do_unspecify_course(pathname):
        """
        unspecify_course [PATHNAME]

        PRE : pathname est de type str et correspond a un fichier existant et connu du programme
        POST : supprimme les liens entre le fichier et le cours auquel il est associe
        RAISES : UnknownObjectNameException si le fichier n'existe pas

        :param pathname: str
            Le chemin d'acces vers le fichier sur la memoire locale ou distante
        """
        do_unspecify_course(pathname)


if __name__ == "__main__":
    username = input("Veuillez entrer votre nom d'utilisateur :")
    students = pickle_get_students()
    admins = pickle_get_admins()
    if username in students["name_id_dict"]:
        try:
            pwd = getpass.getpass("Veuillez entrer votre mot de passe :")
            user_id = students["name_id_dict"][username]
            user_instance = students["objects_dict"][user_id]
            user_instance.verify_pwd(pwd)
        except UnknownPasswordException:
            print("Le mot de passe est errone")
        else:
            Cli.prompt = f"({username}) >>"
            Cli().cmdloop()
    elif username in admins["name_id_dict"]:
        try:
            pwd = getpass.getpass("Veuillez entrer votre mot de passe :")
            user_id = admins["name_id_dict"][username]
            user_instance = admins["objects_dict"][user_id]
            user_instance.verify_pwd(pwd)
        except UnknownPasswordException:
            print("Le mot de passe est errone")
        else:
            AdminCli.prompt = f"({username}) ##"
            AdminCli().cmdloop()
    else:
        print("Le nom d'utilisateur n'existe pas")
