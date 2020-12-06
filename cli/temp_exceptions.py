#!/usr/bin/env python3
class ArgumentException(Exception):
    pass


class FileNotOwnedException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


class UnknownUsernameException(Exception):
    pass


class IncorrectUseOfArgumentsException(Exception):
    pass


class ObjectAlreadyExistantException(Exception):
    pass


class PasswordNotEqualException(Exception):
    pass


class UnknownObjectException(Exception):
    pass


class ImpossibleToDeleteUserException(Exception):
    pass
