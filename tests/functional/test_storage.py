""" SQLite access layer tests"""
import unittest

from restytest import models
from restytest import storage
from restytest.storage import schema


class StorageTestBase(unittest.TestCase):
    def setUp(self):
        self.db = storage.Storage()


class TestUser(StorageTestBase):
    def setUp(self):
        super(TestUser, self).setUp()

        self.groups = ['admins', 'users']
        [self.db.create_group(models.Group(g)) for g in self.groups]

    def tearDown(self):
        del self.db

    def test_create_user_with_group(self):
        user = models.User(
            user_id="bc",
            first_name="Bumbleywump",
            last_name="Cucumberpatch",
            groups=['users'],
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

    def test_create_user_with_many_groups(self):
        user = models.User(
            user_id="bc",
            first_name="Bumbleywump",
            last_name="Cucumberpatch",
            groups=['users', 'admins'],
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
            last_name="Cucumberpatch",
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
        self.assertEqual(result.groups, [])

    def test_get_user_with_group(self):
        user = models.User(
            user_id="bc",
            first_name="Bumbleywump",
            last_name="Cucumberpatch",
            groups=['admins'],
        )

        self.db.create_user(user)

        result = self.db.get_user(user.user_id)

        # NOTE (thomsem): Ensure returned object matches the one requested to
        # be stored.
        self.assertEqual(user.user_id, result.user_id)
        self.assertEqual(user.first_name, result.first_name)
        self.assertEqual(user.last_name, result.last_name)
        self.assertEqual(user.groups, result.groups)

    def test_get_user_without_group(self):
        user = models.User(
            user_id="bc",
            first_name="Bumbleywump",
            last_name="Cucumberpatch",
        )

        self.db.create_user(user)

        result = self.db.get_user(user.user_id)

        # NOTE (thomsem): Ensure returned object matches the one requested to
        # be stored.
        self.assertEqual(user.user_id, result.user_id)
        self.assertEqual(user.first_name, result.first_name)
        self.assertEqual(user.last_name, result.last_name)
        self.assertEqual(user.groups, result.groups)
        self.assertEqual(result.groups, [])

    def test_get_user_not_exists(self):
        result = self.db.get_user('bc')

        self.assertIsNone(result)


class TestGroup(StorageTestBase):
    def setUp(self):
        super(TestGroup, self).setUp()

        self.users = [
            models.User(
                user_id="bc",
                first_name="Bumbleywump",
                last_name="Cucumberpatch",
            ),
            models.User(
                user_id="thomasem",
                first_name="Thomas",
                last_name="Maddox",
            )
        ]
        [self.db.create_user(u) for u in self.users]

    def tearDown(self):
        del self.db

    def test_create_user_with_users(self):
        group = models.Group(
            group_id="users",
            users=['thomasem', 'bc'],
        )

        result = self.db.create_group(group)

        # NOTE(thomasem): Ensure it's two different objects.
        self.assertNotEqual(group, result)

        # NOTE (thomsem): Ensure returned object matches the one requested to
        # be stored.
        self.assertEqual(group.group_id, result.group_id)
        self.assertEqual(group.users, result.users)

    def test_create_user_without_users(self):
        group = models.Group(
            group_id="users",
        )

        result = self.db.create_group(group)

        # NOTE(thomasem): Ensure it's two different objects.
        self.assertNotEqual(group, result)

        # NOTE (thomsem): Ensure returned object matches the one requested to
        # be stored.
        self.assertEqual(group.group_id, result.group_id)
        self.assertEqual(group.users, result.users)
        self.assertEqual(result.users, [])

    def test_get_group_not_exists(self):
        result = self.db.get_group('admins')

        self.assertIsNone(result)


class TestTransaction(StorageTestBase):
    def test_transaction(self):
        series = [
            (
                schema.users.insert().values(
                    id="bc",
                    first_name="Bumbleywump",
                    last_name="Cucumberpatch"
                ),
            ),
            (
                schema.user_group_associations.insert().values(
                    group_id="thisuserdoesnotexist",
                    user_id="thisgroupdoesnotexist"
                ),
            ),
        ]

        with self.assertRaises(Exception):
            self.db._transaction(series)

        result = self.db.get_user('bc')

        self.assertIsNone(result)
