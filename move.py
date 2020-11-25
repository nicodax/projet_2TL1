#! usr/bin/env python3

import argparse
from classes.classes import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("current_pathname", help="chemin d'acces du fichier a deplacer")
    parser.add_argument("new_pathname", help="futur chemin d'acces du fichier")
    args = parser.parse_args()

    current_pathname = args.current_pathname
    new_pathname = args.new_pathname
    file_id = All_files.get_object_id(current_pathname)

    All_files.get_object(file_id).move_file(new_pathname)
    print(f"Le fichier {current_pathname} a ete déplacé vers {new_pathname}")

    with open("pickle_saves/students.pkl", 'wb') as all_students_file:
        pickle.dump(All_students, all_students_file)
    with open("pickle_saves/admins.pkl", 'wb') as all_admins_file:
        pickle.dump(All_admins, all_admins_file)
    with open("pickle_saves/files.pkl", 'wb') as all_files_file:
        pickle.dump(All_files, all_files_file)
    with open("pickle_saves/courses.pkl", 'wb') as all_courses_file:
        pickle.dump(All_courses, all_courses_file)
