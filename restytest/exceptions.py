""" Common exceptions """


class UserNotFound(Exception):
    pass


class GroupNotFound(Exception):
    pass


class ValidationError(Exception):
    pass


class ResourceAlreadyExists(Exception):
    pass


class InvalidIdentifier(Exception):
    pass
