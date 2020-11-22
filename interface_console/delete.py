#! usr/bin/env python3

import argparse

import sys
sys.path.insert(1, '..')
from classes import *

with open("pickle_saves/students.pkl", 'rb') as all_students_file:
    All_students = pickle.load(all_students_file)
with open("pickle_saves/admins.pkl", 'rb') as all_admins_file:
    All_admins = pickle.load(all_admins_file)
with open("pickle_saves/files.pkl", 'rb') as all_files_file:
    All_files = pickle.load(all_files_file)
with open("pickle_saves/courses.pkl", 'rb') as all_courses_file:
    All_courses = pickle.load(all_courses_file)

parser = argparse.ArgumentParser()
parser.add_argument("pathname", help="chemin d'acces du fichier a supprimer")
args = parser.parse_args()

pathname = args.pathname
file_name = os.path.basename(pathname)

username = input("Veuillez entrer votre nom d'utilisateur :")
student_instance = All_students.get_object(username)
if student_instance is not None:
    student_instance.delete_file(file_name)
    print(f"Le fichier {file_name} a ete supprime")
else:
    print("Le nom d'utilisateur est incorrect")
