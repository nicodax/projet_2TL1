#!/usr/bin/env python3
import pickle

from classes.exceptions import AlreadyInListException
from classes.file import File

if __name__ == "__main__":
    with open("pickle_saves/students.pkl", 'rb') as students_file:
        students = pickle.load(students_file)
    with open("pickle_saves/files.pkl", 'rb') as files_file:
        files = pickle.load(files_file)
    with open("pickle_saves/courses.pkl", 'rb') as courses_file:
        courses = pickle.load(courses_file)

    try:
        user_id = students["name_id_dict"]["dax"]
        user_instance = students["objects_dict"][user_id]

        file_instance = File(user_id, "files/helloworld.txt")
        files["objects_dict"][file_instance.file_id] = file_instance
        files["name_id_dict"][file_instance.pathname] = file_instance.file_id

        user_instance.add_file(file_instance.file_id)
        students["objects_dict"][user_instance.user_id] = user_instance
    except AlreadyInListException:
        print(f"Le fichier {file_instance.pathname} existe deja")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\nVeuillez reessayer")
    else:
        with open("pickle_saves/students.pkl", 'wb') as students_file:
            pickle.dump(students, students_file)
        with open("pickle_saves/files.pkl", 'wb') as files_file:
            pickle.dump(files, files_file)
        with open("pickle_saves/courses.pkl", 'wb') as courses_file:
            pickle.dump(courses, courses_file)
        print(f"Le fichier {file_instance.pathname} est maintenant connu du programme")
