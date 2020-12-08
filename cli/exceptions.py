#!/usr/bin/env python3
class ArgumentException(Exception):
    """Exception generee lorsqu'un un utilisateur ne respecte pas la syntaxe d'une commande"""
    pass


class FileNotOwnedException(Exception):
    """Exception generee lorsqu'un fichier n'appartient pas a l'utilisateur connecte"""
    pass


class FileNotFoundException(Exception):
    """Exception generee lorsque l'utilisateur tente d'acceder a un fichier inexistant"""
    pass


class UnknownUsernameException(Exception):
    """Exception generee lorsqu'un utilisateur tente de se connecter avec un username inconnu"""
    pass


class IncorrectUseOfArgumentsException(Exception):
    """Exception generee lorsque les arguments de la fonction pickle_get_instance sont mal utilises"""
    pass


class ObjectAlreadyExistantException(Exception):
    """Exception generee lorsque l'utilisateur tente de creer une instance de classe qui existe deja"""
    pass


class PasswordNotEqualException(Exception):
    """Exception generee lorsque l'utilisateur tente de creer un nouvel utilisateur et que la confirmation de mot
    de passe ne correspond pas avec le mot de passe initialement entre"""
    pass


class UnknownObjectException(Exception):
    """Exception generee lorsque l'utilisateur tente d'acceder a une instance de classe inconnue"""
    pass


class ImpossibleToDeleteUserException(Exception):
    """Exception generee soit lorsque l'utilisateur tente de suprimmer un utilisateur defini dans le fichier
    cli.reset.py, soit lorsque l'utilisateur tente de se supprimer lui meme"""
    pass


class InexistantDirectoryException(Exception):
    """Exception generee lorsque l'utilisateur tente de creer un fichier dans un repertoire n'existant pas"""
    pass
