#!/usr/bin/env python3
import pickle

from classes.course import Course
from classes.user import Student, Admin


def pickle_save(students=None, admins=None, files=None, courses=None):
    """Methode statique permettant d'enregistrer les modifications sur les classes persistantes du programme
            Seules les classes specfiees dans les parametres sont sauvegardees
    """

    if all_students is not None:
        with open("pickle_saves/students.pkl", 'wb') as students_file:
            pickle.dump(students, students_file)
    if all_admins is not None:
        with open("pickle_saves/admins.pkl", 'wb') as admins_file:
            pickle.dump(admins, admins_file)
    if files is not None:
        with open("pickle_saves/files.pkl", 'wb') as files_file:
            pickle.dump(files, files_file)
    if courses is not None:
        with open("pickle_saves/courses.pkl", 'wb') as courses_file:
            pickle.dump(courses, courses_file)


def pickle_save_ids(dict_id):
    """Methode statique permettant d'enregistrer les modifications sur les identifiants uniques des classes utilisateur
        File et Course
    """

    with open("pickle_saves/id_dict.pkl", 'wb') as ids_file:
        pickle.dump(dict_id, ids_file)


class TestException(Exception):
    pass


if __name__ == "__main__":
    id_dict = {"user": 0, "file": 0, "course": 0}

    all_students = {"name_id_dict": {}, "objects_dict": {}}
    all_admins = {"name_id_dict": {}, "objects_dict": {}}
    all_files = {"name_id_dict": {}, "objects_dict": {}}
    all_courses = {"name_id_dict": {}, "objects_dict": {}}

    root = Admin("root", "", "root", id_dict["user"])
    id_dict["user"] += 1
    all_admins["objects_dict"][root.user_id] = root
    all_admins["name_id_dict"][root.username] = root.user_id

    dax = Student("dax", "Nicolas Daxhelet", "user123", id_dict["user"])
    id_dict["user"] += 1
    all_students["objects_dict"][dax.user_id] = dax
    all_students["name_id_dict"][dax.username] = dax.user_id

    daxxra = Admin("daxxra", "Nicolas Daxhelet", "user111", id_dict["user"])
    id_dict["user"] += 1
    all_admins["objects_dict"][daxxra.user_id] = daxxra
    all_admins["name_id_dict"][daxxra.username] = daxxra.user_id

    greg = Student("greg", "Gregoire Delannoit", "user123", id_dict["user"])
    id_dict["user"] += 1
    all_students["objects_dict"][greg.user_id] = greg
    all_students["name_id_dict"][greg.username] = greg.user_id

    the_gregouze = Admin("TheGregouze", "Gregoire Delannoit", "user111", id_dict["user"])
    id_dict["user"] += 1
    all_admins["objects_dict"][the_gregouze.user_id] = the_gregouze
    all_admins["name_id_dict"][the_gregouze.username] = the_gregouze.user_id

    t2011 = Course("T2011", ["Jonathan Noel", "Virginie Van Den Schrieck"], id_dict["course"],
                   "Developpement Informatique II (Theorie)")
    id_dict["course"] += 1
    all_courses["objects_dict"][t2011.course_id] = t2011
    all_courses["name_id_dict"][t2011.name] = t2011.course_id

    t2012 = Course("T2012", ["Xavier Dubruille", "Jonathan Noel", "Virginie Van Den Schrieck"], id_dict["course"],
                   "Developpement Informatique II (Pratique)")
    id_dict["course"] += 1
    all_courses["objects_dict"][t2012.course_id] = t2012
    all_courses["name_id_dict"][t2012.name] = t2012.course_id

    t203 = Course("T203", ["Laurent Schalkwijk", "Marie-Noel Vroman"], id_dict["course"], "Reseaux II")
    id_dict["course"] += 1
    all_courses["objects_dict"][t203.course_id] = t203
    all_courses["name_id_dict"][t203.name] = t203.course_id

    t2051 = Course("T2051", ["Claude Masson"], id_dict["course"], "Systemes d'exploitation (Theorie)")
    id_dict["course"] += 1
    all_courses["objects_dict"][t2051.course_id] = t2051
    all_courses["name_id_dict"][t2051.name] = t2051.course_id

    t2052 = Course("T2052", ["Claude Masson"], id_dict["course"], "Systemes d'exploitation (Pratique)")
    id_dict["course"] += 1
    all_courses["objects_dict"][t2052.course_id] = t2052
    all_courses["name_id_dict"][t2052.name] = t2052.course_id

    t2053 = Course("T2053", ["Virginie Van Den Schrieck"], id_dict["course"],
                   "Administration systemes et reseaux I (Theorie)")
    id_dict["course"] += 1
    all_courses["objects_dict"][t2053.course_id] = t2053
    all_courses["name_id_dict"][t2053.name] = t2053.course_id

    t2054 = Course("T2054", ["Jonathan Noel", "Virginie Van Den Schrieck"], id_dict["course"],
                   "Administration systemes et reseaux I (Pratique)")
    id_dict["course"] += 1
    all_courses["objects_dict"][t2054.course_id] = t2054
    all_courses["name_id_dict"][t2054.name] = t2054.course_id

    t2071 = Course("T2071", ["Youcef Bouterfa", "Arnaud Dewulf"], id_dict["course"], "Electronique digitale (Theorie)")
    id_dict["course"] += 1
    all_courses["objects_dict"][t2071.course_id] = t2071
    all_courses["name_id_dict"][t2071.name] = t2071.course_id

    t2072 = Course("T2072", ["Youcef Bouterfa", "Arnaud Dewulf"], id_dict["course"], "Electronique digitale (Pratique)")
    id_dict["course"] += 1
    all_courses["objects_dict"][t2072.course_id] = t2072
    all_courses["name_id_dict"][t2072.name] = t2072.course_id

    pickle_save_ids(id_dict)
    pickle_save(all_students, all_admins, all_files, all_courses)
    print("La memoire du programme a ete correctement reinitialisee")
