#! usr/bin/env python3

import argparse
from classes.classes import *
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pathname", help="chemin d'acces du fichier a supprimer")
    args = parser.parse_args()

    pathname = args.pathname
    file_name = os.path.basename(pathname)

    username = input("Veuillez entrer votre nom d'utilisateur :")
    student_instance = All_students.get_object(username)
    student_instance.delete_file(file_name)
    print(f"Le fichier {pathname} a ete supprime")
