#!/usr/bin/env python3

from classes.classes import *

if __name__ == "__main__":
    user_id = All_students.get_object_id("dax")
    user_instance = All_students.get_object(user_id)
    user_instance.create_file("files/hello_world.txt", "hello_world.txt")

    with open("pickle_saves/students.pkl", 'wb') as all_students_file:
        pickle.dump(All_students, all_students_file)
    with open("pickle_saves/admins.pkl", 'wb') as all_admins_file:
        pickle.dump(All_admins, all_admins_file)
    with open("pickle_saves/files.pkl", 'wb') as all_files_file:
        pickle.dump(All_files, all_files_file)
    with open("pickle_saves/courses.pkl", 'wb') as all_courses_file:
        pickle.dump(All_courses, all_courses_file)
