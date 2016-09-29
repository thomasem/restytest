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


def _get_user_values(user):
    return dict(
        id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
    )


def _get_group_assocs(user_id, groups):
    return [dict(user_id=user_id, group_id=group_id)
            for group_id in groups]


def _get_group_values(group):
    return dict(
        id=group.group_id,
    )


def _get_user_assocs(group_id, users):
    return [dict(user_id=user_id, group_id=group_id)
            for user_id in users]


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

    def _create_user_series(self, user):
        user_insert = schema.users.insert().values(**_get_user_values(user))
        group_assocs = _get_group_assocs(user.user_id, user.groups)
        series = [(user_insert,)]
        if group_assocs:
            series.append(
                (schema.user_group_associations.insert(), group_assocs)
            )
        return series

    def create_user(self, user):
        series = self._create_user_series(user)
        self._transaction(series)
        return self.get_user(user.user_id)

    def update_user(self, user_id, user):
        # NOTE(thomasem): Breaking apart the create and delete to only
        # returning the query, or a series of queries, allows me a clean and
        # transactional way to do an update as well, by removing the old and
        # creating the new within a single transaction.
        series = [(self._delete_user_query(user_id),)]
        series.extend(self._create_user_series(user))
        self._transaction(series)
        return self.get_user(user.user_id)

    @staticmethod
    def _delete_user_query(user_id):
        return schema.users.delete().where(schema.users.c.id == user_id)

    def delete_user(self, user_id):
        self.conn.execute(self._delete_user_query(user_id))

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

    def _create_group_series(self, group):
        group_id = group.group_id
        group_insert = schema.groups.insert().values(
            **_get_group_values(group))
        user_assocs = _get_user_assocs(group_id, group.users)

        series = [(group_insert,)]
        if user_assocs:
            series.append(
                (schema.user_group_associations.insert(), user_assocs)
            )
        return series

    def create_group(self, group):
        series = self._create_group_series(group)
        self._transaction(series)
        return self.get_group(group.group_id)

    def update_group(self, group_id, group):
        # NOTE(thomasem): Breaking apart the create and delete to only
        # returning the query, or a series of queries, allows me a clean and
        # transactional way to do an update as well, by removing the old and
        # creating the new within a single transaction.
        series = [(self._delete_group_query(group_id),)]
        series.extend(self._create_group_series(group))
        self._transaction(series)
        return self.get_group(group.group_id)

    @staticmethod
    def _delete_group_query(group_id):
        return schema.groups.delete().where(schema.groups.c.id == group_id)

    def delete_group(self, group_id):
        self.conn.execute(self._delete_group_query(group_id))
