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
    }
}

group = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "maxLength": NAME_LENGTH
        }
    }
}


def validate_user(data):
    try:
        jsonschema.validate(data, user)
    except:
        raise exceptions.ValidationError()


def validate_group(data):
    try:
        jsonschema.validate(data, group)
    except:
        raise exceptions.ValidationError()


def validate_userid(userid):
    if not isinstance(userid, str) or len(userid) > NAME_LENGTH:
        raise exceptions.ValidationError()


def validate_group_name(group_name):
    if not isinstance(group_name, str) or len(group_name) > NAME_LENGTH:
        raise exceptions.ValidationError()
