#!/usr/bin/env python3
from classes.exceptions import AlreadyInListException, NotInListException


class Course:
    """Un cours auquel des utilisateurs etudiants sont inscrits.
    Il existe une relation d'association bidirectionnelle entre les classes Courses et Students,
    ainsi qu'entre les classes Courses et Files

    Attributs:
        name            Le code permettant d'identifier le cours
        teachers        Liste les noms des professeurs titulaires du cours
        files           Liste les identifiants uniques des fichiers se rapportant au cours
        students        Liste les noms des etudiants inscrits au cours
        course_id       Identifiant unique associe au cours
        description     L'intitule du cours
    """

    def __init__(self, name, teachers, course_id, description=""):
        """Methode permettant d'initialiser chaque instance de la classe

        PRE :   - name est de type str
                - teachers est de type list
                - course_id est de type int
                - description est de type str
        POST : initialise a vide les listes self.__files et self.description
        """

        self.name = name
        self.__teachers = teachers
        self.__files = []
        self.__course_id = course_id
        self.description = description
        self.__students = []

    @property
    def students(self):
        """Methode permettant d'acceder a self.__students"""

        return self.__students

    @property
    def name(self):
        """Methode permettant d'acceder a self.__name"""

        return self.__name

    @property
    def teachers(self):
        """Methode permettant d'acceder a self.__teachers"""

        return self.__teachers

    @property
    def files(self):
        """Methode permettant d'acceder a self.__files"""

        return self.__files

    @property
    def course_id(self):
        """Methode permettant d'acceder a self.__course_id"""

        return self.__course_id

    def __str__(self):
        """Methode permettant d'imprimer la description du cours en console"""

        return self.__description

    @property
    def description(self):
        """Methode permettant d'acceder a self.description"""

        return self.__description

    @name.setter
    def name(self, new_name):
        """Methode permettant de definir la valeur de self.__name

        PRE :  new_name est de type str
        POST : attribue la valeur de new_name a self.__name ssi elle fait moins de 5 caracteres.
                    Sinon, attribue les 5 premiers caracteres de new_name
        """

        if len(new_name) < 6:
            self.__name = new_name
        else:
            new_name = new_name[:4]
            self.__name = new_name

    @description.setter
    def description(self, string):
        """Methode permettant de definir la valeur de self.description

        PRE :  string est de type str
        POST : attribue la valeur de string a self.description ssi elle fait moins de 50 caracteres.
                    Sinon, attribue les 50 premiers caracteres de string
        """

        if len(string) < 51:
            self.__description = string
        else:
            string = string[:49]
            self.__description = string

    @teachers.setter
    def teachers(self, new_list):
        """Methode permettant de definir la valeur de self.__teachers

        PRE : new_list est de type list
        """

        self.__teachers = new_list

    def is_in_teachers(self, name):
        """Methode permettant de definir si un professeur est titulaire du cours

        PRE : name est de type str
        POST : retourne True si le professeur est deja repertoriee dans la liste self.__teachers, retourne False sinon
        """

        return name in self.__teachers

    def add_teacher(self, name):
        """Methode permettant d'ajouter le nom d'un professeur a la liste des
        professeurs titulaires du cours

        PRE : name est de type str
        POST : ajoute le nom du professeur a la liste self.__teachers ssi il n'y etait pas deja repertorie
        RAISES : AlreadyInListException si le nom est deja repertorie dans la liste
        """

        if not self.is_in_teachers(name):
            self.__teachers.append(name)
        else:
            raise AlreadyInListException

    def remove_teacher(self, name):
        """Methode permettant de supprimer le nom d'un professeur de la liste
        des professeurs titulaires du cours

        PRE : name est de type str
        POST : retire le nom du professeur de la liste self.__teachers ssi il y est deja repertorie
        RAISES : NotInListException si le nom n'est pas deja repertorie dans la liste
        """

        if self.is_in_teachers(name):
            self.__teachers.remove(name)
        else:
            raise NotInListException

    def is_in_files(self, file_id):
        """Methode permettant de definir si un fichier est attribué au cours

        PRE : file_id est de type int
        POST : retourne True si le fichier est deja repertoriee dans la liste self.__files, retourne False sinon
        """

        return file_id in self.__files

    def add_file(self, file_id):
        """Methode permettant d'ajouter l'identifiant unique d'un fichier a la liste
        des fichiers associes au cours.

        PRE : file_id est de type int
        POST : ajoute file_id dans la liste self.__files ssi il n'y etait pas deja repertorie
        RAISES : AlreadyInListException si file_id est deja repertorie dans la liste
        """

        if not self.is_in_files(file_id):
            self.__files.append(file_id)
        else:
            raise AlreadyInListException

    def remove_file(self, file_id):
        """Methode permettant de supprimer l'identifiant unique d'un fichier a la liste
        des fichiers associes au cours.

        PRE : file_id est de type int
        POST : retire file_id de la liste self.__files ssi il y etait deja repertorie
        RAISES : NotInListException si file_id n'est pas repertorie dans la liste
        """

        if self.is_in_files(file_id):
            self.__files.remove(file_id)
        else:
            raise NotInListException

    def is_in_students(self, user_id):
        """Methode permettant de definir si un etudiant est inscrit au cours

        PRE : user_id est de type int
        POST : retourne True si l'etudiant est deja repertoriee dans la liste self.__students, retourne False sinon
        """

        return user_id in self.__students

    def add_student(self, user_id):
        """Methode permettant d'ajouter l'identifiant unique d'un etudiant a la liste
        des etudiants inscrits au cours.

        PRE : user_id est de type int
        POST : ajoute user_id dans la liste self.__students ssi il n'y etait pas deja repertorie
        RAISES : AlreadyInListException si user_id est deja repertorie dans la liste
        """

        if not self.is_in_students(user_id):
            self.__students.append(user_id)
        else:
            raise AlreadyInListException

    def remove_student(self, user_id):
        """Methode permettant de supprimer l'identifiant unique d'un etudiant de la liste
        des etudiants inscrits au cours.

        PRE : user_id est de type int
        POST : retire user_id de la liste self.__students ssi il y etait deja repertorie
        RAISES : NotInListException si user_id n'est pas repertorie dans la liste
        """

        if self.is_in_students(user_id):
            self.__students.remove(user_id)
        else:
            raise NotInListException
