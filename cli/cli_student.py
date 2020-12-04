#!/usr/bin/env python3
import os
import subprocess

from cli.cli_misc import pickle_get_students, pickle_get_files, pickle_get_courses, if_proprietor_get_file, \
    pickle_save, specified_options, pickle_get_ids, pickle_save_ids, pickle_get_admins
from classes.exceptions import FileNotFoundException, FileNotOwnedException, NumberOfArgumentsException, \
    CommandHasNoArgumentsException, UnknownObjectNameException, ObjectAlreadyExistantException, \
    AlreadyInListException, NotInListException
from classes.file import File


def do_del_student(pathname, user_instance):
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

    :param user_instance: object
        utilisateur connecte
    :param pathname: str
        Correspond au pathname du fichier a supprimer sur la memoire locale ou distante
    """
    all_students = pickle_get_students()
    all_files = pickle_get_files()
    all_courses = pickle_get_courses()
    try:
        file_instance = if_proprietor_get_file(pathname, user_instance)
        del all_files["name_id_dict"][pathname]
        del all_files["objects_dict"][file_instance.file_id]

        if file_instance.course_id is not None:
            course_instance = all_courses["objects_dict"][file_instance.course_id]
            course_instance.remove_file(file_instance.file_id)
            all_courses["objects_dict"][course_instance.course_id] = course_instance

        user_instance.remove_file(file_instance.file_id)
        all_students["objects_dict"][user_instance.user_id] = user_instance
    except FileNotFoundException:
        print(f"Le fichier {pathname} n'existe pas\n")
    except FileNotOwnedException:
        print(f"Le fichier {pathname} ne vous appartient pas\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        if os.path.isfile(pathname):
            os.remove(pathname)
            print("Le fichier n'existe plus sur le disque dur")
        else:
            print("Le fichier n'existe pas sur le disque dur")
        print("Le fichier a correctement ete supprime du programme\n")
        pickle_save(all_students, files=all_files, courses=all_courses)


def do_mv(line, user_instance):
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

    :param user_instance: object
        utilisateur connecte
    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_mv dans l'interface
            en ligne de commande cree par le module cmd
    """

    all_files = pickle_get_files()
    current_pathname = ""
    try:
        if len(line.split()) == 2:
            current_pathname, new_pathname = [s for s in line.split()]
        else:
            raise NumberOfArgumentsException
        file_instance = if_proprietor_get_file(current_pathname, user_instance)
        file_instance.pathname = new_pathname
        if os.path.isfile(current_pathname):
            os.rename(current_pathname, new_pathname)
        else:
            raise FileNotFoundException
        all_files["objects_dict"][file_instance.file_id] = file_instance
        all_files["name_id_dict"][file_instance.pathname] = file_instance.file_id
        del all_files["name_id_dict"][current_pathname]
    except NumberOfArgumentsException:
        print("La commande mv demande deux arguments : [CURRENT_PATHNAME] [NEW_PATHNAME]\n")
    except FileNotFoundException:
        print(f"Le fichier {current_pathname} n'existe pas\n")
    except FileNotOwnedException:
        print(f"Le fichier {current_pathname} ne vous appartient pas\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        print(f"Le fichier {current_pathname} a ete déplacé vers {new_pathname}\n")
        pickle_save(files=all_files)


def do_touch(line, user_instance):
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

    :param user_instance: object
        utilisateur connecte
    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_touch dans l'interface
            en ligne de commande cree par le module cmd
    """

    print(line)
    tag_index = ["--tag " in line, "--tag "]
    course_index = ["--course " in line, "--course "]
    script_index = [("--script " in line) or line.endswith("--script"), "--script "]
    options = [tag_index, course_index, script_index]
    print(options)
    specified_options_dict = specified_options(line, options)

    try:
        pathname = line.split(" --")[0]
    except AttributeError:
        pathname = line
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
        return
    tags = None
    script = False
    course_id = None
    course_name = ""

    try:
        all_students = pickle_get_students()
        all_courses = pickle_get_courses()
        all_files = pickle_get_files()

        if "--tag " in specified_options_dict:
            tags = list(specified_options_dict["--tag "].split())
        if "--script " in specified_options_dict:
            print(specified_options_dict["--script"])
            if not specified_options_dict["--script"]:
                raise CommandHasNoArgumentsException
            script = True
            print(script)
        if "--course " in specified_options_dict:
            course_name = specified_options_dict["--course "]
            if course_name in all_courses["name_id_dict"]:
                course_id = all_courses["name_id_dict"][course_name]
            else:
                raise UnknownObjectNameException

        id_dict = pickle_get_ids()
        print(script)
        file_instance = File(user_instance.user_id, pathname, course_id, id_dict["file"], script, tags)
        if file_instance.pathname not in all_files["name_id_dict"]:
            print(file_instance.script)
            all_files["objects_dict"][file_instance.file_id] = file_instance
            all_files["name_id_dict"][file_instance.pathname] = file_instance.file_id
        else:
            raise ObjectAlreadyExistantException

        user_instance.add_file(file_instance.file_id)
        all_students["objects_dict"][user_instance.user_id] = user_instance
        if course_id is not None:
            course_instance = all_courses["objects_dict"][course_id]
            course_instance.add_file(file_instance.file_id)
            all_courses["objects_dict"][course_id] = course_instance
    except CommandHasNoArgumentsException:
        print("L'option --script ne prend pas d'argument\nVeuillez reessayer :\n")
    except UnknownObjectNameException:
        print(f"Le cours {course_name} n'existe pas\n")
    except ObjectAlreadyExistantException:
        print(f"Le fichier {pathname} est deja connu du programme:\n")
    except AlreadyInListException:
        print(f"Le fichier {pathname} existe deja:\n")
    # except Exception as e:
        # print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        pickle_save(all_students=all_students, files=all_files, courses=all_courses)
        print(f"Le fichier {file_instance.pathname} est maintenant connu du programme\n")
        id_dict["file"] += 1
        pickle_save_ids(id_dict)


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

    try:
        all_files = pickle_get_files()
        if pathname in all_files["name_id_dict"]:
            file_id = all_files["name_id_dict"][pathname]
            file_instance = all_files["objects_dict"][file_id]
            file_instance.read_file()
        else:
            raise FileNotFoundException
    except FileExistsError:
        print(f"Le fichier {pathname} n'existe pas")
    except IOError:
        print('Erreur IO.')
    except FileNotFoundException:
        print(f"Le fichier {pathname} n'existe pas\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")


def do_write(line, user_instance):
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

    :param user_instance: object
        utilisateur connecte
    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_write dans l'interface
            en ligne de commande cree par le module cmd
    """

    pathname = line.split()[0]
    content = line.replace(pathname + " ", "")
    try:
        file_instance = if_proprietor_get_file(pathname, user_instance)
        file_instance.write_file(content)
    except FileExistsError:
        print(f"Le fichier {pathname} n'existe pas")
    except IOError:
        print('Erreur IO.')
    except FileNotFoundException:
        print(f"Le fichier {pathname} n'existe pas\n")
    except FileNotOwnedException:
        print(f"Le fichier {pathname} ne vous appartient pas\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        print(f"Le contenu a ete correctement ecrit sur {pathname}\n")


def do_append(line, user_instance):
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

    :param user_instance: object
        utilisateur connecte
    :param line: str
        La ligne d'arguments introduite a la suite de l'appel de la fonction do_write dans l'interface
            en ligne de commande cree par le module cmd
    """

    pathname = line.split()[0]
    content = line.replace(pathname + " ", "")
    try:
        file_instance = if_proprietor_get_file(pathname, user_instance)
        file_instance.append_file(content)
    except FileExistsError:
        print(f"Le fichier {pathname} n'existe pas")
    except IOError:
        print('Erreur IO.')
    except FileNotFoundException:
        print(f"Le fichier {pathname} n'existe pas\n")
    except FileNotOwnedException:
        print(f"Le fichier {pathname} ne vous appartient pas\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        print(f"Le contenu a ete correctement ecrit sur {pathname}\n")


def do_vi(pathname, user_instance):
    """
    vi [PATHNAME]

    Methode permettant d'ouvrir un fichier dans l'editeur de texte vi

    PRE : pathname est de type str et correspond au pathname d'un fichier existant et connu du programme
    POST : le fichier est ouvert dans vi en console ssi pathname correspond au pathname d'un fichier
        existant sur la memoire locale ou distante et connu du programme

    :param user_instance: object
        utilisateur connecte
    :param pathname: str
        Correspond au pathname sur la memoire locale ou distante du fichier que l'on desire editer avec vi
    """

    try:
        if_proprietor_get_file(pathname, user_instance)
        editor = os.getenv('EDITOR', 'vi')
        subprocess.call(f"{editor} {pathname}", shell=True)
    except FileNotFoundException:
        print(f"Le fichier {pathname} n'existe pas\n")
    except FileNotOwnedException:
        print(f"Le fichier {pathname} ne vous appartient pas\n")
    except FileExistsError:
        print(f"Le fichier {pathname} n'existe pas")
    except IOError:
        print('Erreur IO.')
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")


def do_my_files(line, user_instance):
    """
    my_files

    PRE : line est une chaine de caractere vide
    RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

    Methode permettant de lister les fichiers appartenant a l'utilisateur connecte

    :param user_instance: object
        utilisateur connecte
    :param line: str
        chaine vide car la fonction reset ne demande pas de parametres
    """

    try:
        if line != "":
            raise CommandHasNoArgumentsException
    except CommandHasNoArgumentsException:
        print("La fonction n'accepte aucun argument\nVeuillez reesayer :\n")
    else:
        all_files = pickle_get_files()
        all_courses = pickle_get_courses()
        files = user_instance.files
        if files:
            print("")
            print("---------------------------------------------------------------------------------------------" +
                  "----------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------------" +
                  "----------------------------------------------------------------")
            for i in files:
                file_instance = all_files['objects_dict'][i]
                pathname = file_instance.pathname
                script = file_instance.script
                tags = file_instance.tags
                course_id = file_instance.course_id
                course_name = ""
                if course_id is not None:
                    course_name = all_courses["objects_dict"][course_id].name
                add_to_i = ""
                add_to_pathname = ""
                add_to_course_name = ""
                add_to_script = ""
                if len(str(i)) < 3:
                    max_value = 3 - len(str(i))
                    for j in range(max_value):
                        add_to_i += " "
                if len(pathname) < 85:
                    max_value = 85 - len(pathname)
                    for j in range(max_value):
                        add_to_pathname += " "
                if len(course_name) < 5:
                    max_value = 5 - len(course_name)
                    for j in range(max_value):
                        add_to_course_name += " "
                if len(str(script)) < 5:
                    max_value = 5 - len(str(script))
                    for j in range(max_value):
                        add_to_script += " "
                print(f"id={i}{add_to_i}  {course_name}{add_to_course_name}  {script}{add_to_script}" +
                      f"  {pathname}{add_to_pathname}  {tags}")
        print("\n")


def do_list_courses(line):
    """
    courses

    PRE : line est une chaine de caractere vide
    RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

    Methode permettant de lister les cours connus du programme

    :param line: str
        chaine vide car la fonction reset ne demande pas de parametres
    """

    try:
        if line != "":
            raise CommandHasNoArgumentsException
    except CommandHasNoArgumentsException:
        print("La fonction n'accepte aucun argument\nVeuillez reesayer :\n")
    else:
        all_courses = pickle_get_courses()
        course_keys = all_courses["name_id_dict"].keys()
        if course_keys:
            print(" id     code        proffesseurs                                                             " +
                  "              intitule")
            print("---------------------------------------------------------------------------------------------" +
                  "----------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------------" +
                  "----------------------------------------------------------------")
            for i in course_keys:
                course_id = all_courses['name_id_dict'][i]
                course_instance = all_courses['objects_dict'][course_id]
                add_to_course_id = ""
                add_to_teachers = ""
                add_to_i = ""
                num_teachers = len(course_instance.teachers)
                tot_len = (num_teachers * 2) + 2 + ((num_teachers - 1) * 2)
                if len(str(course_id)) < 3:
                    max_value = 3 - len(str(course_id))
                    for j in range(max_value):
                        add_to_course_id += " "
                if len(i) < 10:
                    max_value = 10 - len(i)
                    for j in range(max_value):
                        add_to_i += " "
                for j in course_instance.teachers:
                    tot_len += len(j)
                if tot_len < 85:
                    max_value = 85 - tot_len
                    for j in range(max_value):
                        add_to_teachers += " "
                print(f"id={course_id}{add_to_course_id}  {i}{add_to_i}  " +
                      f"{course_instance.teachers}{add_to_teachers}  {course_instance.description}")
        print("\n")


def do_my_courses(line, user_instance):
    """
    my_courses

    PRE : line est une chaine de caractere vide
    RAISES : CommandHasNoArgumentsException si line n'est pas une chaine de caractere vide

    Methode permettant de lister les cours auxquels l'utilisateur connecte est inscrit

    :param user_instance: object
        utilisateur connecte
    :param line: str
        chaine vide car la fonction reset ne demande pas de parametres
    """

    try:
        if line != "":
            raise CommandHasNoArgumentsException
    except CommandHasNoArgumentsException:
        print("La fonction n'accepte aucun argument\nVeuillez reesayer :\n")
    else:
        all_courses = pickle_get_courses()
        courses = user_instance.courses

        if courses:
            print(" id     code        proffesseurs                                                             " +
                  "              intitule")
            print("---------------------------------------------------------------------------------------------" +
                  "----------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------------" +
                  "----------------------------------------------------------------")
            for i in courses:
                course_instance = all_courses['objects_dict'][i]
                name = course_instance.name
                add_to_name = ""
                add_to_teachers = ""
                add_to_i = ""
                num_teachers = len(course_instance.teachers)
                tot_len = (num_teachers * 2) + 2 + ((num_teachers - 1) * 2)
                if len(str(i)) < 3:
                    max_value = 3 - len(str(i))
                    for j in range(max_value):
                        add_to_i += " "
                if len(name) < 10:
                    max_value = 10 - len(name)
                    for j in range(max_value):
                        add_to_name += " "
                for j in course_instance.teachers:
                    tot_len += len(j)
                if tot_len < 85:
                    max_value = 85 - tot_len
                    for j in range(max_value):
                        add_to_teachers += " "
                print(f"id={i}{add_to_i}  {name}{add_to_name}  {course_instance.teachers}{add_to_teachers}" +
                      f"  {course_instance.description}")
            print("\n")


def do_sub(course_name, user_instance):
    """
    sub [COURSE_NAME]

    PRE : course_name est de type str et correspond au nom d'un cours connu du programme
    POST : inscrit l'utilisateur connecte au cours ssi le cours est connu du programme
    RAISES : UnknownObjectNameException si le cours n'existe pas

    :param user_instance: object
        utilisateur connecte
    :param course_name: str
        Le nom du cours auquel l'utilisateur connecte desire s'inscrire
    """

    all_courses = pickle_get_courses()
    all_students = pickle_get_students()
    course_instance_id = all_courses["name_id_dict"][course_name]
    course_instance = all_courses["objects_dict"][course_instance_id]
    try:
        course_instance.add_student(user_instance.user_id)
        user_instance.add_course(course_instance_id)
        all_students["objects_dict"][user_instance.user_id] = user_instance
        all_courses["objects_dict"][course_instance_id] = course_instance
    except AlreadyInListException:
        print("Vous etes deja inscrits a ce cours\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        pickle_save(all_students=all_students, courses=all_courses)
        print(f"Vous etes maintenant inscrit au cours {course_name}")


def do_unsub(course_name, user_instance):
    """
    unsub [COURSE_NAME]

    PRE : course_name est de type str et correspond au nom d'un cours connu du programme
    POST : desinscrit l'utilisateur connecte du cours ssi le cours est connu du programme
    RAISES : UnknownObjectNameException si le cours n'existe pas

    :param user_instance: object
        utilisateur connecte
    :param course_name: str
        Le nom du cours auquel l'utilisateur connecte desire s'inscrire
    """

    all_courses = pickle_get_courses()
    all_students = pickle_get_students()
    course_instance_id = all_courses["name_id_dict"][course_name]
    course_instance = all_courses["objects_dict"][course_instance_id]
    try:
        course_instance.remove_student(user_instance.user_id)
        user_instance.remove_course(course_instance_id)
    except NotInListException:
        print("Vous n'etes pas inscrits a ce cours\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        pickle_save(all_students=all_students, courses=all_courses)
        print(f"Vous etes maintenant desinscrit du cours {course_name}")


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

    all_files = pickle_get_files()
    all_courses = pickle_get_courses()
    pathname = line.split()[0]
    course_name = line.split()[1]
    try:
        if not (pathname in all_files["name_id_dict"] and course_name in all_courses["name_id_dict"]):
            raise UnknownObjectNameException
        file_instance_id = all_files["name_id_dict"][pathname]
        file_instance = all_files["objects_dict"][file_instance_id]
        course_instance_id = all_files["name_id_dict"][course_name]
        course_instance = all_files["objects_dict"][course_instance_id]

        file_instance.course_id = course_instance_id
        course_instance.add_file(file_instance_id)
    except UnknownObjectNameException:
        print("Le fichier et/ou le cours precise n'existe pas\nVeuillez reessayer :\n")
    except AlreadyInListException:
        print(f"Le fichier {pathname} est deja associe au cours {course_name}\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        pickle_save(files=all_files, courses=all_courses)
        print(f"Le fichier {pathname} est maintenant associe au cours {course_name}")


def do_unspecify_course(pathname):
    """
    unspecify_course [PATHNAME]

    PRE : pathname est de type str et correspond a un fichier existant et connu du programme
    POST : supprimme les liens entre le fichier et le cours auquel il est associe
    RAISES : UnknownObjectNameException si le fichier n'existe pas

    :param pathname: str
        Le chemin d'acces vers le fichier sur la memoire locale ou distante
    """

    all_files = pickle_get_files()
    all_courses = pickle_get_courses()
    try:
        if pathname not in all_files["name_id_dict"]:
            raise UnknownObjectNameException
        file_instance_id = all_files["name_id_dict"][pathname]
        file_instance = all_files["objects_dict"][file_instance_id]
        course_instance_id = file_instance.course_id
        if course_instance_id not in all_courses["objects_dict"]:
            raise UnknownObjectNameException
        course_instance = all_files["objects_dict"][course_instance_id]

        file_instance.course_id = None
        course_instance.remove_file(file_instance_id)
    except UnknownObjectNameException:
        print("Le fichier et/ou le cours precise n'existe pas\nVeuillez reessayer :\n")
    except NotInListException:
        print(f"Le fichier {pathname} n'est associe associe a aucun cours\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer\n")
    else:
        pickle_save(files=all_files, courses=all_courses)
        print(f"Le fichier {pathname} n'est plus associe a aucun cours")


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

    all_students = pickle_get_students()
    all_admins = pickle_get_admins()
    if usertype == "all" or usertype == "students":
        print("Utilisateurs etudiants :")
        key_list = all_students["objects_dict"].keys()
        print(" id     username                         fullname")
        print("------------------------------------------------------------------------")
        print("------------------------------------------------------------------------")
        for i in key_list:
            user_name = all_students['objects_dict'][i].username
            instance_user = all_students['objects_dict'][i]
            add_to_user_name = ""
            add_to_i = ""
            if len(str(i)) < 3:
                max_value = 3 - len(str(i))
                for j in range(max_value):
                    add_to_i += " "
            if len(user_name) < 25:
                max_value = 25 - len(user_name)
                for j in range(max_value):
                    add_to_user_name += " "
            print(f"id={i}{add_to_i}  {user_name}{add_to_user_name}        {instance_user.fullname}")
        print("\n")
    if usertype == "all" or usertype == "admins":
        print("Utilisateurs administrateurs :")
        key_list = all_admins["objects_dict"].keys()
        print(" id     username                         fullname")
        print("------------------------------------------------------------------------")
        print("------------------------------------------------------------------------")
        for i in key_list:
            user_name = all_admins['objects_dict'][i].username
            instance_user = all_admins['objects_dict'][i]
            add_to_user_name = ""
            add_to_i = ""
            if len(str(i)) < 3:
                max_value = 3 - len(str(i))
                for j in range(max_value):
                    add_to_i += " "
            if len(user_name) < 25:
                max_value = 25 - len(user_name)
                for j in range(max_value):
                    add_to_user_name += " "
            print(f"id={i}{add_to_i}  {user_name}{add_to_user_name}        {instance_user.fullname}")
        print("\n")
    if usertype != "all" and usertype != "students" and usertype != "admins":
        print("L'argument [USERTYPE] a trois valeurs autorisees :\nall\nstudents\nadmins\n")
