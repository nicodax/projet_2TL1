#!/usr/bin/env python3
from classes.exceptions import UnknownPasswordException, AlreadyInListException, NotInListException


class User:
    """Un utilisateur generique servant de modele pour les Admins et les Students

    Attributs:
        username        Le nom permettant d'identifier l'utilisateur
        fullname        Le nom complet de l'utilisateur
        pwd             Le mot de passe associe a l'utilisateur
        user_id         L'identifiant unique associe a l'utilisateur
        is_admin        Indicateur du statut de l'utilisateur

    Variables de classe:
        user_id_counter     Compteur necessaire a la creation d'identifiants uniques
    """

    def __init__(self, username, fullname, pwd, user_id):
        """Methode permettant l'initialisation de chaque instance de la classe

        PRE : username, fullname et pwd sont de type str

        :param username: str
            Le nom permettant d'identifier l'utilisateur
        :param fullname: str
            Le nom complet de l'utilisateur
        :param pwd: str
            Le mot de passe associe a l'utilisateur
        """

        self.__username = username
        self.__fullname = fullname
        self.__pwd = pwd
        self.__user_id = user_id
        self.__is_admin = False

    @property
    def username(self):
        """Methode permettant d'acceder a la variable privee username

        :return self.__username : str
            Le nom permettant d'identifier l'utilisateur
        """

        return self.__username

    @property
    def fullname(self):
        """Methode permettant d'acceder a la variable privee fullname

        :return self.__fullname : str
            Le nom complet de l'utilisateur
        """

        return self.__fullname

    @property
    def user_id(self):
        """Methode permettant d'acceder a la variable privee user_id

        :return self.__user_id : int
            L'identifiant unique associe a l'utilisateur
        """

        return self.__user_id

    @property
    def is_admin(self):
        """Methode permettant d'acceder a la variable privee is_admin

        :return self.__is_admin : bool
            L'indicateur de statut de l'utilisateur
        """

        return self.__is_admin

    @username.setter
    def username(self, new_username):
        """Methode permettant de modifier la valeur de la variable privee username

        PRE : new_username est de type str

        :param new_username: str
            Nouvelle valeur de username
        """

        self.__username = new_username

    @fullname.setter
    def fullname(self, new_fullname):
        """Methode permettant de modifier la valeur de la variable privee fullname

        PRE : new_fullname est de type str

        :param new_fullname: str
            Nouvelle valeur de fullname
        """

        self.__fullname = new_fullname

    def pwd(self, old_pwd, new_pwd):
        """Methode permettant de modifier la valeur de la variable privee pwd.
        La demande de modification n'est prise en compte que si le mot de passe actuel est precise

        PRE :   - old_pwd et new_pwd sont de type str
                - old_pwd correspond à self.__pwd
        POST : change la valeur de self.__pwd ssi old_pwd == self.__pwd

        :param old_pwd: str
            Mot de passe actuellement associe a l'utilisateur
        :param new_pwd: str
            Nouvelle valeur de pwd
        """

        if self.verify_pwd(old_pwd):
            self.__pwd = new_pwd

    def verify_pwd(self, pwd):
        """Methode permettant de verifier qu'un mot de passe entre par l'utilisateur correspond au
        mot de passe stocke dans la variable privee pwd

        PRE : pwd est de type str
        POST : retourne True si pwd == self.__pwd
        RAISES : UnknownPasswordException si pwd != self.__pwd

        :param pwd: str
            Le mot de passe a verifier

        :return: bool
            Indique si le mot de passe entre par l'utilisateur correspond au mot de passe enregistre
        """

        if self.__pwd == pwd:
            return True
        else:
            raise UnknownPasswordException


class Student(User):
    """Un utilisateur etudiant correspondant a l'utilisateur cible du programme.
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

        PRE : username, fullname et pwd sont de type str

        :param username: str
            Le nom permettant d'identifier l'utilisateur etudiant
        :param fullname: str
            Le nom complet de l'utilisateur etudiant
        :param pwd: str
            Le mot de passe associe a l'utilisateur etudiant
        """
        super().__init__(username, fullname, pwd, user_id)
        self.__courses = []
        self.__files = []

    @property
    def courses(self):
        """Methode permettant d'acceder a la variable privee courses

        :return self.__courses : list
            Liste les identifiants des cours (course_id: int) auxquels l'utilisateur etudiant est inscrit
        """
        return self.__courses

    @property
    def files(self):
        """Methode permettant d'acceder a la variable privee files

        :return self.__files : list
            Liste les identifiants des fichiers (file_id: int) appartenants a l'utilisateur etudiant
        """
        return self.__files

    def is_in_courses(self, course_id):
        """Methode permettant de verifier si un identifiant de cours est present dans la liste des cours

        PRE : course_id est de type int
        POST : retourne True ssi le cours est deja enregistre dans la liste

        :param course_id: int
            L'identifiant unique du cours
        :return: bool
            Indique si course_id existe dans la liste
        """

        return course_id in self.__courses

    def is_in_files(self, file_id):
        """Methode permettant de verifier si un identifiant de fichier est present dans la liste files

        PRE : file_id est de type int
        POST : retourne True ssi le fichier est deja enregistre dans la liste

        :param file_id: int
            L'identifiant unique du fichier
        :return: bool
            Indique si file_id existe dans la liste
        """

        return file_id in self.__files

    def add_course(self, course_id):
        """Methode permettant d'inscrire l'utilisateur etudiant a un cours

        PRE : course_id est de type int et n'est pas deja repertorie dans la liste courses
        POST : ajoute l'identifiant unique associe au cours dans la liste courses ssi celui-ci n'est pas
            pas deja dans la liste
        RAISES : AlreadyInListException si l'identifiant unique du cours est deja repertorie dans la liste

        :param course_id: int
            identifiant unique du cours
        """

        if not self.is_in_courses(course_id):
            self.__courses.append(course_id)
        else:
            raise AlreadyInListException

    def remove_course(self, course_id):
        """Methode permettant de desinscrire l'utilisateur etudiant d'un cours

        PRE : course_id est de type int et est deja repertorie dans la liste courses
        POST : supprime l'identifiant unique associe au cours de la liste courses ssi il y etait deja repertorie
        RAISES : NotInListException si course_id n'est pas repertorie dans la liste courses

        :param course_id: int
            identifiant unique du cours
        """

        if self.is_in_courses(course_id):
            self.__courses.remove(course_id)
        else:
            raise NotInListException

    def add_file(self, file_id):
        """Methode permettant d'ajouter un fichier a la liste de fichiers appartenant a l'utilisateur etudiant

        PRE : file_id est de type int et n'est pas deja repertorie dans la liste files
        POST : ajoute l'identifiant unique associe au fichier dans la liste files ssi celui-ci n'est pas
            pas deja dans la liste
        RAISES : AlreadyInListException si l'identifiant unique du fichier est deja repertorie dans la liste

        :param file_id: int
            identifiant unique du fichier
        """

        if not self.is_in_files(file_id):
            self.__files.append(file_id)
        else:
            raise AlreadyInListException

    def remove_file(self, file_id):
        """Methode permettant de retirer un fichier de la liste des fichiers appartenant a l'utilisateur

        PRE : file_id est de type int et est deja repertorie dans la liste files
        POST : supprime l'identifiant unique associe au fichier de la liste files ssi il y etait deja repertorie
        RAISES : NotInListException si file_id n'est pas repertorie dans la liste files

        :param file_id: int
            identifiant unique du fichier
        """

        if self.is_in_files(file_id):
            self.__files.remove(file_id)
        else:
            raise NotInListException


class Admin(User):
    """Un super utilisateur autorise a effectuer des modifications d'ordre administratif

    Attributs:
        username        Le nom permettant d'identifier l'utilisateur administrateur
        fullname        Le nom complet de l'utilisateur administrateur
        pwd             Le mot de passe associe a l'utilisateur administrateur
        user_id         L'identifiant unique associe a l'utilisateur administrateur
    """

    def __init__(self, username, fullname, pwd, user_id):
        """Methode permettant l'initialisation de chaque instance de la classe

        PRE : username, fullname et pwd sont de type str

        :param username: str
            Le nom permettant d'identifier l'utilisateur administrateur
        :param fullname: str
            Le nom complet de l'utilisateur administrateur
        :param pwd: str
            Le mot de passe associe a l'utilisateur administrateur
        """

        super().__init__(username, fullname, pwd, user_id)
        self._is_admin = True
