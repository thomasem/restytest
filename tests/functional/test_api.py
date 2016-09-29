""" API end-to-end tests """

import unittest

import webtest

from restytest.api import app


class APITestBase(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(app.app)

    def tearDown(self):
        # NOTE(thomasem): Get an entirely new API for each test.
        reload(app)


class TestAPIGroups(APITestBase):
    def setUp(self):
        super(TestAPIGroups, self).setUp()

        self.app.post_json(
            "/users",
            {
                "userid": "bc",
                "first_name": "Bumbleywump",
                "last_name": "Cucumberpatch",
                "groups": []
            }
        )

    def test_create_group(self):
        expected = {
            "userids": []
        }

        resp = self.app.post_json("/groups", {"name": "admins"})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

    def test_get_group(self):
        expected = {
            "userids": []
        }
        self.app.post_json("/groups", {"name": "admins"})

        resp = self.app.get("/groups/admins")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

    def test_delete_group(self):
        expected = {
            "userids": []
        }
        self.app.post_json('/groups', {'name': "admins"})

        resp = self.app.get('/groups/admins')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

        resp = self.app.delete('/groups/admins')
        self.assertEqual(resp.status_code, 204)

        resp = self.app.get('/groups/admins', status=404)
        self.assertEqual(resp.status_code, 404)

    def test_create_group_invalid_json(self):
        resp = self.app.post_json("/groups", {"foo": "bar"}, status=422)

        self.assertEqual(resp.status_code, 422)

    def test_put_group_add_users(self):
        self.app.post_json("/groups", {"name": "admins"})

        resp = self.app.put_json("/groups/admins", {"userids": ["bc"]})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['userids'], ['bc'])


class TestAPIUsers(APITestBase):
    def setUp(self):
        super(TestAPIUsers, self).setUp()
        for group in ("admins", "developers", "wookiees"):
            resp = self.app.post_json('/groups', {'name': group})
            self.assertEqual(resp.status_code, 200)

    def test_create_user(self):
        expected = {
            "userid": "bc",
            "first_name": "Bumbleywump",
            "last_name": "Cucumberpatch",
            "groups": []
        }

        resp = self.app.post_json("/users", expected)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

    def test_create_user_existing_groups(self):
        expected = {
            "userid": "bc",
            "first_name": "Bumbleywump",
            "last_name": "Cucumberpatch",
            "groups": ["admins", "developers"]
        }
        resp = self.app.post_json("/users", expected)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

    def test_get_user_existing_groups(self):
        expected = {
            "userid": "bc",
            "first_name": "Bumbleywump",
            "last_name": "Cucumberpatch",
            "groups": ["admins", "developers"]
        }
        self.app.post_json("/users", expected)

        resp = self.app.get('/users/bc')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

    def test_delete_user_existing_groups(self):
        expected = {
            "userid": "bc",
            "first_name": "Bumbleywump",
            "last_name": "Cucumberpatch",
            "groups": ["admins", "developers"]
        }
        self.app.post_json("/users", expected)

        resp = self.app.get('/users/bc')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected)

        resp = self.app.delete('/users/bc')
        self.assertEqual(resp.status_code, 204)

        resp = self.app.get('/users/bc', status=404)
        self.assertEqual(resp.status_code, 404)

    def test_create_user_invalid_json(self):
        request = {
            "userid": "bc",
            "first_eman": "Bumbleywump",
            "last_eman": "Cucumberpatch",
            "groups": ["admins", "developers"]
        }
        resp = self.app.post_json("/users", request, status=422)

        self.assertEqual(resp.status_code, 422)

    def test_put_user_add_groups(self):
        user = {
            "userid": "bc",
            "first_name": "Bumbleywump",
            "last_name": "Cucumberpatch",
            "groups": []
        }

        self.app.post_json("/users", user)

        user.update({"groups": ["admins", "wookiees"]})

        resp = self.app.put_json("/users/bc", user)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, user)
        self.assertEqual(resp.json['groups'], ['admins', 'wookiees'])
