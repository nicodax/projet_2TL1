#! usr/bin/env python3

import argparse
from classes.classes import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pathname", help="chemin d'acces du fichier a supprimer")
    args = parser.parse_args()

    pathname = args.pathname

    username = input("Veuillez entrer votre nom d'utilisateur :")
    user_id = All_students.get_object_id(username)
    student_instance = All_students.get_object(user_id)
    student_instance.delete_file(pathname)
    print(f"Le fichier {pathname} a ete supprime")

    with open("pickle_saves/students.pkl", 'wb') as all_students_file:
        pickle.dump(All_students, all_students_file)
    with open("pickle_saves/admins.pkl", 'wb') as all_admins_file:
        pickle.dump(All_admins, all_admins_file)
    with open("pickle_saves/files.pkl", 'wb') as all_files_file:
        pickle.dump(All_files, all_files_file)
    with open("pickle_saves/courses.pkl", 'wb') as all_courses_file:
        pickle.dump(All_courses, all_courses_file)
