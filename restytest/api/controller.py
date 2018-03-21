""" RestyTest Controller """

from restytest import exceptions
from restytest import models
from restytest import storage
from restytest.api import validations

# These belong in restytest.models... not here!
def _to_group(group_name, data):
    return models.Group(
        group_id=group_name,
        users=[u for u in data.get('userids', [])] # Why did you use a list comprehension here? Isn't this just data.get('userids', [])
    )


def _to_user(data):
    return models.User(
        user_id=data['userid'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        groups=[g for g in data['groups']] # Same question here... what?
    )


class Controller(object):
    def __init__(self):
        self.db = storage.Storage()

    # Feedback: Don't like that you're using exceptions as flow control here. The problem starts here with that whole pattern.
    # why not just return None and let the view decide what to do with a None?
    def _get_user_or_raise(self, userid):
        user = self.db.get_user(userid)
        if not user:
            raise exceptions.UserNotFound()
        return user

    def _get_group_or_raise(self, group_name):
        group = self.db.get_group(group_name)
        if not group:
            raise exceptions.GroupNotFound()
        return group

    def create_user(self, data):
        validations.validate_user(data)
        user = _to_user(data)
        if self.db.get_user(user.user_id):
            raise exceptions.ResourceAlreadyExists()
        return self.db.create_user(user)

    def get_user(self, userid):
        validations.validate_userid(userid)
        return self._get_user_or_raise(userid)

    def update_user(self, userid, data):
        # Why is the userid not in the data? Why is the double validation
        validations.validate_user(data)
        validations.validate_userid(userid)
        user = _to_user(data)
        self._get_user_or_raise(userid)
        return self.db.update_user(userid, user)

    def delete_user(self, userid):
        # Question: Why validate here?
        # Answer: Circuit-breaker to avoid dirty inputs getting to the backend.
        validations.validate_userid(userid)
        # These could be better documented or broken apart
        # Feedback: You could still have a get_user_or_raise, or maybe have a function raise_for_user... it's confusing that you're calling a function
        # to get a user object, but doing nothing with it - you're only using it for the side-effect. Maybe that's where self._raise_for_user
        # would be more appropriate, so it's not returning anything at all, but raising if that user doesn't exist.
        self._get_user_or_raise(userid)
        self.db.delete_user(userid)

    def create_group(self, data):
        validations.validate_group_post(data)
        group = _to_group(data['name'], data)
        if self.db.get_group(group.group_id):
            raise exceptions.ResourceAlreadyExists()
        return self.db.create_group(group)

    def get_group(self, group_name):
        validations.validate_group_name(group_name)
        return self._get_group_or_raise(group_name)

    def update_group(self, group_name, data):
        validations.validate_group_put(data)
        validations.validate_group_name(group_name)
        group = _to_group(group_name, data)
        # Needs a comment to specify why this is being done.
        self._get_group_or_raise(group_name)
        return self.db.update_group(group_name, group)

    def delete_group(self, group_name):
        validations.validate_group_name(group_name)
        self._get_group_or_raise(group_name)
        self.db.delete_group(group_name)
