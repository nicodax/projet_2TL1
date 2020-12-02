#!/usr/bin/env python3

class UnknownPasswordException(Exception):
    pass


class AlreadyInListException(Exception):
    pass


class NotInListException(Exception):
    pass


class ObjectAlreadyExistantException(Exception):
    pass


class UnknownObjectNameException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


class FileNotOwnedException(Exception):
    pass
