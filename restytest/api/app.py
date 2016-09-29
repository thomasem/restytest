""" REST API Application """

import functools
import json
import os

import bottle

from restytest import exceptions
from restytest.api import controller
from restytest.api import views


USERS_ROUTE = '/users'
USER_ROUTE = '{}/<userid>'.format(USERS_ROUTE)
GROUPS_ROUTE = '/groups'
GROUP_ROUTE = '{}/<group_name>'.format(GROUPS_ROUTE)
API_MIMETYPE = "application/json"

app = bottle.default_app()
cntrlr = controller.Controller()


def common_failures(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError):
            raise
            bottle.abort(400)
        except (exceptions.GroupNotFound, exceptions.UserNotFound):
            bottle.abort(404)
        except exceptions.ValidationError:
            bottle.abort(422)
        except exceptions.ResourceAlreadyExists:
            bottle.abort(409)
    return wrapper


@bottle.hook('after_request')
def set_content_type():
    bottle.response.set_header("Content-Type", API_MIMETYPE)


@app.error(500)
def handle500(error):
    return "Internal server error"


@app.post(USERS_ROUTE)
@common_failures
def create_user():
    request_json = json.load(bottle.request.body)
    return views.user(cntrlr.create_user(request_json))


@app.get(USER_ROUTE)
@common_failures
def get_user(userid):
    return views.user(cntrlr.get_user(userid))


@app.put(USER_ROUTE)
@common_failures
def update_user(userid):
    request_json = json.load(bottle.request.body)
    return views.user(cntrlr.update_user(userid, request_json))


@app.delete(USER_ROUTE)
@common_failures
def delete_user(userid):
    cntrlr.delete_user(userid)
    bottle.response.status = 204


@app.post(GROUPS_ROUTE)
@common_failures
def create_group():
    request_json = json.load(bottle.request.body)
    return views.group(cntrlr.create_group(request_json))


@app.get(GROUP_ROUTE)
@common_failures
def get_group(group_name):
    return views.group(cntrlr.get_group(group_name))


@app.put(GROUP_ROUTE)
@common_failures
def update_group(group_name):
    request_json = json.load(bottle.request.body)
    return views.group(cntrlr.update_group(group_name, request_json))


@app.delete(GROUP_ROUTE)
@common_failures
def delete_group(group_name):
    cntrlr.delete_group(group_name)
    bottle.response.status = 204


def serve():
    app.run(
        host=os.environ.get('RESTYTEST_HOST', 'localhost'),
        port=os.environ.get('RESTYTEST_PORT', 8080)
    )
