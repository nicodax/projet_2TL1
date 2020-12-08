#!/usr/bin/env python3
from classes.exceptions import AlreadyInListException, NotInListException


class File:
    """Un fichier existant sur la memoire.
    Il existe une relation d'association bidirectionnelle entre les classes Files et Students,
    ainsi qu'entre les classes Files et Courses

    Attributs:
        script          Indique si le fichier est un script
        file_id         Identifiant unique associe au fichier
        user_id         Identifiant unique associe a l'utilisateur etudiant proprietaire du fichier
        course_id       L'identifiant unique du cours auquel le fichier fait reference
        tags            Liste d'etiquettes associees au fichier
        pathname        Le chemin d'acces vers le fichier sur la memoire locale ou distante
    """

    def __init__(self, user_id, pathname, course_id, file_id, script, tags):
        """Methode permettant d'initialiser chaque instance de la classe

        PRE :   - user_id est de type int
                - pathname est de type str
                - script est de type bool
                - course_id est soit de type int soit None
                - tags est soit de type list soit None
                - file_id est de type int
        POST : cree le fichier sur la memoire si il n'y existait pas deja
        """

        if tags is None:
            tags = []
        self.__script = script
        self.__file_id = file_id
        self.__user_id = user_id
        self.__course_id = course_id
        self.__tags = tags
        self.__pathname = pathname
        try:
            with open(self.__pathname, 'x'):
                print(f"Le fichier {pathname} a correctement ete cree")
        except FileExistsError:
            pass

    @property
    def file_id(self):
        """Methode permettant d'acceder a self.__file_id"""

        return self.__file_id

    @property
    def script(self):
        """Methode permettant d'acceder a self.__script"""

        return self.__script

    @property
    def tags(self):
        """Methode permettant d'acceder a self.__tags"""

        return self.__tags

    @property
    def pathname(self):
        """Methode permettant d'acceder a self.__pathname"""

        return self.__pathname

    @property
    def user_id(self):
        """Methode permettant d'acceder a self.__user_id"""

        return self.__user_id

    @property
    def course_id(self):
        """Methode permettant d'acceder a self.__course_name"""

        return self.__course_id

    @pathname.setter
    def pathname(self, new_pathname):
        """Methode permettant de modifier la valeur de self.__fullname

        PRE : new_pathname est de type str
        """

        self.__pathname = new_pathname

    @course_id.setter
    def course_id(self, new_course_id):
        """Methode permettant de modifier la valeur de self.__course_id

        PRE : new_course_id est de type int
        """

        self.__course_id = new_course_id

    @script.setter
    def script(self, new_value):
        """Methode permettant de modifier la valeur de self.__script

        PRE : new_value est de type bool
        """

        self.__script = new_value

    @tags.setter
    def tags(self, new_tags):
        """Methode permettant de modifier la valeur de self.__tags

        PRE : new_tags est de type list
        """

        self.__tags = new_tags

    def is_in_tags(self, tag):
        """Methode permettant de definir si un etiquette est attribuee au fichier

        PRE : tag est de type str
        POST : retourne True si l'etiquette est deja repertoriee dans la liste self.__tags, retourne False sinon
        """

        return tag in self.__tags

    def add_tag(self, new_tag):
        """Methode permettant d'ajouter un etiquette a la liste de la variable privee tag

        PRE : new_tag est de type str
        POST : ajoute l'etiquette a la liste self.__tags ssi elle n'y etait pas deja repertoriee
        RAISES : AlreadyInListException si l'etiquette est deja repertorie dans la liste
        """

        if not self.is_in_tags(new_tag):
            self.__tags.append(new_tag)
        else:
            raise AlreadyInListException

    def delete_tag(self, tag):
        """Methode permettant de retirer une etiquette de la liste de la variable privee tag

        PRE : tag est de type str et existe deja comme etiquette du fichier
        POST : supprime l'etiquette de la liste self.__tags ssi elle y etait deja repertoriee
        RAISES : NotInListException si l'etiquette n'est pas deja repertorie dans la liste
        """

        if self.is_in_tags(tag):
            self.__tags.remove(tag)
        else:
            raise NotInListException
