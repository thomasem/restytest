""" JSON Schema validations """

import jsonschema

from restytest import exceptions


NAME_LENGTH = 35


user = {
    "type": "object",
    "properties": {
        "userid": {
            "type": "string",
            "maxLength": NAME_LENGTH
        },
        "first_name": {
            "type": "string",
            "maxLength": NAME_LENGTH
        },
        "last_name": {
            "type": "string",
            "maxLength": NAME_LENGTH
        },
        "groups": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength": NAME_LENGTH
            },
            "maxItems": 50
        }
    },
    "additionalProperties": False
}

group_post = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "maxLength": NAME_LENGTH
        }
    },
    "additionalProperties": False
}

group_put = {
    "type": "object",
    "properties": {
        "userids": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength": NAME_LENGTH
            },
            "maxItems": 50
        }
    },
    "additionalProperties": False
}


def validate_user(data):
    try:
        jsonschema.validate(data, user)
    except:
        raise exceptions.ValidationError()


def validate_group_post(data):
    try:
        jsonschema.validate(data, group_post)
    except:
        raise exceptions.ValidationError()


def validate_group_put(data):
    try:
        jsonschema.validate(data, group_put)
    except:
        raise exceptions.ValidationError()


def validate_userid(userid):
    if len(userid) > NAME_LENGTH:
        raise exceptions.InvalidIdentifier()


def validate_group_name(group_name):
    if len(group_name) > NAME_LENGTH:
        raise exceptions.InvalidIdentifier()
