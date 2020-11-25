#! usr/bin/env python3

from classes.classes import *

if __name__ == "__main__":
    All_students = Container()
    All_admins = Container()
    All_files = Container()
    All_courses = Container()

    with open("pickle_saves/students.pkl", 'wb') as all_students_file:
        pickle.dump(All_students, all_students_file)
    with open("pickle_saves/admins.pkl", 'wb') as all_admins_file:
        pickle.dump(All_admins, all_admins_file)
    with open("pickle_saves/files.pkl", 'wb') as all_files_file:
        pickle.dump(All_files, all_files_file)
    with open("pickle_saves/courses.pkl", 'wb') as all_courses_file:
        pickle.dump(All_courses, all_courses_file)
