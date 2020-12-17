#!/usr/bin/env python3
from classes.exceptions import UnknownPasswordException, AlreadyInListException, NotInListException


class Admin:
    """Un super utilisateur autorise a effectuer des modifications d'ordre administratif
    Sert de modele pour la creation de la classe Student

    Attributs:
        username        Le nom permettant d'identifier l'utilisateur
        fullname        Le nom complet de l'utilisateur
        pwd             Le mot de passe associe a l'utilisateur
        user_id         L'identifiant unique associe a l'utilisateur
        is_admin        Indicateur du statut de l'utilisateur
    """
    def __init__(self, username, fullname, pwd, user_id):
        """
        PRE:    - username est de type str
                - fullname est de type str
                - pwd est de type str
                - user_id est de type int
        POST: initialise chaque instance de la classe
                initialise self.__is_admin a True
        """
        self.username = username
        self.fullname = fullname
        self.__pwd = pwd
        self.__user_id = user_id
        self.__is_admin = True

    @property
    def username(self):
        """
        PRE:
        POST: accede a self.__username
        """
        return self.__username

    @property
    def fullname(self):
        """
        PRE:
        POST: accede a self.__fullname
        """
        return self.__fullname

    @property
    def user_id(self):
        """
        PRE:
        POST: accede a self.__user_id
        """
        return self.__user_id

    @property
    def is_admin(self):
        """
        PRE:
        POST: accede a self.__is_admin
        """
        return self.__is_admin

    @username.setter
    def username(self, new_username):
        """
        PRE: new_username est de type str
        POST: modifie la valeur de self.__username
        """
        if len(new_username) < 26:
            self.__username = new_username
        else:
            new_username = new_username[:24]
            self.__username = new_username

    @fullname.setter
    def fullname(self, new_fullname):
        """
        PRE: new_fullname est de type str
        POST: modifie la valeur de self.__fullname
        """
        if len(new_fullname) < 33:
            self.__fullname = new_fullname
        else:
            new_fullname = new_fullname[:31]
            self.__fullname = new_fullname

    def pwd(self, old_pwd, new_pwd):
        """
        PRE:    - old_pwd est de type str
                - new_pwd est de type str
        POST: change la valeur de self.__pwd ssi old_pwd == self.__pwd
        """
        if self.verify_pwd(old_pwd):
            self.__pwd = new_pwd

    def verify_pwd(self, pwd):
        """
        PRE: pwd est de type str
        POST: retourne True si pwd == self.__pwd
        RAISES: UnknownPasswordException si pwd != self.__pwd
        """
        if self.__pwd == pwd:
            return True
        else:
            raise UnknownPasswordException


class Student(Admin):
    """Un utilisateur etudiant correspondant a l'utilisateur cible du programme.
    Herite de la classe Admin.
    Il existe une relation d'association bidirectionnelle entre les classes Students et Courses,
    ainsi qu'entre les classes Students et Files

    Attributs:
        username        Le nom permettant d'identifier l'utilisateur etudiant
        fullname        Le nom complet de l'utilisateur etudiant
        pwd             Le mot de passe associe a l'utilisateur etudiant
        user_id         L'identifiant unique associe a l'utilisateur etudiant
        is_admin        L'indicateur de statut de l'utilisateur
        courses         La liste des cours auxquels l'utilisateur etudiant est inscrit
        files           La liste des fichiers appartenants a l'utilisateur etudiant
    """
    def __init__(self, username, fullname, pwd, user_id):
        """
        PRE:    - username est de type str
                - fullname est de type str
                - pwd est de type str
                - user_id est de type int
        POST: initialise chaque instance de la classe
                - initialise self.__is_admin a True
                - initialise a vide les listes self.__files et self.__courses
        """
        super().__init__(username, fullname, pwd, user_id)
        self.__courses = []
        self.__files = []

    @property
    def courses(self):
        """
        PRE:
        POST: accede a self.__courses
        """
        return self.__courses

    @property
    def files(self):
        """
        PRE:
        POST: accede a self.__files
        """
        return self.__files

    def is_in_courses(self, course_id):
        """
        PRE: course_id est de type int
        POST: retourne True ssi le cours est deja enregistre dans la liste self.__courses, retourne False sinon
        """
        return course_id in self.__courses

    def add_course(self, course_id):
        """
        PRE: course_id est de type int
        POST: ajoute course_id dans la liste self.__courses ssi celui-ci n'est pas deja dans la liste
        RAISES: AlreadyInListException si course_id est deja repertorie dans la liste
        """
        if not self.is_in_courses(course_id):
            self.__courses.append(course_id)
        else:
            raise AlreadyInListException

    def remove_course(self, course_id):
        """
        PRE: course_id est de type int
        POST: supprime course_id de la liste self.__courses ssi il y etait deja repertorie
        RAISES: NotInListException si course_id n'est pas repertorie dans la liste courses
        """
        if self.is_in_courses(course_id):
            self.__courses.remove(course_id)
        else:
            raise NotInListException

    def is_in_files(self, file_id):
        """
        PRE: file_id est de type int
        POST: retourne True ssi file_id est deja enregistre dans la liste self.__files, retourne False sinon
        """
        return file_id in self.__files

    def add_file(self, file_id):
        """
        PRE: file_id est de type int
        POST: ajoute file_id dans la liste self.__files ssi celui-ci n'est pas pas deja dans la liste
        RAISES: AlreadyInListException si l'identifiant unique du fichier est deja repertorie dans la liste
        """
        if not self.is_in_files(file_id):
            self.__files.append(file_id)
        else:
            raise AlreadyInListException

    def remove_file(self, file_id):
        """
        PRE: file_id est de type int
        POST: supprime file_id de la liste self.__files ssi il y etait deja repertorie
        RAISES: NotInListException si file_id n'est pas repertorie dans la liste
        """
        if self.is_in_files(file_id):
            self.__files.remove(file_id)
        else:
            raise NotInListException
