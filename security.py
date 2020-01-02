from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    # When using get, we can provide a default value, which is not possible when using [] to access dictionary elements
    # user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    # use safe_str_cmp to compare without worrying about encoding formats
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)
