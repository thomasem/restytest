""" REST API Application """

import os

import bottle


USERS_ROUTE = '/users'
USER_ROUTE = '{}/<userid>'.format(USERS_ROUTE)
GROUPS_ROUTE = '/groups'
GROUP_ROUTE = '{}/<group_name>'.format(GROUPS_ROUTE)

app = bottle.default_app()


@app.post(USERS_ROUTE)
def create_user():
    pass


@app.get(USER_ROUTE)
def get_user(userid):
    pass


@app.put(USER_ROUTE)
def update_user(userid):
    pass


@app.delete(USER_ROUTE)
def delete_user(userid):
    pass


@app.post(GROUPS_ROUTE)
def create_group():
    pass


@app.get(GROUP_ROUTE)
def get_group(group_name):
    pass


@app.put(GROUP_ROUTE)
def update_group(group_name):
    pass


@app.delete(GROUP_ROUTE)
def delete_group(group_name):
    pass


def serve():
    app.run(
        host=os.environ.get('RESTYTEST_HOST', 'localhost'),
        port=os.environ.get('RESTYTEST_PORT', 8080),
    )
