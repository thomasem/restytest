""" SQLite access layer tests"""
import unittest

from restytest import storage
from restytest import models


class TestUser(unittest.TestCase):
    def setUp(self):
        self.db = storage.Storage()
        self.db.conn.execute(
            "INSERT INTO groups (id) VALUES ('admins'),('users');"
        )
        # self.groups = ['admins', 'users']
        # [self.db.create_group(models.Group(g)) for g in groups]

    def tearDown(self):
        del self.db

    def test_create_user_with_group(self):
        user = models.User(
            user_id="bc",
            first_name="Bumbleywump",
            last_name="Cucumberpatch",
            groups=['users']
        )

        result = self.db.create_user(user)

        # NOTE(thomasem): Ensure it's two different objects.
        self.assertNotEqual(user, result)

        # NOTE (thomsem): Ensure returned object matches the one requested to
        # be stored.
        self.assertEqual(user.user_id, result.user_id)
        self.assertEqual(user.first_name, result.first_name)
        self.assertEqual(user.last_name, result.last_name)
        self.assertEqual(user.groups, result.groups)

    def test_create_user_without_group(self):
        user = models.User(
            user_id="bc",
            first_name="Bumbleywump",
            last_name="Cucumberpatch"
        )

        result = self.db.create_user(user)

        # NOTE(thomasem): Ensure it's two different objects.
        self.assertNotEqual(user, result)

        # NOTE (thomsem): Ensure returned object matches the one requested to
        # be stored.
        self.assertEqual(user.user_id, result.user_id)
        self.assertEqual(user.first_name, result.first_name)
        self.assertEqual(user.last_name, result.last_name)
        self.assertEqual(user.groups, result.groups)
