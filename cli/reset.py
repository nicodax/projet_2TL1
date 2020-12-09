#!/usr/bin/env python3
import pickle

from classes.course import Course
from classes.user import Student, Admin

initial_students = ["dax", "greg"]
initial_student_fullnames = ["Nicolas Daxhelet", "Gregoire Delannoit"]
initial_student_pwds = ["user123", "user123"]

initial_admins = ["root", "daxxra", "TheGregouze"]
initial_admin_fullnames = ["", "Nicolas Daxhelet", "Gregoire Delannoit"]
initial_admin_pwds = ["root", "user111", "user111"]

initial_courses = ["T2011", "T2012", "T203", "T2051", "T2052", "T2053", "T2054", "T2071", "T2072"]
initial_course_teachers = [
    ["Jonathan Noel", "Virginie Van Den Schrieck"],
    ["Xavier Dubruille", "Jonathan Noel", "Virginie Van Den Schrieck"],
    ["Laurent Schalkwijk", "Marie-Noel Vroman"],
    ["Claude Masson"],
    ["Claude Masson"],
    ["Virginie Van Den Schrieck"],
    ["Jonathan Noel", "Virginie Van Den Schrieck"],
    ["Youcef Bouterfa", "Arnaud Dewulf"],
    ["Youcef Bouterfa", "Arnaud Dewulf"],
]
initial_course_descriptions = ["Developpement Informatique II (Theorie)", "Developpement Informatique II (Pratique)",
                               "Reseaux II", "Systemes d'exploitation (Theorie)", "Systemes d'exploitation (Pratique)",
                               "Administration systemes et reseaux I (Theorie)",
                               "Administration systemes et reseaux I (Pratique)", "Electronique digitale (Theorie)",
                               "Electronique digitale (Pratique)"]


def reset():
    """
    POST : reinitialise la memoire du programme (reinitialise les fichiers de sauvegarde pickle)
    """
    id_dict = {"user": 0, "file": 0, "course": 0}

    all_students = {"name_id_dict": {}, "objects_dict": {}}
    all_admins = {"name_id_dict": {}, "objects_dict": {}}
    all_files = {"name_id_dict": {}, "objects_dict": {}}
    all_courses = {"name_id_dict": {}, "objects_dict": {}}

    for i in range(len(initial_admins)):
        admin_instance = Admin(initial_admins[i], initial_admin_fullnames[i], initial_admin_pwds[i], id_dict["user"])
        id_dict["user"] += 1
        all_admins["objects_dict"][admin_instance.user_id] = admin_instance
        all_admins["name_id_dict"][admin_instance.username] = admin_instance.user_id

    for i in range(len(initial_students)):
        student_instance = Student(initial_students[i], initial_student_fullnames[i], initial_student_pwds[i],
                                   id_dict["user"])
        id_dict["user"] += 1
        all_students["objects_dict"][student_instance.user_id] = student_instance
        all_students["name_id_dict"][student_instance.username] = student_instance.user_id

    for i in range(len(initial_courses)):
        course_instance = Course(initial_courses[i], initial_course_teachers[i], id_dict["course"],
                                 initial_course_descriptions[i])
        id_dict["course"] += 1
        all_courses["objects_dict"][course_instance.course_id] = course_instance
        all_courses["name_id_dict"][course_instance.name] = course_instance.course_id

    return all_students, all_admins, all_files, all_courses, id_dict


def pickle_save(all_students=None, all_admins=None, all_files=None, all_courses=None, id_dict=None):
    """
    ATTENTION : il s'agit de la meme fonction que cli.cli_misc.pickle_save ! Elle est recopiee ici car le pathname
    des fichiers pickle doit être adapte a la position de reset.py dans l'arborescence du programme. En effet,
    si la CLI est inaccessible pour une raison ou une autre, il doit quand meme etre possible de reinitialiser la
    memoire du programme

    PRE : all_students, all_admins, all_files, all_courses et id_dict sont soit de type dict soit None
    POST : enregistre chaque dictionnaire passe en argument
    """

    if all_students is not None:
        with open("../pickle_saves/students.pkl", 'wb') as students_file:
            pickle.dump(all_students, students_file)
    if all_admins is not None:
        with open("../pickle_saves/admins.pkl", 'wb') as admins_file:
            pickle.dump(all_admins, admins_file)
    if all_files is not None:
        with open("../pickle_saves/files.pkl", 'wb') as files_file:
            pickle.dump(all_files, files_file)
    if all_courses is not None:
        with open("../pickle_saves/courses.pkl", 'wb') as courses_file:
            pickle.dump(all_courses, courses_file)
    if id_dict is not None:
        with open("../pickle_saves/id_dict.pkl", 'wb') as id_dict_file:
            pickle.dump(id_dict, id_dict_file)


if __name__ == "__main__":
    students, admins, files, courses, id_dict = reset()
    pickle_save(students, admins, files, courses, id_dict)
    print("La memoire du programme a ete correctement reinitialisee")
