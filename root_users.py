#!/usr/bin/env python3

from classes.classes import *

if __name__ == "__main__":
    Dax = Students("dax", "Nicolas Daxhelet", "user123")
    Daxxra = Admins("daxxra", "Nicolas Daxhelet", "user111")
    Greg = Students("greg", "Gregoire Delannoit", "user123")
    TheGregouze = Admins("TheGregouze", "Gregoire Delannoit", "user111")

    All_students.add_object(Dax.user_id, Dax)
    All_students.add_name_id_pair(Dax.username, Dax.user_id)
    All_students.add_object(Greg.user_id, Greg)
    All_students.add_name_id_pair(Greg.username, Greg.user_id)
    All_admins.add_object(Daxxra.user_id, Daxxra)
    All_admins.add_name_id_pair(Daxxra.username, Daxxra.user_id)
    All_admins.add_object(TheGregouze.user_id, TheGregouze)
    All_admins.add_name_id_pair(TheGregouze.username, TheGregouze.user_id)

    with open("pickle_saves/students.pkl", 'wb') as all_students_file:
        pickle.dump(All_students, all_students_file)
    with open("pickle_saves/admins.pkl", 'wb') as all_admins_file:
        pickle.dump(All_admins, all_admins_file)
    with open("pickle_saves/files.pkl", 'wb') as all_files_file:
        pickle.dump(All_files, all_files_file)
    with open("pickle_saves/courses.pkl", 'wb') as all_courses_file:
        pickle.dump(All_courses, all_courses_file)
