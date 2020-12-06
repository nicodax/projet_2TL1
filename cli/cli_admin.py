#!/usr/bin/env python3
import getpass

from classes.course import Course
from classes.user import Student, Admin
import cli.cli_misc
import cli.reset
from cli.temp_exceptions import ObjectAlreadyExistantException, PasswordNotEqualException


def new_student(username, fullname):
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


def new_course(course_name, teachers, description):
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
    persistent_data = cli.cli_misc.pickle_get(students_arg=True)
    all_students = persistent_data[0]
    student_instance = cli.cli_misc.pickle_get_instance(username, student=True)
    del all_students["name_id_dict"][username]
    del all_students["objects_dict"][student_instance.user_id]
    cli.cli_misc.pickle_save(all_students=all_students)


def delete_admin(username):
    persistent_data = cli.cli_misc.pickle_get(admins_arg=True)
    all_admins = persistent_data[1]
    admin_instance = cli.cli_misc.pickle_get_instance(username, admin=True)
    del all_admins["name_id_dict"][username]
    del all_admins["objects_dict"][admin_instance.user_id]
    cli.cli_misc.pickle_save(all_admins=all_admins)


def delete_course(course_name):
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    del all_courses["name_id_dict"][course_name]
    del all_courses["objects_dict"][course_instance.course_id]
    cli.cli_misc.pickle_save(all_courses=all_courses)


def list_all_admins():
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
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    course_instance.add_teacher(teacher_name)
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_courses=all_courses)


def course_add_description(course_name, description):
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    course_instance.description(description)
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_courses=all_courses)


def course_remove_teacher(course_name, teacher_name, all_teachers):
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    if all_teachers:
        course_instance.teachers = []
    else:
        course_instance.remove_teacher(teacher_name)
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_courses=all_courses)


def course_remove_description(course_name):
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    course_instance = cli.cli_misc.pickle_get_instance(course_name, course=True)
    course_instance.description("")
    all_courses["objects_dict"][course_instance.course_id] = course_instance
    cli.cli_misc.pickle_save(all_courses=all_courses)
