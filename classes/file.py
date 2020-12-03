#!/usr/bin/env python3
from classes.exceptions import AlreadyInListException, NotInListException


class File:
    """Un fichier existant sur la memoire locale ou distante.
    Il existe une relation d'association bidirectionnelle entre les classes Files et Students,
    ainsi qu'entre les classes Files et Courses

    Attributs:
        script          Indique si le fichier est un script
        file_id         Identifiant unique associe au fichier
        user_id         Identifiant unique associe a l'utilisateur etudiant proprietaire du fichier
        course_id       L'identifiant unique du cours auquel le fichier fait reference
        tags             Liste d'etiquettes associees au fichier
        pathname        Le chemin d'acces vers le fichier sur la memoire locale ou distante

    Variables de classe:
        file_id_counter     Compteur necessaire a la creation d'identifiants uniques
    """
    file_id_counter = 0

    def __init__(self, user_id, pathname, course_id, script, tags):
        """Methode permettant d'initialiser chaque instance de la classe
        Si le fichier n'existe pas deja, il est cree a l'emplacement specifie

        PRE :   - user_id est de type int
                - script est de type bool
                - course_id est soit de type int soit None
                - tag est de type list

        :param user_id: int
            Identifiant unique associe a l'utilisateur etudiant proprietaire du fichier
        :param pathname: str
            Le chemin d'acces vers le fichier sur la memoire locale ou distante
        :param course_id: int ou None
            L'identifiant unique du cours auquel le fichier fait reference
            ou None dans le cas ou le fichier n'est pas associe a un cours
        :param script: bool
            Indique si le fichier est un script
        :param tags: list
            Liste d'etiquettes associees au fichier
        """

        if tags is None:
            tags = []
        self.__script = script
        self.__file_id = File.file_id_counter
        File.file_id_counter += 1
        self.__user_id = user_id
        self.__course_id = course_id
        self.__tag = tags
        self.__pathname = pathname
        try:
            with open(self.__pathname, 'x'):
                print(f"Le fichier {pathname} a correctement ete cree")
        except FileExistsError:
            pass

    @property
    def file_id(self):
        """Methode permettant d'acceder a la variable privee file_id

        :return self.__file_id : int
            Identifiant unique associe au fichier
        """

        return self.__file_id

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
    def course_id(self):
        """Methode permettant d'acceder a la variable privee course_name

        :return self.__course_id : int
            Le nom du cours traite dans le fichier
        """

        return self.__course_id

    @pathname.setter
    def pathname(self, new_pathname):
        """Methode permettant de modifier la valeur de la variable privee fullname

        PRE : new_pathname est de type str

        :param new_pathname: str
            Nouvelle valeur de pathname
        """

        self.__pathname = new_pathname

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
        RAISES : AlreadyInListException si l'etiquette est deja repertorie dans la liste

        :param new_tag: str
            Nouvelle etiquette a ajouter a la liste
        """

        if not self.is_in_tag(new_tag):
            self.__tag.append(new_tag)
        else:
            raise AlreadyInListException

    def delete_tag(self, tag):
        """Methode permettant de retirer une etiquette de la liste de la variable privee tag

        PRE : tag est de type str et existe deja comme etiquette du fichier
        POST : supprime l'etiquette de la liste tag ssi elle y etait deja repertoriee
        RAISES : NotInListException si l'etiquette n'est pas deja repertorie dans la liste

        :param tag: str
            Etiquette a retirer de la liste
        """

        if self.is_in_tag(tag):
            self.__tag.remove(tag)
        else:
            raise NotInListException

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
            print(f'Le fichier {self.__pathname} est introuvable.')
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
            print(f"Le fichier {self.__pathname} n'existe pas")
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
