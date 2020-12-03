#!/usr/bin/env python3
import pickle

from classes.user import Student, Admin

if __name__ == "__main__":
    Dax = Student("dax", "Nicolas Daxhelet", "user123")
    Daxxra = Admin("daxxra", "Nicolas Daxhelet", "user111")

    Greg = Student("greg", "Gregoire Delannoit", "user123")
    TheGregouze = Admin("TheGregouze", "Gregoire Delannoit", "user111")

    with open("pickle_saves/students.pkl", 'wb') as students_file:
        students = {"name_id_dict": {}, "objects_dict": {}}

        students["objects_dict"][Dax.user_id] = Dax
        students["name_id_dict"][Dax.username] = Dax.user_id

        students["objects_dict"][Greg.user_id] = Greg
        students["name_id_dict"][Greg.username] = Greg.user_id

        pickle.dump(students, students_file)

    with open("pickle_saves/admins.pkl", 'wb') as admins_file:
        admins = {"name_id_dict": {}, "objects_dict": {}}

        admins["objects_dict"][Daxxra.user_id] = Daxxra
        admins["name_id_dict"][Daxxra.username] = Daxxra.user_id

        admins["objects_dict"][TheGregouze.user_id] = TheGregouze
        admins["name_id_dict"][TheGregouze.username] = TheGregouze.user_id
        pickle.dump(admins, admins_file)

    with open("pickle_saves/files.pkl", 'wb') as files_file:
        files = {"name_id_dict": {}, "objects_dict": {}}
        pickle.dump(files, files_file)
    with open("pickle_saves/courses.pkl", 'wb') as courses_file:
        courses = {"name_id_dict": {}, "objects_dict": {}}
        pickle.dump(courses, courses_file)
