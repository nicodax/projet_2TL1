class UnknownPasswordException(Exception):
    """Exception generee lorsque un mot de passe entre par l'utilisateur ne correspond pas a un mot de passe connu"""
    pass


class AlreadyInListException(Exception):
    """Exception generee lorsque l'utilisateur tente d'ajouter dans une liste un element qui y existe deja"""
    pass


class NotInListException(Exception):
    """Exception generee lorsque l'utilisateur tente de supprimer d'une liste un element qui n'y existe pas"""
    pass
