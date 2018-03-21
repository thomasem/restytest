""" Common exceptions """

# Feedback: Inconsistent naming might be a little awkward to work with.
class UserNotFound(Exception):
    pass


class GroupNotFound(Exception):
    pass


class ValidationError(Exception):
    pass


class ResourceAlreadyExists(Exception):
    pass

# Either get rid of this, or make it a subclass of ValidationError (I'd personally get rid of it).
class InvalidIdentifier(Exception):
    pass
