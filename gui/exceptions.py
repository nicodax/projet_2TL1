#!/usr/bin/env python3


class UserNameNotFoundException(Exception):
    """Exception generee lorsque le nom utilisateur n est pas reconnu."""
    pass


class SamePathnameException(Exception):
    """Exception generee lorsque l'ancien pathname et le nouveau sont les memes."""
    pass