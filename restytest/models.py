""" Application models """


class User(object):
    def __init__(self, user_id, first_name, last_name, groups=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.groups = groups if groups else [] # self.groups = groups or [], less to type, not repeating yourself.


class Group(object):
    def __init__(self, group_id, users=None):
        self.group_id = group_id
        self.users = users if users else [] # self.users = users or [], less to type, not repeating yourself.
