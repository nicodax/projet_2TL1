#!/usr/bin/env python3
import cli.cli_misc


def list_all_students():
    """
    PRE:
    POST: cree un dictionnaire des informations relatives aux etudiants
    RAISES:
    """
    persistent_data = cli.cli_misc.pickle_get(students_arg=True)
    all_students = persistent_data[0]
    content_to_display = []
    for student_instance_id in all_students["objects_dict"]:
        student_instance = all_students["objects_dict"][student_instance_id]
        user_display_dict = {
                                "user_id": student_instance.user_id,
                                "username": student_instance.username,
                                "fullname": student_instance.fullname,
        }
        content_to_display.append(user_display_dict)
    print("Utilisateurs etudiants :")
    cli.cli_misc.users_terminal_display(content_to_display)


def list_all_courses():
    """
    PRE:
    POST: cree un dictionnaire des informations relatives aux cours
    RAISES:
    """
    persistent_data = cli.cli_misc.pickle_get(courses_arg=True)
    all_courses = persistent_data[3]
    content_to_display = []
    for course_instance_id in all_courses["objects_dict"]:
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
