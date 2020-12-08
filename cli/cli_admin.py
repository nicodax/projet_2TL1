#!/usr/bin/env python3
import getpass

from classes.course import Course
from classes.user import Student, Admin
import cli.cli_misc
import cli.reset
from cli.exceptions import ObjectAlreadyExistantException, PasswordNotEqualException, UnknownObjectException


def new_student(username, fullname):
    """
    PRE : username et fullname sont de type str
    POST : cree une instance de Student ssi le username n'existe pas deja
    RAISES :    - ObjectAlreadyExistantException si le username existe deja
                - PasswordNotEqualException si les deux mots de passe entres par l'utilisateur ne correspondent pas
    """
    pwd1 = getpass.getpass("Veuillez creer un mot de passe :")
    pwd2 = getpass.getpass("Veuillez confirmer le mot de passe :")
    if pwd1 == pwd2:
        persistent_data = cli.cli_misc.pickle_get(students_arg=True, id_dict_arg=True)
        all_students = persistent_data[0]
        id_dict = persistent_data[4]
        student_instance = Student(username, fullname, pwd1, id_dict["user"])
        id_dict["user"] += 1
        if username in all_students["name_id_dict"]:
            raise ObjectAlreadyExistantException
        all_students["objects_dict"][student_instance.user_id] = student_instance
        all_students["name_id_dict"][username] = student_instance.user_id
        cli.cli_misc.pickle_save(all_students=all_students, id_dict=id_dict)
    else:
        raise PasswordNotEqualException


def new_admin(username, fullname):
    """
    PRE : username et fullname sont de type str
    POST : cree une instance de Admin ssi le username n'existe pas deja
    RAISES :    - ObjectAlreadyExistantException si le username existe deja
                - PasswordNotEqualException si les deux mots de passe entres par l'utilisateur ne correspondent pas
    """
    pwd1 = getpass.getpass("Veuillez creer un mot de passe :")
    pwd2 = getpass.getpass("Veuillez confirmer le mot de passe :")
    if pwd1 == pwd2:
        persistent_data = cli.cli_misc.pickle_get(admins_arg=True, id_dict_arg=True)
        all_admins = persistent_data[1]
        id_dict = persistent_data[4]
        admin_instance = Admin(username, fullname, pwd1, id_dict["user"])
        id_dict["user"] += 1
        if username in all_admins["name_id_dict"]:
            raise ObjectAlreadyExistantException
        all_admins["objects_dict"][admin_instance.user_id] = admin_instance
        all_admins["name_id_dict"][username] = admin_instance.user_id
        cli.cli_misc.pickle_save(all_admins=all_admins, id_dict=id_dict)
    else:
        raise PasswordNotEqualException


def new_course(course_name, teachers, description):
    """
    PRE :   - course_name et description sont de type str
            - teachers est de type list
    POST : cree une instance de Course ssi le code de cours n'existe pas deja
    RAISES : ObjectAlreadyExistantException si le code du cours existe deja
    """
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True, id_dict_arg=True)
    all_courses = persistent_data[3]
    id_dict = persistent_data[4]
    course_instance = Course(course_name, teachers, id_dict["course"], description)
    id_dict["course"] += 1
    if course_name in all_courses["name_id_dict"]:
        raise ObjectAlreadyExistantException
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    all_courses["name_id_dict"][course_name] = course_instance.course_id
    cli.cli_misc.pickle_save(all_courses=all_courses, id_dict=id_dict)


def delete_student(username):
    """
    PRE : username est de type str
    POST : supprime l'instance de Student correspondant a username si le username existe
    RAISES : UnknownObjectException si le username n'existe pas
    """
    persistent_data = cli.cli_misc.pickle_get(students_arg=True)
    all_students = persistent_data[0]
    if username not in all_students["name_id_dict"]:
        raise UnknownObjectException
    student_instance = cli.cli_misc.pickle_get_instance(username, student=True)
    del all_students["name_id_dict"][username]
    del all_students["objects_dict"][student_instance.user_id]
    cli.cli_misc.pickle_save(all_students=all_students)


def delete_admin(username):
    """
    PRE : username est de type str
    POST : supprime l'instance de Admin correspondant a username si le username existe
    RAISES : UnknownObjectException si le username n'existe pas
    """
    persistent_data = cli.cli_misc.pickle_get(admins_arg=True)
    all_admins = persistent_data[1]
    if username not in all_admins["name_id_dict"]:
        raise UnknownObjectException
    admin_instance = cli.cli_misc.pickle_get_instance(username, admin=True)
    del all_admins["name_id_dict"][username]
    del all_admins["objects_dict"][admin_instance.user_id]
    cli.cli_misc.pickle_save(all_admins=all_admins)


def delete_course(course_name):
    """
    PRE : course_name est de type str
    POST : supprime l'instance de Course correspondant a course_name si le course_name existe
    RAISES : UnknownObjectException si le course_name n'existe pas
    """
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    if course_name not in all_courses["name_id_dict"]:
        raise UnknownObjectException
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    del all_courses["name_id_dict"][course_name]
    del all_courses["objects_dict"][course_instance.course_id]
    cli.cli_misc.pickle_save(all_courses=all_courses)


def list_all_admins():
    """
    POST : cree un dictionnaire des informations relatives aux administrateurs
    """
    persistent_data = cli.cli_misc.pickle_get(admins_arg=True)
    all_admins = persistent_data[1]
    content_to_display = []
    for admin_instance_id in all_admins["objects_dict"]:
        admin_instance = all_admins["objects_dict"][admin_instance_id]
        user_display_dict = {
            "user_id": admin_instance.user_id,
            "username": admin_instance.username,
            "fullname": admin_instance.fullname,
        }
        content_to_display.append(user_display_dict)
    print("Utilisateurs administrateurs :")
    cli.cli_misc.users_terminal_display(content_to_display)


def course_add_teacher(course_name, teacher_name):
    """
    PRE : course_name et teacher_name sont de type str
    POST : ajoute teacher_name a la liste des professeurs titulaires du cours ssi le course_name existe
    RAISES : UnknownObjectException si le cours n'existe pas
    """
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    if course_name not in all_courses["name_id_dict"]:
        raise UnknownObjectException
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    course_instance.add_teacher(teacher_name)
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_courses=all_courses)


def course_add_description(course_name, description):
    """
    PRE : course_name et description sont de type str
    POST : modifie la description du cours ssi course_name existe
    RAISES : UnknownObjectException si le course_name n'existe pas
    """
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    if course_name not in all_courses["name_id_dict"]:
        raise UnknownObjectException
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    course_instance.description = description
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_courses=all_courses)


def course_remove_teacher(course_name, teacher_name, all_teachers):
    """
    PRE :   - course_name et teacher_name sont de type str
            - all_teachers est de type bool
    POST : retire teacher_name de la liste des professeurs titulaires du cours ssi course_name existe
    RAISES : UnknownObjectException si course_name n'existe pas
    """
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    if course_name not in all_courses["name_id_dict"]:
        raise UnknownObjectException
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    if all_teachers:
        course_instance.teachers = []
    else:
        course_instance.remove_teacher(teacher_name)
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_courses=all_courses)


def course_remove_description(course_name):
    """
    PRE : course_name est de type str
    POST : supprime la description du cours ssi course_name existe
    RAISES : UnknownObjectException si course_name n'existe pas
    """
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    if course_name not in all_courses["name_id_dict"]:
        raise UnknownObjectException
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    course_instance.description = ""
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_courses=all_courses)
