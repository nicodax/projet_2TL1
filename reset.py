#!/usr/bin/env python3
import pickle

from classes.user import Student, Admin

if __name__ == "__main__":
    Dax = Student("dax", "Nicolas Daxhelet", "user123")
    Daxxra = Admin("daxxra", "Nicolas Daxhelet", "user111")

    Greg = Student("greg", "Gregoire Delannoit", "user123")
    TheGregouze = Admin("TheGregouze", "Gregoire Delannoit", "user111")

    with open("pickle_saves/students.pkl", 'wb') as all_students_file:
        all_students = {"name_id_dict": {}, "objects_dict": {}}

        all_students["objects_dict"][Dax.user_id] = Dax
        all_students["name_id_dict"][Dax.username] = Dax.user_id

        all_students["objects_dict"][Greg.user_id] = Greg
        all_students["name_id_dict"][Greg.username] = Greg.user_id

        pickle.dump(all_students, all_students_file)

    with open("pickle_saves/admins.pkl", 'wb') as all_admins_file:
        all_admins = {"name_id_dict": {}, "objects_dict": {}}

        all_admins["objects_dict"][Daxxra.user_id] = Daxxra
        all_admins["name_id_dict"][Daxxra.username] = Daxxra.user_id

        all_admins["objects_dict"][TheGregouze.user_id] = TheGregouze
        all_admins["name_id_dict"][TheGregouze.username] = TheGregouze.user_id
        pickle.dump(all_admins, all_admins_file)

    with open("pickle_saves/files.pkl", 'wb') as all_files_file:
        all_files = {"name_id_dict": {}, "objects_dict": {}}
        pickle.dump(all_files, all_files_file)
    with open("pickle_saves/courses.pkl", 'wb') as all_courses_file:
        all_courses = {"name_id_dict": {}, "objects_dict": {}}
        pickle.dump(all_courses, all_courses_file)
