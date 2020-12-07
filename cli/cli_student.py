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
    return content_to_display


def list_sorted_files_on_tags(tags, user_instance):
    content_to_display = []
    owned_files = list_owned_files(user_instance)
    for i in owned_files:
        number_of_tags = len(tags)
        count_number_of_tags = 0
        for g in tags:
            if g in i["tags"]:
                count_number_of_tags += 1
        if count_number_of_tags == number_of_tags:
            content_to_display.append(i)
    return content_to_display


def list_sorted_files_on_course(course_name, user_instance):
    content_to_display = []
    owned_files = list_owned_files(user_instance)
    for i in owned_files:
        for g in course_name:
            if g in i["course_name"]:
                content_to_display.append(i)
                break
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
