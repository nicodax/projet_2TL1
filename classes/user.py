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
        """Methode permettant l'initialisation de chaque instance de la classe

        PRE :   - username est de type str
                - fullname est de type str
                - pwd est de type str
                - user_id est de type int
        POST : initialise self.__is_admin a True
        """

        self.username = username
        self.fullname = fullname
        self.__pwd = pwd
        self.__user_id = user_id
        self.__is_admin = True

    @property
    def username(self):
        """Methode permettant d'acceder a self.__username"""

        return self.__username

    @property
    def fullname(self):
        """Methode permettant d'acceder a self.__fullname"""

        return self.__fullname

    @property
    def user_id(self):
        """Methode permettant d'acceder a self.__user_id"""

        return self.__user_id

    @property
    def is_admin(self):
        """Methode permettant d'acceder a self.__is_admin"""

        return self.__is_admin

    @username.setter
    def username(self, new_username):
        """Methode permettant de modifier la valeur de self.__username

        PRE : new_username est de type str
        """
        if len(new_username) < 26:
            self.__username = new_username
        else:
            new_username = new_username[:24]
            self.__username = new_username

    @fullname.setter
    def fullname(self, new_fullname):
        """Methode permettant de modifier la valeur de self.__fullname

        PRE : new_fullname est de type str
        """

        if len(new_fullname) < 33:
            self.__fullname = new_fullname
        else:
            new_fullname = new_fullname[:31]
            self.__fullname = new_fullname

    def pwd(self, old_pwd, new_pwd):
        """Methode permettant de modifier la valeur de self.__pwd.

        PRE :   - old_pwd est de type str
                - new_pwd est de type str
        POST : change la valeur de self.__pwd ssi old_pwd == self.__pwd
        """

        if self.verify_pwd(old_pwd):
            self.__pwd = new_pwd

    def verify_pwd(self, pwd):
        """Methode permettant de verifier qu'un mot de passe entre par l'utilisateur correspond au
        mot de passe stocke dans self.__pwd

        PRE : pwd est de type str
        POST : retourne True si pwd == self.__pwd
        RAISES : UnknownPasswordException si pwd != self.__pwd
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
        """Methode permettant l'initialisation de chaque instance de la classe

        PRE :   - username est de type str
                - fullname est de type str
                - pwd est de type str
                - user_id est de type int
        POST :  - initialise self.__is_admin a True
                - initialise a vide les listes self.__files et self.__courses
        """
        super().__init__(username, fullname, pwd, user_id)
        self.__courses = []
        self.__files = []

    @property
    def courses(self):
        """Methode permettant d'acceder a self.__courses"""

        return self.__courses

    @property
    def files(self):
        """Methode permettant d'acceder a self.__files"""

        return self.__files

    def is_in_courses(self, course_id):
        """Methode permettant de verifier si un identifiant de cours est present dans la liste self.__courses

        PRE : course_id est de type int
        POST : retourne True ssi le cours est deja enregistre dans la liste self.__courses, retourne False sinon
        """

        return course_id in self.__courses

    def add_course(self, course_id):
        """Methode permettant d'inscrire l'utilisateur etudiant a un cours

        PRE : course_id est de type int
        POST : ajoute l'identifiant unique associe au cours dans la liste self.__courses ssi celui-ci n'est pas
            pas deja dans la liste
        RAISES : AlreadyInListException si l'identifiant unique du cours est deja repertorie dans la liste
        """

        if not self.is_in_courses(course_id):
            self.__courses.append(course_id)
        else:
            raise AlreadyInListException

    def remove_course(self, course_id):
        """Methode permettant de desinscrire l'utilisateur etudiant d'un cours

        PRE : course_id est de type int
        POST : supprime l'identifiant unique associe au cours de la liste courses ssi il y etait deja repertorie
        RAISES : NotInListException si course_id n'est pas repertorie dans la liste courses
        """

        if self.is_in_courses(course_id):
            self.__courses.remove(course_id)
        else:
            raise NotInListException

    def is_in_files(self, file_id):
        """Methode permettant de verifier si un identifiant de fichier est present dans la liste self.__files

        PRE : file_id est de type int
        POST : retourne True ssi le fichier est deja enregistre dans la liste self.__files, retourne False sinon
        """

        return file_id in self.__files

    def add_file(self, file_id):
        """Methode permettant d'ajouter un fichier a la liste de fichiers appartenant a l'utilisateur etudiant

        PRE : file_id est de type int
        POST : ajoute l'identifiant unique associe au fichier dans la liste self.__files ssi celui-ci n'est pas
            pas deja dans la liste
        RAISES : AlreadyInListException si l'identifiant unique du fichier est deja repertorie dans la liste
        """

        if not self.is_in_files(file_id):
            self.__files.append(file_id)
        else:
            raise AlreadyInListException

    def remove_file(self, file_id):
        """Methode permettant de retirer un fichier de la liste des fichiers appartenant a l'utilisateur

        PRE : file_id est de type int
        POST : supprime l'identifiant unique associe au fichier de la liste self.__files ssi il y etait deja repertorie
        RAISES : NotInListException si file_id n'est pas repertorie dans la liste
        """

        if self.is_in_files(file_id):
            self.__files.remove(file_id)
        else:
            raise NotInListException
