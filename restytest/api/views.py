""" View logic for converting models """


def user(user_model):
    return {
        "userid": user_model.user_id,
        "first_name": user_model.first_name,
        "last_name": user_model.last_name,
        "groups": [g for g in user_model.groups]
    }


def group(group_model):
    return {
        "group_name": group_model.group_id,
        "users": [u for u in group_model.users]
    }
