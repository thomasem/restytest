""" RestyTest Controller """

from restytest import exceptions
from restytest import models
from restytest import storage
from restytest.api import validations


def _to_group(data):
    return models.Group(
        group_id=data['name']
    )


def _to_user(data):
    return models.Group(
        user_id=data['userid'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        groups=[g for g in data['groups']]
    )


class Controller(object):
    def __init__(self):
        self.db = storage.Storage()

    def create_user(self, data):
        validations.validate_user(data)
        user = _to_user(data)

        if self.db.get_user(user.group_id):
            raise exceptions.ResourceAlreadyExists()

        return self.db.create_user(user)

    def get_user(self, userid):
        validations.validate_userid(userid)
        user = self.db.get_user(userid)
        if not user:
            raise exceptions.UserNotFound()
        return user

    def update_user(self, updated):
        # validate
        # store updates
        # return updated from view
        pass

    def delete_user(self, userid):
        # validate user_id
        # delete
        # return no content
        pass

    def create_group(self, data):
        validations.validate_group(data)
        group = _to_group(data)

        if self.db.get_group(group.group_id):
            raise exceptions.ResourceAlreadyExists()

        return self.db.create_group(group)

    def get_group(self, group_name):
        validations.validate_group_name(group_name)
        group = self.db.get_group(group_name)
        if not group:
            raise exceptions.GroupNotFound()
        return group

    def update_group(self, updated):

        pass

    def delete_group(self, group_name):
        # validate group_name
        # delete
        # return no content
        pass
