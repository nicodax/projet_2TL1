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
        """
        PRE :   - name est de type str
                - teachers est de type list
                - course_id est de type int
                - description est de type str
        POST : initialise chaque instance de la classe.
                initialise a vide les listes self.__files et self.description
        """
        self.name = name
        self.__teachers = teachers
        self.__files = []
        self.__course_id = course_id
        self.description = description
        self.__students = []

    @property
    def students(self):
        """
        POST : accede a self.__students
        """
        return self.__students

    @property
    def name(self):
        """
        POST : accede a self.__name
        """
        return self.__name

    @property
    def teachers(self):
        """
        POST : accede a self.__teachers
        """
        return self.__teachers

    @property
    def files(self):
        """
        POST : accede a self.__files
        """
        return self.__files

    @property
    def course_id(self):
        """
        POST : accede a self.__course_id
        """
        return self.__course_id

    def __str__(self):
        """
        POST : imprime la description du cours en console
        """
        return self.__description

    @property
    def description(self):
        """
        POST : accede a self.description
        """
        return self.__description

    @name.setter
    def name(self, new_name):
        """
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
        """
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
        """
        PRE : new_list est de type list
        POST : definit la valeur de self.__teachers
        """
        self.__teachers = new_list

    def is_in_teachers(self, name):
        """
        PRE : name est de type str
        POST : retourne True si le name est deja repertoriee dans la liste self.__teachers, retourne False sinon
        """
        return name in self.__teachers

    def add_teacher(self, name):
        """
        PRE : name est de type str
        POST : ajoute le name a la liste self.__teachers ssi il n'y etait pas deja repertorie
        RAISES : AlreadyInListException si name est deja repertorie dans la liste
        """
        if not self.is_in_teachers(name):
            self.__teachers.append(name)
        else:
            raise AlreadyInListException

    def remove_teacher(self, name):
        """
        PRE : name est de type str
        POST : retire le name de la liste self.__teachers ssi il y est deja repertorie
        RAISES : NotInListException si le nom n'est pas deja repertorie dans la liste
        """
        if self.is_in_teachers(name):
            self.__teachers.remove(name)
        else:
            raise NotInListException

    def is_in_files(self, file_id):
        """
        PRE : file_id est de type int
        POST : retourne True si file_id est deja repertorie dans la liste self.__files, retourne False sinon
        """
        return file_id in self.__files

    def add_file(self, file_id):
        """
        PRE : file_id est de type int
        POST : ajoute file_id dans la liste self.__files ssi il n'y etait pas deja repertorie
        RAISES : AlreadyInListException si file_id est deja repertorie dans la liste
        """
        if not self.is_in_files(file_id):
            self.__files.append(file_id)
        else:
            raise AlreadyInListException

    def remove_file(self, file_id):
        """
        PRE : file_id est de type int
        POST : retire file_id de la liste self.__files ssi il y etait deja repertorie
        RAISES : NotInListException si file_id n'est pas repertorie dans la liste
        """
        if self.is_in_files(file_id):
            self.__files.remove(file_id)
        else:
            raise NotInListException

    def is_in_students(self, user_id):
        """
        PRE : user_id est de type int
        POST : retourne True si user_id est deja repertoriee dans la liste self.__students, retourne False sinon
        """
        return user_id in self.__students

    def add_student(self, user_id):
        """
        PRE : user_id est de type int
        POST : ajoute user_id dans la liste self.__students ssi il n'y etait pas deja repertorie
        RAISES : AlreadyInListException si user_id est deja repertorie dans la liste
        """
        if not self.is_in_students(user_id):
            self.__students.append(user_id)
        else:
            raise AlreadyInListException

    def remove_student(self, user_id):
        """
        PRE : user_id est de type int
        POST : retire user_id de la liste self.__students ssi il y etait deja repertorie
        RAISES : NotInListException si user_id n'est pas repertorie dans la liste
        """
        if self.is_in_students(user_id):
            self.__students.remove(user_id)
        else:
            raise NotInListException
