#!/usr/bin/env python3

import os
import pickle


class Users:
    """Un utilisateur generique servant de modele pour les Admins et les Students

    Attributs:
        username        Le nom permettant d'identifier l'utilisateur
        fullname        Le nom complet de l'utilisateur
        pwd             Le mot de passe associe a l'utilisateur
        user_id         L'identifiant unique associe a l'utilisateur
    """

    def __init__(self, username, fullname, pwd):
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
        self.__user_id = UsersIdGenerator.generate_new_id()

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


class Admins(Users):
    """Un super utilisateur autorise a effectuer des modifications d'ordre administratif

    Attributs:
        username        Le nom permettant d'identifier l'utilisateur administrateur
        fullname        Le nom complet de l'utilisateur administrateur
        pwd             Le mot de passe associe a l'utilisateur administrateur
        user_id         L'identifiant unique associe a l'utilisateur administrateur
    """

    def __init__(self, username, fullname, pwd):
        """Methode permettant l'initialisation de chaque instance de la classe

        PRE : username, fullname et pwd sont de type str

        :param username: str
            Le nom permettant d'identifier l'utilisateur administrateur
        :param fullname: str
            Le nom complet de l'utilisateur administrateur
        :param pwd: str
            Le mot de passe associe a l'utilisateur administrateur
        """

        super().__init__(username, fullname, pwd)

    @staticmethod
    def create_student(username, fullname, pwd):
        """Methode statique permettant la creation d'une nouvelle instance de la classe Students

        PRE : username, fullname et pwd sont de type str
        POST : cree une instance de la classe Students ssi celle-ci n'existe pas deja

        :param username: str
            Le nom permettant d'identifier le futur utilisateur etudiant
        :param fullname: str
            Le nom complet du futur utilisateur etudiant
        :param pwd: str
            Le mot de passe associe au futur utilisateur etudiant
        """

        student_instance = Students(username, fullname, pwd)
        All_students.add_object(student_instance.user_id, student_instance)
        All_students.add_name_id_pair(username, student_instance.user_id)

    @staticmethod
    def delete_student(username):
        """Methode statique permettant la suppression d'une instance de la classe Students

        PRE : username est de type str et correspond a l'attribut username d'une instance de la classe Students
        POST : supprime l'instance specifiee par username ssi elle existait deja

        :param username: str
            Le nom permettant d'identifier l'utilisateur etudiant
        """

        student_id = All_students.get_object_id(username)
        All_students.delete_object(student_id)
        All_students.delete_name_id_pair(username)

    @staticmethod
    def create_admin(username, fullname, pwd):
        """Methode statique permettant la creation d'une nouvelle instance de la classe Admins

        PRE : username, fullname et pwd sont de type str
        POST : cree une instance de la classe Admins ssi celle-ci n'existe pas deja

        :param username: str
            Le nom permettant d'identifier le futur utilisateur administrateur
        :param fullname: str
            Le nom complet du futur utilisateur administrateur
        :param pwd: str
            Le mot de passe associe au futur utilisateur administrateur
        """

        admin_instance = Admins(username, fullname, pwd)
        All_admins.add_object(admin_instance.user_id, admin_instance)
        All_admins.add_name_id_pair(username, admin_instance.user_id)

    @staticmethod
    def delete_admin(username):
        """Methode statique permettant la suppression d'une instance de la classe Admins

        PRE : username est de type str et correspond a l'attribut username d'une instance de la classe Admins
        POST : supprime l'instance specifiee par username ssi elle existait deja

        :param username: str
            Le nom permettant d'identifier l'utilisateur administrateur
        """

        admin_id = All_admins.get_object_id(username)
        All_admins.delete_object(admin_id)
        All_admins.delete_name_id_pair(username)

    @staticmethod
    def create_course(name, teachers):
        """Methode statique permettant la creation d'une nouvelle instance de la classe Courses

        PRE :   - name est de type str
                - teachers est de type list
        POST : cree une instance de la classe Courses ssi celle-ci n'existe pas deja

        :param name: str
            L'intitule permettant d'identifier le cours
        :param teachers: list
            Liste les noms (str) des professeurs titulaires du cours
        """

        course_instance = Courses(name, teachers)
        All_courses.add_object(course_instance.course_id, course_instance)
        All_courses.add_name_id_pair(name, course_instance.course_id)

    @staticmethod
    def delete_course(name):
        """Methode statique permettant la suppression d'une instance de la classe Courses

        PRE : name est de type str et correspond a l'attribut name d'une instance de la classe Courses
        POST : supprimme l'instance specifiee par name ssi elle existait deja

        :param name: str
            L'intitule permettant d'identifier le cours
        """

        course_id = All_courses.get_object_id(name)
        All_courses.delete_object(course_id)
        All_courses.delete_name_id_pair(name)


class Students(Users):
    """Un utilisateur etudiant correspondant a l'utilisateur cible du programme.
    Il existe une relation d'association bidirectionnelle entre les classes Students et Courses,
    ainsi qu'entre les classes Students et Files

    Attributs:
        username        Le nom permettant d'identifier l'utilisateur etudiant
        fullname        Le nom complet de l'utilisateur etudiant
        pwd             Le mot de passe associe a l'utilisateur etudiant
        user_id         L'identifiant unique associe a l'utilisateur etudiant
        courses         La liste des cours auxquels l'utilisateur etudiant est inscrit
        files           La liste des fichiers appartenants a l'utilisateur etudiant
    """

    def __init__(self, username, fullname, pwd):
        """Methode permettant l'initialisation de chaque instance de la classe

        PRE : username, fullname et pwd sont de type str

        :param username: str
            Le nom permettant d'identifier l'utilisateur etudiant
        :param fullname: str
            Le nom complet de l'utilisateur etudiant
        :param pwd: str
            Le mot de passe associe a l'utilisateur etudiant
        """
        super().__init__(username, fullname, pwd)
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

    def add_course(self, course_name):
        """Methode permettant d'inscrire l'utilisateur etudiant a un cours

        PRE : course_name est de type str et le cours en question n'est pas deja repertorie dans la liste courses
        POST : ajoute l'identifiant unique associe au cours dans la liste courses ssi celui-ci n'est pas
            pas deja dans la liste
        RAISES : AlreadyInListException si l'identifiant unique du cours est deja repertorie dans la liste

        :param course_name: str
            nom du cours
        """

        course_id = All_courses.get_object_id(course_name)
        if not self.is_in_courses(course_id):
            self.__courses.append(course_name)
        else:
            raise AlreadyInListException

    def delete_course(self, course_name):
        """Methode permettant de desinscrire l'utilisateur etudiant d'un cours

        PRE : course_name est de type str et le cours en question deja repertorie dans la liste courses
        POST : supprime l'identifiant unique associe au cours de la liste courses ssi il y etait deja repertorie
        RAISES : NotInListException si course_id n'est pas repertorie dans la liste courses

        :param course_name: str
            nom du cours
        """

        course_id = All_courses.get_object_id(course_name)
        if self.is_in_courses(course_id):
            self.__courses.remove(course_id)
        else:
            raise NotInListException

    def create_file(self, pathname, file_name, script=False, course_name=None, tag=None):
        """Methode permettant la creation d'une nouvelle instance de la classe Files
        et de l'ajouter a la liste des cours auxquels l'utilisateur etudiant est inscrit

        PRE :   - pathname et file_name sont de type str
                - script est de type bool
                - course_name est soit de type str soit None
                - tag est soit de type list soit None
        POST : cree une instance de la classe Files et ajoute son identifiant a la liste files
            ssi celle-ci n'existe pas deja
        RAISES : AlreadyInListException si le fichier est deja repertorie dans la liste files

        :param pathname: str
            Le chemin d'acces vers le fichier sur la memoire locale ou distante
        :param file_name: str
            Le nom et l'extension du fichier sur la memoire locale ou distante
            et le nom permettant d'identifier le fichier
        :param script: bool
            Indique si le fichier est un script
        :param course_name: str
            Le nom du cours auquel le fichier est associe
        :param tag: list
            Liste d'etiquettes associees au fichier
        """

        if tag is None:
            tag = []
        file_instance = Files(file_name, self.user_id, pathname, course_name, script, tag)
        All_files.add_object(file_instance.file_id, file_instance)
        All_files.add_name_id_pair(pathname, file_instance.file_id)
        if not self.is_in_files(file_instance.file_id):
            self.__files.append(file_instance.file_id)
        else:
            raise AlreadyInListException

    def delete_file(self, pathname):
        """Methode permettant la suppression d'une instance de la classe Files,
        de supprimer le fichier de la liste files de son proprietaire,
        s'il est associe a un cours, de le retirer de la liste des fichiers associés a ce cours,
        et, s'il existe, de le supprimer de la memoire locale ou distante

        PRE : file_name est de type str
        POST :  - supprimme l'instance specifiee par pathname ssi elle existait deja
                - supprime l'identifiant du fichier de la liste files de son proprietaire
                - supprime l'identifiant du fichier de la liste files du cours associé ssi le fichier
                    etait associe a un cours
                - supprime le fichier de la memoire locale ou distante ssi il y existait
        RAISES : NotInListException si le fichier n'est pas repertorie dans la liste files de son utilisateur

        :param pathname: str
            Le nom complet du fichier sur la memoire locale ou distante
            et le nom permettant d'identifier le fichier
        """

        file_id = All_files.get_object_id(pathname)
        if self.is_in_files(file_id):
            self.__files.remove(file_id)
        else:
            raise NotInListException
        course_name = All_files.get_object(file_id).course_name
        if course_name is not None:
            course_id = All_courses.get_object_id(course_name)
            All_courses.get_object(course_id).delete_file(file_id)
        if os.path.isfile(pathname):
            os.remove(pathname)
        All_files.delete_object(file_id)
        All_files.delete_name_id_pair(pathname)


class Files:
    """Un fichier existant sur la memoire locale ou distante.
    Il existe une relation d'association bidirectionnelle entre les classes Files et Students,
    ainsi qu'entre les classes Files et Courses

    Attributs:
        name            Le nom et l'extension du fichier sur la memoire locale ou distante
                        et le nom permettant d'identifier le fichier
        script          Indique si le fichier est un script
        file_id         Identifiant unique associe au fichier
        user_id         Identifiant unique associe a l'utilisateur etudiant proprietaire du fichier
        course_name     Le nom du cours auquel le fichier fait reference
        tag             Liste d'etiquettes associees au fichier
        pathname        Le chemin d'acces vers le fichier sur la memoire locale ou distante
    """

    def __init__(self, name, user_id, pathname, course_name, script, tag):
        """Methode permettant d'initialiser chaque instance de la classe
        Si le fichier n'existe pas deja, il est cree a l'emplacement specifie

        PRE :   - name et pathname sont de type str
                - user_id est de type int
                - script est de type bool
                - course_name est soit de type str soit None
                - tag est de type list

        :param name: str
            Le nom et l'extension du fichier sur la memoire locale ou distante
            et le nom permettant d'identifier le fichier
        :param user_id: int
            Identifiant unique associe a l'utilisateur etudiant proprietaire du fichier
        :param pathname: str
            Le chemin d'acces vers le fichier sur la memoire locale ou distante
        :param course_name: str ou None
            Le nom du cours auquel le fichier fait reference
            ou None dans le cas ou le fichier n'est pas associe a un cours
        :param script: bool
            Indique si le fichier est un script
        :param tag: list
            Liste d'etiquettes associees au fichier
        """

        self.__name = name
        self.__script = script
        self.__file_id = FilesIdGenerator.generate_new_id()
        self.__user_id = user_id
        self.__course_name = course_name
        self.__tag = tag
        self.__pathname = pathname
        try:
            with open(self.__pathname, 'x'):
                print(f"Le fichier {pathname} a correctement ete cree")
        except FileExistsError:
            print(f"Le fichier {pathname} existait deja. Il est maintenant connu du programme")
        if self.__course_name is not None:
            course_id = All_courses.get_object_id(self.__course_name).course_id
            All_courses.get_object(course_id).add_file(self.__file_id)

    @property
    def file_id(self):
        """Methode permettant d'acceder a la variable privee file_id

        :return self.__file_id : int
            Identifiant unique associe au fichier
        """

        return self.__file_id

    @property
    def name(self):
        """Methode permettant d'acceder a la variable privee name

        :return self.__name : str
            Le nom et l'extension du fichier sur la memoire locale ou distante
            et le nom permettant d'identifier le fichier
        """

        return self.__name

    @property
    def script(self):
        """Methode permettant d'acceder a la variable privee script

        :return self.__script : bool
            Indique si le fichier est un script
        """

        return self.__script

    @property
    def tag(self):
        """Methode permettant d'acceder a la variable privee tag

        :return self.__tag : list
            Liste d'etiquettes associees au fichier
        """

        return self.__tag

    @property
    def pathname(self):
        """Methode permettant d'acceder a la variable privee pathname

        :return self.__pathname : str
            Le chemin d'acces vers le fichier sur la memoire locale ou distante
        """

        return self.__pathname

    @property
    def user_id(self):
        """Methode permettant d'acceder a la variable privee user_id

        :return self.__user_id : int
            Identifiant unique associe a l'utilisateur etudiant proprietaire du fichier
        """

        return self.__user_id

    @property
    def course_name(self):
        """Methode permettant d'acceder a la variable privee course_name

        :return self.__course_name : str
            Le nom du cours traite dans le fichier
        """

        return self.__course_name

    def is_in_tag(self, tag):
        """Methode permettant de definir si un etiquette est attribuee au fichier

        PRE : tag est de type str
        POST : retourne True si l'etiquette est deja repertoriee dans la liste self.__tag

        :param tag: str
            L'etiquette dont on cherche a savoir si elle est deja attribuee au fichier
        :return: bool
            Indique si l'etiquette est deja attribuee au fichier
        """

        return tag in self.__tag

    def add_tag(self, new_tag):
        """Methode permettant d'ajouter un etiquette a la liste de la variable privee tag

        PRE : new_tag est de type str et n'existe pas deja comme etiquette du fichier
        POST : ajoute l'etiquette a la liste tag ssi elle n'y etait pas deja repertoriee
        RAISES : AlreadyDefinedTagException si l'etiquette est deja repertorie dans la liste

        :param new_tag: str
            Nouvelle etiquette a ajouter a la liste
        """

        if not self.is_in_tag(new_tag):
            self.__tag.append(new_tag)

    def delete_tag(self, tag):
        """Methode permettant de retirer une etiquette de la liste de la variable privee tag

        PRE : tag est de type str et existe deja comme etiquette du fichier
        POST : supprime l'etiquette de la liste tag ssi elle y etait deja repertoriee
        RAISES : NotADefinedTagException si l'etiquette n'est pas deja repertorie dans la liste

        :param tag: str
            Etiquette a retirer de la liste
        """

        if self.is_in_tag(tag):
            self.__tag.remove(tag)

    def move_file(self, new_pathname):
        """Methode permettant de deplacer le fichier sur la memoire locale ou distante
        et de changer la valeur de ses attributs pathname et name en consequence

        PRE : new_pathname est de type str
        POST :  - modifie la valeur des attributs pathname et name du fichier
                - deplace et/ou modifie le nom du fichier sur la memoire locale ou distante ssi le fichier existe
                - modifie le dictionnaire All_files.__name_id_dict pour tenir compte du changement de pathname
        RAISES : FileNotFoundException si le fichier n'existe pas

        :param new_pathname: str
            Nouvelle valeur de pathname
        """

        if os.path.isfile(self.__pathname):
            new_name = os.path.basename(new_pathname)
            self.__name = new_name
            os.rename(self.__pathname, new_pathname)
            All_files.append_name_id_pair(self.__pathname, new_pathname)
            self.__pathname = new_pathname
        else:
            raise FileNotFoundException

    def read_file(self):
        """Methode permettant de lire le contenu d'un fichier sur la memoire locale ou distante

        PRE : le fichier existe
        POST : ouvre le fichier ssi il existe

        :return: A VENIR
            ACTUELLEMENT, LA METHODE NE RETOURNE RIEN MAIS IMPRIME LE CONTENU EN CONSOLE
            EN DEFINITIVE, LA METHODE RETOURNERA LE CONTENU DU FICHIER POUR QU'IL SOIT AFFICHE
            DANS L'EDITEUR DE TEXTE
        """
        try:
            with open(self.__pathname, 'r') as file:
                for line in file:
                    print(line.rstrip())
        except FileNotFoundError:
            print(f'Le fichier {self.__name} est introuvable.')
        except IOError:
            print('Erreur IO.')

    def write_file(self, content_to_write):
        """Methode permettant d'ecrire du contenu dans un fichier sur la memoire locale ou distante

        PRE :   - content_to_write est de type str
                - le fichier existe
        POST : ecrit dans le fichier ssi il existe

        :param content_to_write: str
            Le contenu a ecrire dans le fichier
        """
        try:
            with open(self.__pathname, 'w') as file:
                file.write(content_to_write)
        except FileExistsError:
            print(f"Le fichier {self.__name} n'existe pas")
        except IOError:
            print('Erreur IO.')

    def append_file(self, content_to_append):
        """Methode permettant d'ecrire du contenu dans un fichier sur la memoire locale ou distante,
        a la suite du contenu preexistant

        PRE :   - content_to_append est de type str
                - le fichier existe
        POST : ecrit a la suite du contenu du fichier ssi il existe

        :param content_to_append: str
            Le contenu a ecrire dans le fichier
        """
        try:
            with open(self.__pathname, 'a') as file:
                file.write(content_to_append)
        except FileExistsError:
            print("Le fichier n'existe pas")
        except IOError:
            print('Erreur IO.')


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
    """

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
        self.__course_id = CoursesIdGenerator.generate_new_id()
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

    def delete_teacher(self, name):
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

    def delete_file(self, file_id):
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


class IdGenerator:
    """Cette classe permet de generer les identifiants uniques pour les instances
    des classes Users, Files et Courses

    Attributs:
        id              Compteur d'identifiants uniques
    """

    def __init__(self):
        """Methode permettant d'initialiser chaque instance de la classe"""
        self.__id = 0

    def generate_new_id(self):
        """Methode permettant de generer un identifiant unique en incrementant le compteur id

        :return self.__id : int
            L'identifiant unique genere pour l'instance de la classe Users, Files ou Courses ayant
            appelle la methode
        """
        self.__id += 1
        return self.__id


class Container:
    """Cette classe permet d'enregistrer chaque instance d'une meme classe

    Attributs:
        object_container    Dictionnaire repertoriant toutes les instances d'une meme classe
        name_id_dict        Dictionnaire répertoriant les paires nom <--> id des objets contenus dans object_container
    """

    def __init__(self):
        """Methode permettant d'initialiser chaque instance de la classe"""

        self.__object_container = {}
        self.__name_id_dict = {}

    @property
    def object_container(self):
        """Methode permettant d'acceder a la variable privee object_container

        :return self.__object_container : dict
            Dictionnaire repertoriant toutes les instances d'une meme classe
        """

        return self.__object_container

    @property
    def name_id_dict(self):
        """Methode permettant d'acceder a la variable privee name_id_dict

        :return self.__name_id_dict : dict
            Dictionnaire répertoriant les paires nom <--> id des objets contenus dans object_container
        """

        return self.__name_id_dict

    def is_in_name_id_dict(self, name):
        """Methode permettant de definir si un nom d'objet est deja repertorie dans le dictionnaire

        PRE : name est de type str
        POST : retourne True ssi le nom est repertorie dans le dictionnaire self.__name_id_dict

        :param name: str
            Utilise comme cle dans le dictionnaire
            Correspond au nom de l'objet recherche
        :return: bool
            Indique si name est une cle du dictionnaire
        """

        return name in self.__name_id_dict

    def is_in_object_container(self, obj_id):
        """Methode permettant de definir si un identifiant est deja repertorie dans le dictionnaire

        PRE : obj_id est de type int
        POST : retourne True ssi l'identifiant unique est repertorie dans le dictionnaire self.__object_container

        :param obj_id: int
            Utilise comme cle dans le dictionnaire
            Correspond a l'identifiant unique de l'objet recherche
        :return: bool
            Indique si obj_id est une cle du dictionnaire
        """

        return obj_id in self.__object_container

    def add_name_id_pair(self, name, obj_id):
        """Methode permettant d'ajouter une paire {name: obj_id} dans self.__name_id_dict

        PRE :   - name est de type str
                - obj_id est de type int
                - name ne correspond pas deja a une cle du dictionnaire
        POST : ajoute la paire {name: obj_id} au dictionnaire ssi name n'est pas deja une cle du dictionnaire
        RAISES : ObjectAlreadyExistantException si name correspond deja a aucune cle du dictionnaire

        :param name: str
            Utilise comme cle dans le dictionnaire
            Correspond au nom de l'objet recherche
            ### ATTENTION ! Dans le cas des fichiers, name ne correspond pas au nom du fichier mais a son pathname !
        :param obj_id: int
            Correspond a l'identifiant unique de l'objet a repertorier
        """

        if not self.is_in_name_id_dict(name):
            self.__name_id_dict[name] = obj_id
        else:
            raise ObjectAlreadyExistantException

    def append_name_id_pair(self, current_name, new_name):
        """Methode permettant de modifier la cle d'une paire {current_name: obj_id} dans self.__name_id_dict

        PRE : current_name et new_name sont de type str
        POST : modifie la cle de la paire {current_name: obj_id} du dictionnaire ssi la cle est deja repertorie
            dans le dictionnaire
        RAISES : UnknownKeyException si la cle n'est pas repertoriee dans le dictionnaire

        :param current_name: str
            Utilise comme cle dans le dictionnaire
            Correspond au nom de l'objet recherche
        :param new_name: str
            Future cle dans le dictionnaire pour l'objet
        :return:
        """
        if self.is_in_name_id_dict(current_name):
            All_files.name_id_dict[new_name] = All_files.name_id_dict.pop(current_name)
        else:
            raise UnknownKeyException

    def add_object(self, obj_id, obj):
        """Methode permettant d'ajouter un element dans le dictionnaire object_container

        PRE :   - obj_id est de type int
                - obj est une instance de classe
                - obj_id ne correspond pas deja a une cle du dictionnaire
        POST : ajoute la paire {obj_id: obj} au dictionnaire ssi obj_id n'est pas deja une cle du dictionnaire
        RAISES : ObjectAlreadyExistantException si obj_id correspond deja a aucune cle du dictionnaire

        :param obj_id: int
            Utilise comme cle dans le dictionnaire.
            Correspond a l'identifiant unique de l'instance de la classe que la cle repertorie
        :param obj: object
            L'instance de la classe a repertorier
        """

        if not self.is_in_object_container(obj_id):
            self.__object_container[obj_id] = obj
        else:
            raise ObjectAlreadyExistantException

    def get_object_id(self, name):
        """Methode permettant de recupere l'identifiant unique d'un objet sur base de son nom

        PRE : name est de type str et correspond a une cle du dictionnaire name_id_dict
        POST : retourne l'identifiant unique de l'objet recherche ssi name correspond a une cle du dictionnaire
        RAISES : UnknownObjectNameException si name ne correspond a aucune cle du dictionnaire

        :param name: str
            Utilise comme cle dans le dictionnaire
            Correspond au nom de l'objet
        :return obj_id : int
            Correspond a l'identifiant unique de l'objet recherche
        """

        if self.is_in_name_id_dict(name):
            return self.__name_id_dict[name]
        else:
            raise UnknownObjectNameException

    def get_object(self, obj_id):
        """Methode permettant de recuperer, dans le dictionnaire,
        l'instance d'une classe sur base de son identifiant unique

        PRE : obj_id est de type int et correspond a une cle du dictionnaire object_container
        POST : retourne l'objet recherche ssi obj_id correspond a une cle du dictionnaire
        RAISES : UnknownObjectIdException si obj_id ne correspond a aucune cle du dictionnaire

        :param obj_id: int
            Correspond a l'identifiant unique de l'instance de la classe que la cle repertorie

        :return self.__object_container[name] : object
            L'instance de la classe recherchee
        """

        if self.is_in_object_container(obj_id):
            return self.__object_container[obj_id]
        else:
            raise UnknownObjectIdException

    def delete_object(self, obj_id):
        """Methode permettant de supprimer un element du dictionnaire object_container sur base de sa cle

        PRE : obj_id est de type int et correspond a une cle du dictionnaire object_container
        POST : supprime l'objet du dictionnaire ssi obj_id correspond a une cle du dictionnaire
        RAISES : UnknownObjectIdException si obj_id ne correspond a aucune cle du dictionnaire

        :param obj_id: int
            L'identifiant unique de l'element a supprimer.
            Correspond a la cle de l'objet a supprimer dans le dictionnaire
        """

        if self.is_in_object_container(obj_id):
            del self.__object_container[obj_id]
        else:
            raise UnknownObjectIdException

    def delete_name_id_pair(self, name):
        """Methode permettant de supprimer un element du dictionnaire name_id_dict sur base de sa cle

        PRE : name est de type str et correspond a une cle du dictionnaire name_id_dict
        POST : supprime l'objet du dictionnaire ssi name correspond a une cle du dictionnaire
        RAISES : UnknownObjectNameException si name ne correspond a aucune cle du dictionnaire

        :param name: str
            Le nom de l'element a supprimer.
            Correspond a la cle de l'objet a supprimer dans le dictionnaire
            ### ATTENTION ! Dans le cas des fichiers, name ne correspond pas au nom du fichier mais a son pathname !
        """

        if self.is_in_name_id_dict(name):
            del self.__name_id_dict[name]
        else:
            raise UnknownObjectNameException


class UnknownKeyException(Exception):
    pass


class UnknownPasswordException(Exception):
    pass


class UnknownObjectNameException(Exception):
    pass


class UnknownObjectIdException(Exception):
    pass


class ObjectAlreadyExistantException(Exception):
    pass


class AlreadyInListException(Exception):
    pass


class NotInListException(Exception):
    pass


class AlreadyDefinedTagException(Exception):
    pass


class NotADefinedTagException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


"""Creation des instances de la classe Container
necessaires pour enregistrer les instances des classes associees"""
with open("pickle_saves/students.pkl", 'rb') as all_students_file:
    All_students = pickle.load(all_students_file)
with open("pickle_saves/admins.pkl", 'rb') as all_admins_file:
    All_admins = pickle.load(all_admins_file)
with open("pickle_saves/files.pkl", 'rb') as all_files_file:
    All_files = pickle.load(all_files_file)
with open("pickle_saves/courses.pkl", 'rb') as all_courses_file:
    All_courses = pickle.load(all_courses_file)

# All_students = Container()
# All_admins = Container()
# All_files = Container()
# All_courses = Container()

"""Creation des instances de la classe IdGenerator
necessaires pour creer les identifiants uniques des classes associees"""
UsersIdGenerator = IdGenerator()
FilesIdGenerator = IdGenerator()
CoursesIdGenerator = IdGenerator()
