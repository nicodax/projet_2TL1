#! usr/bin/env python3

import argparse
from classes.classes import *
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("current_pathname", help="chemin d'acces du fichier a deplacer")
    parser.add_argument("new_pathname", help="futur chemin d'acces du fichier")
    args = parser.parse_args()

    current_pathname = args.current_pathname
    new_pathname = args.new_pathname
    file_name = os.path.basename(current_pathname)

    All_files.get_object(file_name).move_file(new_pathname)
    print(f"Le fichier {file_name} a ete déplacé vers {new_pathname}")
