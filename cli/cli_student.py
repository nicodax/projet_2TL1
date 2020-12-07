#!/usr/bin/env python3
import os
import subprocess

from classes.file import File
import cli.cli_misc


def new_file(pathname, script, course_id, tags, student_instance):
    persistent_data = cli.cli_misc.pickle_get(students_arg=True, files_arg=True, courses_arg=True, id_dict_arg=True)
    all_students = persistent_data[0]
    all_files = persistent_data[2]
    all_courses = persistent_data[3]
    id_dict = persistent_data[4]
    file_instance = File(student_instance.user_id, pathname, course_id, id_dict["file"], script, tags)
    student_instance.add_file(id_dict["file"])
    id_dict["file"] += 1
    course_instance = None
    if course_id is not None:
        course_instance = all_courses["objects_dict"][course_id]
        course_instance.add_file(id_dict["file"])
    all_files["name_id_dict"][pathname] = file_instance.file_id
    all_files["objects_dict"][file_instance.file_id] = file_instance
    all_students["objects_dict"][student_instance.user_id] = student_instance
    if course_instance is not None:
        all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_students=all_students, all_files=all_files, all_courses=all_courses, id_dict=id_dict)


def delete_file(file_instance, student_instance):
    persistent_data = cli.cli_misc.pickle_get(students_arg=True, files_arg=True, courses_arg=True)
    all_students = persistent_data[0]
    all_files = persistent_data[2]
    all_courses = persistent_data[3]
    course_instance = None
    if file_instance.course_id is not None:
        course_instance = all_courses["objects_dict"][file_instance.course_id]
        course_instance.remove_file(file_instance.file_id)
    student_instance.remove_file(file_instance.file_id)
    del all_files["name_id_dict"][file_instance.pathname]
    del all_files["objects_dict"][file_instance.file_id]
    all_students["objects_dict"][student_instance.user_id] = student_instance
    if course_instance is not None:
        all_courses["objects_dict"][file_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_students=all_students, all_files=all_files, all_courses=all_courses)
    if os.path.isfile(file_instance.pathname):
        os.remove(file_instance.pathname)


def file_change_script_attribute(pathname, script):
    persistent_data = cli.cli_misc.pickle_get(files_arg=True)
    all_files = persistent_data[2]
    file_instance = cli.cli_misc.pickle_get_instance(pathname, file=True)
    file_instance.script = script
    all_files["objects_dict"][file_instance.file_id] = file_instance
    cli.cli_misc.pickle_save(all_files=all_files)


def file_add_course(pathname, course_name):
    persistent_data = cli.cli_misc.pickle_get(files_arg=True, courses_arg=True)
    all_files = persistent_data[2]
    all_courses = persistent_data[3]
    file_instance = cli.cli_misc.pickle_get_instance(pathname, file=True)
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    file_instance.course_id = course_instance.course_id
    course_instance.add_file(file_instance.file_id)
    all_files["objects_dict"][file_instance.file_id] = file_instance
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_files=all_files, all_courses=all_courses)


def file_add_tag(pathname, tags):
    persistent_data = cli.cli_misc.pickle_get(files_arg=True)
    all_files = persistent_data[2]
    file_instance = cli.cli_misc.pickle_get_instance(pathname, file=True)
    print(file_instance.tags)
    print(tags)
    for i in range(len(tags)):
        file_instance.add_tag(tags[i])
    all_files["objects_dict"][file_instance.file_id] = file_instance
    cli.cli_misc.pickle_save(all_files=all_files)


def file_remove_course(pathname):
    persistent_data = cli.cli_misc.pickle_get(files_arg=True)
    all_files = persistent_data[2]
    file_instance = cli.cli_misc.pickle_get_instance(pathname, file=True)
    file_instance.course_id = None
    all_files["objects_dict"][file_instance.file_id] = file_instance
    cli.cli_misc.pickle_save(all_files=all_files)


def file_remove_tag(pathname, tag):
    persistent_data = cli.cli_misc.pickle_get(files_arg=True)
    all_files = persistent_data[2]
    file_instance = cli.cli_misc.pickle_get_instance(pathname, file=True)
    if tag:
        file_instance.delete_tag(tag)
    else:
        file_instance.tags = tag
    all_files["objects_dict"][file_instance.file_id] = file_instance
    cli.cli_misc.pickle_save(all_files=all_files)


def move_file(current_pathname, new_pathname):
    persistent_data = cli.cli_misc.pickle_get(files_arg=True)
    all_files = persistent_data[2]
    file_instance = cli.cli_misc.pickle_get_instance(current_pathname, file=True)
    file_instance.pathname = new_pathname
    del all_files["name_id_dict"][current_pathname]
    all_files["name_id_dict"][file_instance.pathname] = file_instance.file_id
    all_files["objects_dict"][file_instance.file_id] = file_instance
    cli.cli_misc.pickle_save(all_files=all_files)


def open_file_in_vi(pathname):
    editor = os.getenv('EDITOR', 'vi')
    subprocess.call(f"{editor} {pathname}", shell=True)


def list_subbed_courses(user_instance):
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    content_to_display = []
    temp_courses_dict = {}
    for course_id in all_courses["objects_dict"]:
        if course_id in user_instance.courses:
            temp_courses_dict[course_id] = all_courses["objects_dict"][course_id]
    for course_instance_id in temp_courses_dict:
        course_instance = all_courses["objects_dict"][course_instance_id]
        course_instance_teachers_string = ""
        for i in course_instance.teachers:
            course_instance_teachers_string += f"{i}, "
        course_instance_teachers_string = course_instance_teachers_string[:-2]
        course_display_dict = {
            "course_id": course_instance.course_id,
            "course_name": course_instance.name,
            "description": course_instance.description,
            "teachers": course_instance_teachers_string
        }
        content_to_display.append(course_display_dict)
    cli.cli_misc.courses_terminal_display(content_to_display)


def list_owned_files(user_instance):
    persistent_data = cli.cli_misc.pickle_get(files_arg=True, courses_arg=True)
    all_files = persistent_data[2]
    all_courses = persistent_data[3]
    content_to_display = []
    temp_files_dict = {}
    for file_id in all_files["objects_dict"]:
        if file_id in user_instance.files:
            temp_files_dict[file_id] = all_files["objects_dict"][file_id]
    for file_instance_id in temp_files_dict:
        file_instance = all_files["objects_dict"][file_instance_id]
        file_instance_tags_string = ""
        for i in file_instance.tags:
            file_instance_tags_string += f"{i}, "
        file_instance_tags_string = file_instance_tags_string[:-2]
        course_name = None
        if file_instance.course_id is not None:
            course_name = all_courses["objects_dict"][file_instance.course_id].name
        file_display_dict = {
            "file_id": file_instance.file_id,
            "course_name": course_name,
            "script": file_instance.script,
            "pathname": file_instance.pathname,
            "tags": file_instance_tags_string
        }
        content_to_display.append(file_display_dict)
    cli.cli_misc.files_terminal_display(content_to_display)


def list_sorted_files_on_tags(tags):
    """
    Fonction permettant generer les lignes de chaines de caracteres a afficher en console
        comme resultat du tri sur un ou plusieurs tags

    :param tags: list
        Liste des tags sur base desquels il faut trier les fichiers
    :return content_do_display: list
        Liste des lignes de fichier (sous forme de string) a afficher en console
        Chaque ligne presente plusieurs champs :
            * id={File.file_id}
            * pathname={File.pathname}
            * course={course_name}
                    on trouve course_name grace a File.course_id en allant chercher dans le fichier courses.pkl
                    grace a la fonction cli.cli_misc.pickle_get()
                        persistent_data = cli.cli_misc.pickle_get(all_courses=True)
                        all_courses = persistent_data[3]
                        course_name = all_course["objects_dict"][File.course_id]
            * script={File.script}
    """

    # RECUPERER L'ENTIERETE DES FICHIERS GRACE A LA FONCTION cli.cli_misc.pickle_get()
    # CFR EXPLICATION POUR RECUPERER all_courses DANS LA DOCSTRING
    # NB: tu peux faire en sorte de recupere les deux en une seule ligne :
    #           persistent_data = cli.cli_misc.pickle_get(all_files=True, all_courses=True)
    #           all_files = persistent_data[2]
    #           all_courses = persistent_data[3]

    # UNE FOIS FAIT, IL NE FAUT GARDER QUE LES FICHIERS QUE L'UTILISATEUR CONNECTE POSSEDE
    #   TU PEUX LE SAVOIR GRACE A File.user_id
    #   File.user_id DOIT CORRESPONDRE A current_user_instance.user_id
    #   current_user_instance est normalement defini dans cli.temp_main grace a la fonction cli.cli_misc.login

    # UNE FOIS FAIT, IL NE FAUT GARDER QUE LES FICHIERS QUI POSSEDENT LE (OU LES) TAG(S) SPECIFIES

    content_to_display = []
    # GENERER, POUR CHAQUE FICHIER SELECTIONE, UNE CHAINE DE CARACTERE REPONDANT AUX CONDITIONS DECRITES
    #   DANS LA DOCSTRING AU NIVEAU DE LA DESCRIPTION DE content_to_display ET
    #   LES ENREGISTRER DANS content_to_display

    # RETOURNER content_to_display
    return content_to_display


def list_sorted_files_on_course(course_name):
    """
        Fonction permettant generer les lignes de chaines de caracteres a afficher en console
            comme resultat du tri sur un cours

        :param course_name: str
            Nom du cours sur base duquel il faut trier les fichiers
        :return content_do_display: list
            Liste des lignes de fichier (sous forme de string) a afficher en console
            Chaque ligne presente plusieurs champs :
                * id={File.file_id}
                * pathname={File.pathname}
                * course={course_name}
                        NB :    ici course_name est donne, mais pour effectuer le tri, il sera necessaire de connaitre
                                    course_id (vu que c'est course_id qui est enregistre dans un fichier pour
                                    specifier son appartenance a un cours)
                                on trouve course_id en allant chercher dans le fichier courses.pkl
                                    grace a la fonction cli.cli_misc.pickle_get()
                                        persistent_data = cli.cli_misc.pickle_get(all_courses=True)
                                        all_courses = persistent_data[3]
                                        course_id = all_course["name_id_dict"][course_name]
                * script={File.script}
        """

    # RECUPERER L'ENTIERETE DES FICHIERS GRACE A LA FONCTION cli.cli_misc.pickle_get()
    # CFR EXPLICATION POUR RECUPERER all_courses DANS LA DOCSTRING
    # NB: tu peux faire en sorte de recupere les deux en une seule ligne :
    #           persistent_data = cli.cli_misc.pickle_get(all_files=True, all_courses=True)
    #           all_files = persistent_data[2]
    #           all_courses = persistent_data[3]

    # UNE FOIS FAIT, IL NE FAUT GARDER QUE LES FICHIERS QUE L'UTILISATEUR CONNECTE POSSEDE
    #   TU PEUX LE SAVOIR GRACE A File.user_id
    #   File.user_id DOIT CORRESPONDRE A current_user_instance.user_id
    #   current_user_instance est defini dans cli.temp_main grace a la fonction cli.cli_misc.login

    # UNE FOIS FAIT, IL NE FAUT GARDER QUE LES FICHIERS QUI SONT ASSOCIES AU COURS SPECIFIE

    content_to_display = []
    # GENERER, POUR CHAQUE FICHIER SELECTIONE, UNE CHAINE DE CARACTERE REPONDANT AUX CONDITIONS DECRITES
    #   DANS LA DOCSTRING AU NIVEAU DE LA DESCRIPTION DE content_to_display ET
    #   LES ENREGISTRER DANS content_to_display

    # RETOURNER content_to_display
    return content_to_display


def subscribe_user_to_course(course_name, user_instance):
    persistent_data = cli.cli_misc.pickle_get(students_arg=True, courses_arg=True)
    all_students = persistent_data[0]
    all_courses = persistent_data[3]
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    user_instance.add_course(course_instance.course_id)
    course_instance.add_student(user_instance.user_id)
    all_students["objects_dict"][user_instance.user_id] = user_instance
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_students=all_students, all_courses=all_courses)


def unsubscribe_user_from_course(course_name, user_instance):
    persistent_data = cli.cli_misc.pickle_get(students_arg=True, courses_arg=True)
    all_students = persistent_data[0]
    all_courses = persistent_data[3]
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    user_instance.remove_course(course_instance.course_id)
    course_instance.remove_student(user_instance.user_id)
    all_students["objects_dict"][user_instance.user_id] = user_instance
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_students=all_students, all_courses=all_courses)
