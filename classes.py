#! usr/bin/env python3

# TO DO :
#       - Inclure les lignes specifiees en bas du script dans le main.py
#       - Gestion des erreurs --> pas utiliser print mais generer une erreur en console
#       _ Files.read_file --> gestion du retour de la methode

import os


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

        :param new_username: str
            Nouvelle valeur de username
        """
        self.__username = new_username

    @fullname.setter
    def fullname(self, new_fullname):
        """Methode permettant de modifier la valeur de la variable privee fullname

        :param new_fullname: str
            Nouvelle valeur de fullname
        """
        self.__fullname = new_fullname

    def pwd(self, old_pwd, new_pwd):
        """Methode permettant de modifier la valeur de la variable privee pwd.
        La demande de modification n'est prise en compte que si le mot de passe actuel est precise

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

        :param pwd: str
            Le mot de passe a verifier

        :return: bool
            Indique si le mot de passe entre par l'utilisateur correspond au mot de passe enregistre
        """
        return self.__pwd == pwd


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

        :param username: str
            Le nom permettant d'identifier le futur utilisateur etudiant
        :param fullname: str
            Le nom complet du futur utilisateur etudiant
        :param pwd: str
            Le mot de passe associe au futur utilisateur etudiant
        """
        All_students.add_object(username, Students(username, fullname, pwd))

    @staticmethod
    def delete_student(username):
        """Methode statique permettant la suppression d'une instance de la classe Students

        :param username: str
            Le nom permettant d'identifier l'utilisateur etudiant
        """
        All_students.delete_object(username)

    @staticmethod
    def create_admin(username, fullname, pwd):
        """Methode statique permettant la creation d'une nouvelle instance de la classe Admins

        :param username: str
            Le nom permettant d'identifier le futur utilisateur administrateur
        :param fullname: str
            Le nom complet du futur utilisateur administrateur
        :param pwd: str
            Le mot de passe associe au futur utilisateur administrateur
        """
        All_admins.add_object(username, Admins(username, fullname, pwd))

    @staticmethod
    def delete_admin(username):
        """Methode statique permettant la suppression d'une instance de la classe Admins

        :param username: str
            Le nom permettant d'identifier l'utilisateur administrateur
        """
        All_admins.delete_object(username)

    @staticmethod
    def create_course(name, teachers):
        """Methode statique permettant la creation d'une nouvelle instance de la classe Courses

        :param name: str
            L'intitule permettant d'identifier le cours
        :param teachers: list
            Liste les noms (str) des professeurs titulaires du cours
        """
        All_courses.add_object(name, Courses(name, teachers))

    @staticmethod
    def delete_course(name):
        """Methode statique permettant la suppression d'une instance de la classe Courses

        :param name: str
            L'intitule permettant d'identifier le cours
        """
        All_courses.delete_object(name)


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

    def add_course(self, course_id):
        """Methode permettant d'inscrire l'utilisateur etudiant a un cours

        :param course_id: int
            Identifiant unique associe au cours
        """
        self.__courses.append(course_id)

    def delete_course(self, course_id):
        """Methode permettant de desinscrire l'utilisateur etudiant d'un cours

        :param course_id: int
            Identifiant unique associe au cours
        """
        self.__courses.remove(course_id)

    def create_file(self, pathname, file_name, script, course_name=None, tag=None):
        """Methode permettant la creation d'une nouvelle instance de la classe Files
        et de l'ajouter a la liste des cours auxquels l'utilisateur etudiant est inscrit

        :param pathname: str
            Le chemin d'acces vers le fichier sur la memoire locale ou distante
        :param file_name: str
            Le nom et l'extension du fichier sur la memoire locale ou distante
            et le nom permettant d'identifier le fichier
        :param script: bool
            Indique si le fichier est un script
        :param course_name: str
            Le nom du cours auquel le fichier est associe
        :param tag: str
            L'etiquette associee au fichier
        """
        All_files.add_object(file_name, Files(file_name, self.user_id, pathname, course_name, script, tag))
        self.__files.append(All_files.get_object(file_name).file_id)

    def delete_file(self, file_name):
        """Methode permettant la suppression d'une instance de la classe Files,
        de le retirer de la liste des cours auxquels l'utilisateur etudiant est inscrit
        et, s'il esxiste, de le supprimer de la memoire locale ou distante

        :param file_name: str
            Le nom et l'extension du fichier sur la memoire locale ou distante
            et le nom permettant d'identifier le fichier
        """
        file_id = All_files.get_object(file_name).file_id
        self.__files.remove(file_id)
        course_name = All_files.get_object(file_name).course_name
        if course_name is not None:
            All_courses.get_object(course_name).delete_file(file_id)
        pathname = All_files.get_object(file_name).pathname
        if os.path.exists(pathname):
            os.remove(pathname)
        All_files.delete_object(file_name)


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
        tag             L'etiquette associee au fichier
        pathname        Le chemin d'acces vers le fichier sur la memoire locale ou distante
    """
    def __init__(self, name, user_id, pathname, course_name, script=False, tag=None):
        """Methode permettant d'initialiser chaque instance de la classe
        Si le fichier n'existe pas deja, il est cree a l'emplacement specifie

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
        :param tag: str
            L'etiquette associee au fichier
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
                pass
        except FileExistsError:
            pass
        if self.__course_name is not None:
            All_courses.get_object(self.__course_name).add_file(self.__file_id)

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

        :return self.__tag : str
            L'etiquette associee au fichier
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

    @tag.setter
    def tag(self, new_tag):
        """Methode permettant de modifier la valeur de la variable privee tag

        :param new_tag: str
            Nouvelle valeur de tag
        """
        self.__tag = new_tag

    def rename(self, new_name):
        """Methode permettant de renommer le fichier sur la memoire locale ou distante
        et de changer les valeurs de ses attributs name et pathname en consequence

        :param new_name: str
            Nouvelle valeur de name
        """
        self.__name = new_name
        new_pathname = os.path.dirname(self.__pathname) + "/" + new_name
        os.rename(self.__pathname, new_pathname)
        self.__pathname = new_pathname

    def move_file(self, new_pathname):
        """Methode permettant de deplacer le fichier sur la memoire locale ou distante
        et de changer la valeur de son attribut pathname

        :param new_pathname: str
            Nouvelle valeur de pathname
        """
        os.rename(self.__pathname, new_pathname)
        self.__pathname = new_pathname

    def read_file(self):
        """Methode permettant de lire le contenu d'un fichier sur la memoire locale ou distante

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

    def add_teacher(self, name):
        """Methode permettant d'ajouter le nom d'un professeur a la liste des
        professeurs titulaires du cours

        :param name: str
            Le nom du professeur
        """
        self.__teachers.append(name)

    def delete_teacher(self, name):
        """Methode permettant de supprimer le nom d'un professeur de la liste
        des professeurs titulaires du cours

        :param name: str
            Le nom du professeur
        """
        self.__teachers.remove(name)

    def add_file(self, file_id):
        """Methode permettant d'ajouter l'identifiant unique d'un fichier a la liste
        des fichiers associes au cours.
        Cette méthode est apellee automatiquement par la classe Files lors de l'initialisation :
        elle ne doit donc JAMAIS etre apellee directement

        :param file_id: int
            L'identifiant unique du fichier se rapportant au cours
        """
        self.__files.append(file_id)

    def delete_file(self, file_id):
        """Methode permettant de supprimer l'identifiant unique d'un fichier a la liste
        des fichiers associes au cours.
        Cette méthode est apellee automatiquement par la classe Students lors de la suppression d'un fichier :
        elle ne doit donc JAMAIS etre apellee directement

        :param file_id: int
            L'identifiant unique du fichier se rapportant au cours
        """
        self.__files.remove(file_id)


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
    """
    def __init__(self):
        """Methode permettant d'initialiser chaque instance de la classe"""
        self.__object_container = {}

    def add_object(self, name, obj):
        """Methode permettant d'ajouter un element dans le dictionnaire object_container

        :param name: str
            Utilise comme cle dans le dictionnaire.
            Correspond a l'attribut name de l'instance de la classe que la cle repertorie
        :param obj: object
            L'instance de la classe a repertorier
        """
        self.__object_container[name] = obj

    def get_object(self, name):
        """Methode permettant de recuperer, dans le dictionnaire,
        l'instance d'une classe sur base de son attribut name

        :param name: str
            L'attribut name de la classe recherchee.
            Correspond a la cle de l'element recherche dans le dictionnaire

        :return self.__object_container[name] : object
            L'instance de la classe recherchee
        """
        return self.__object_container[name]

    def delete_object(self, name):
        """Methode permettant de supprimer un element du dictionnaire sur base de sa cle

        :param name: str
            L'attribut name de l'element a supprimer.
            Correspond a l'attribut name de l'instance de la classe a supprimer
        """
        del self.__object_container[name]


if __name__ == '__main__':
    # A METTRE DANS LE MAIN.PY PAR LA SUITE
    """Creation des instances de la classe Container
    necessaires pour enregistrer les instances des classes associees"""
    All_files = Container()
    All_users = Container()
    All_admins = Container()
    All_courses = Container()
    All_students = Container()

    """Creation des instances de la classe IdGenerator
    necessaires pour creer les identifiants uniques des classes associees"""
    UsersIdGenerator = IdGenerator()
    FilesIdGenerator = IdGenerator()
    CoursesIdGenerator = IdGenerator()

    # TESTS

    Dax = Students("dax", "Nicolas Daxhelet", "user123")
    Daxxra = Admins("daxxra", "Nicolas Daxhelet", "user124")

    """ATTENTION : les pathnames suivants sont valables uniquement sur la machine de Nicolas Daxhelet"""
    print('# README.md : \n')

    Dax.create_file("//wsl$/Ubuntu-20.04/home/daxxramass/EPHEC/BLOC2/T2012/projet_2TL1/README.md", "README.md", False)
    All_files.get_object("README.md").read_file()

    print('\n# hello_world.txt : \n')

    Dax.create_file("//wsl$/Ubuntu-20.04/home/daxxramass/EPHEC/BLOC2/T2012/hello_world.txt", "hello_world.txt", False)
    All_files.get_object("hello_world.txt").write_file("Hello World !\nNew line here...")
    All_files.get_object("hello_world.txt").append_file("\nAnd another here...")
    All_files.get_object("hello_world.txt").read_file()
    Dax.delete_file("hello_world.txt")
