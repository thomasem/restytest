""" Common exceptions """


class UserNotFound(Exception):
    pass


class GroupNotFound(Exception):
    pass


class ValidationError(Exception):
    pass


class AlreadyExists(Exception):
    pass
