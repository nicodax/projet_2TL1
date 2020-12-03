#!/usr/bin/env python3
from classes.exceptions import AlreadyInListException, NotInListException


class Courses:
    """Un cours auquel des utilisateurs etudiants sont inscrits.
    Il existe une relation d'association bidirectionnelle entre les classes Courses et Students,
    ainsi qu'entre les classes Courses et Files

    Attributs:
        name            L'intitule permettant d'identifier le cours
        teachers        Liste les noms des professeurs titulaires du cours
        files           Liste les identifiants uniques des fichiers se rapportant au cours
        course_id       Identifiant unique associe au cours
        description     Description du cours

    Variables de classe:
        course_id_counter     Compteur necessaire a la creation d'identifiants uniques
    """
    course_id_counter = 0

    def __init__(self, name, teachers):
        """Methode permettant d'initialiser chaque instance de la classe

        PRE :   - name est de type str
                - teachers est de type list

        :param name: str
            L'intitule permettant d'identifier le cours
        :param teachers: list
            Liste les noms (str) des professeurs titulaires du cours
        """

        self.__name = name
        self.__teachers = teachers
        self.__files = []
        self.__course_id = Courses.course_id_counter
        Courses.course_id_counter += 1
        self.__description = ""

    @property
    def name(self):
        """Methode permettant d'acceder a la variable privee name

        :return self.__name : str
            L'intitule permettant d'identifier le cours
        """

        return self.__name

    @property
    def teachers(self):
        """Methode permettant d'acceder a la variable privee teachers

        :return self.__teachers : list
            Liste les noms (str) des professeurs titulaires du cours
        """

        return self.__teachers

    @property
    def files(self):
        """Methode permettant d'acceder a la variable privee files

        :return self.__files : list
            Liste les identifiants uniques des fichiers (file_id : int)
            se rapportant au cours
        """

        return self.__files

    @property
    def course_id(self):
        """Methode permettant d'acceder a la variable privee course_id

        :return self.__course_id : int
            Identifiant unique associe au cours
        """

        return self.__course_id

    def __str__(self):
        """Methode permettant d'imprimer la description du cours en console

        :return self.__description : str
            Description du cours
        """

        return self.__description

    def is_in_teachers(self, name):
        """Methode permettant de definir si un professeur est titulaire du cours

        PRE : name est de type str
        POST : retourne True si le professeur est deja repertoriee dans la liste teachers

        :param name: str
            Le nom du professeur dont on cherche a savoir si il est deja titulaire du cours
        :return: bool
            Indique si le nom du professeur est deja repertorie dans la liste
        """

        return name in self.__teachers

    def is_in_files(self, file_id):
        """Methode permettant de definir si un fichier est attribué au cours

        PRE : file_id est de type int
        POST : retourne True si le fichier est deja repertoriee dans la liste files

        :param file_id: int
            L'identifiant unique du fichier dont on cherche a determiner si il est deja attribue au cours
        :return: bool
            Indique si l'identifiant est deja repertorie dans la liste
        """

        return file_id in self.__files

    def add_teacher(self, name):
        """Methode permettant d'ajouter le nom d'un professeur a la liste des
        professeurs titulaires du cours

        PRE : name est de type str et n'est pas deja repertorie dans la liste teachers
        POST : ajoute le nom du professeur a la liste teachers ssi il n'y etait pas deja repertorie
        RAISES : AlreadyInListException si le nom est deja repertorie dans la liste

        :param name: str
            Le nom du professeur
        """

        if not self.is_in_teachers(name):
            self.__teachers.append(name)
        else:
            raise AlreadyInListException

    def remove_teacher(self, name):
        """Methode permettant de supprimer le nom d'un professeur de la liste
        des professeurs titulaires du cours

        PRE : name est de type str et correspond a une entree de la liste teachers
        POST : retire le nom du professeur de la liste teachers ssi il y est deja repertorie
        RAISES : NotInListException si le nom n'est pas deja repertorie dans la liste

        :param name: str
            Le nom du professeur
        """

        if self.is_in_teachers(name):
            self.__teachers.remove(name)
        else:
            raise NotInListException

    def add_file(self, file_id):
        """Methode permettant d'ajouter l'identifiant unique d'un fichier a la liste
        des fichiers associes au cours.
        Cette méthode est apellee automatiquement par la classe Files lors de l'initialisation :
        elle ne doit donc JAMAIS etre apellee directement

        PRE : file_id est de type int et n'est pas deja repertorie dans la liste files
        POST : ajoute file_id dans la liste ssi il n'y etait pas deja repertorie
        RAISES : AlreadyInListException si file_id est deja repertorie dans la liste

        :param file_id: int
            L'identifiant unique du fichier se rapportant au cours
        """

        if not self.is_in_files(file_id):
            self.__files.append(file_id)
        else:
            raise AlreadyInListException

    def remove_file(self, file_id):
        """Methode permettant de supprimer l'identifiant unique d'un fichier a la liste
        des fichiers associes au cours.
        Cette méthode est apellee automatiquement par la classe Students lors de la suppression d'un fichier :
        elle ne doit donc JAMAIS etre apellee directement

        PRE : file_id est de type int et est deja repertorie dans la liste files
        POST : retire file_id de la liste ssi il y etait deja repertorie
        RAISES : NotInListException si file_id n'est pas repertorie dans la liste

        :param file_id: int
            L'identifiant unique du fichier se rapportant au cours
        """

        if self.is_in_files(file_id):
            self.__files.remove(file_id)
        else:
            raise NotInListException
