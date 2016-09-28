""" Data Access """

import sqlalchemy as sa

from restytest import models
from restytest.storage import schema


MEMORY_URI = 'sqlite://'


def _to_user(user, assocs):
    return models.User(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        groups=[a.group_id for a in assocs]
    )


def _to_group(group, assocs):
    return models.Group(
        group_id=group.id,
        users=[a.user_id for a in assocs]
    )


class Storage(object):
    def __init__(self):
        engine = sa.create_engine(MEMORY_URI)
        schema.metadata.create_all(engine)
        self.conn = engine.connect()

        # NOTE(thomasem): SQLite needs to have Foreign Key constraints enabled
        # as they aren't on by default.
        self.conn.execute('PRAGMA foreign_keys=ON')

    def _transaction(self, series):
        trans = self.conn.begin()
        try:
            for query in series:
                self.conn.execute(*query)
            trans.commit()
        except:
            trans.rollback()
            raise

    def get_user(self, user_id):
        # NOTE(thomasem): Willing to make two queries because it's in-memory.
        # for a persistent storage solution, would want to use functionality
        # that's not available for an in-memory solution, such as sub-query and
        # array casting, if possible.
        user_select = schema.users.select().where(schema.users.c.id == user_id)
        groups_select = schema.user_group_associations.select().where(
            schema.user_group_associations.c.user_id == user_id
        )
        user = self.conn.execute(user_select).fetchone()
        assocs = self.conn.execute(groups_select)
        return _to_user(user, assocs) if user else None

    def create_user(self, user):
        user_id = user.user_id
        user_insert = schema.users.insert().values(
            id=user_id,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        groups_values = [
            {
                "user_id": user_id,
                "group_id": group_id
            }
            for group_id in user.groups
        ]

        series = [(user_insert,)]
        if groups_values:
            series.append(
                (schema.user_group_associations.insert(), groups_values)
            )

        self._transaction(series)

        return self.get_user(user_id)

    def delete_user(self, user_id):
        delete = schema.users.delete().where(schema.users.c.id == user_id)
        self.conn.execute(delete)

    def get_group(self, group_id):
        # NOTE(thomasem): Willing to make two queries because it's in-memory.
        # for a persistent storage solution, would want to use functionality
        # that's not available for an in-memory solution, such as sub-query and
        # array casting, if possible.
        group_select = schema.groups.select()
        group_select = group_select.where(schema.groups.c.id == group_id)
        users_select = schema.user_group_associations.select().where(
            schema.user_group_associations.c.group_id == group_id
        )
        group = self.conn.execute(group_select).fetchone()
        assocs = self.conn.execute(users_select)
        return _to_group(group, assocs) if group else None

    def create_group(self, group):
        group_id = group.group_id
        group_insert = schema.groups.insert().values(
            id=group_id,
        )
        users_values = [
            {
                "user_id": user_id,
                "group_id": group_id
            }
            for user_id in group.users
        ]

        series = [(group_insert,)]
        if users_values:
            series.append(
                (schema.user_group_associations.insert(), users_values)
            )

        self._transaction(series)

        return self.get_group(group_id)
