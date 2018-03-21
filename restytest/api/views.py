""" View logic for converting models """


def user(user_model):
    return {
        "userid": user_model.user_id,
        "first_name": user_model.first_name,
        "last_name": user_model.last_name,
        "groups": [g for g in user_model.groups] # Why a list comprehension??
    }


def group(group_model):
    return {
        "userids": [u for u in group_model.users] # Why a list comprehension?
    }
