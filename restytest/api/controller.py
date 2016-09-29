""" RestyTest Controller """

from restytest import exceptions
from restytest import models
from restytest import storage
from restytest.api import validations


def _to_group(group_name, data):
    return models.Group(
        group_id=group_name,
        users=[u for u in data.get('userids', [])]
    )


def _to_user(data):
    return models.User(
        user_id=data['userid'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        groups=[g for g in data['groups']]
    )


class Controller(object):
    def __init__(self):
        self.db = storage.Storage()

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
        validations.validate_user(data)
        validations.validate_userid(userid)
        user = _to_user(data)
        self._get_user_or_raise(userid)
        return self.db.update_user(userid, user)

    def delete_user(self, userid):
        validations.validate_userid(userid)
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
        self._get_group_or_raise(group_name)
        return self.db.update_group(group_name, group)

    def delete_group(self, group_name):
        validations.validate_group_name(group_name)
        self._get_group_or_raise(group_name)
        self.db.delete_group(group_name)
