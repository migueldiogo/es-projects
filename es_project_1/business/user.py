from crud import user as crud_user
from models import User
from . import utils
from .custom_exceptions import *


def create_user(user_first_name: str, user_last_name: str, user_email: str, user_password: str) -> bool:
    password_hashing = utils.hash_password(password_raw = user_password)
    password_hash = password_hashing.get('password_hash')
    password_salt = password_hashing.get('password_salt')
    
    auth_token = utils.generate_uuid()
    
    return crud_user.create_user(
            user_first_name,
            user_last_name,
            user_email,
            password_hash,
            password_salt,
            auth_token)


def update_user(user_auth_token: str, user_first_name: str, user_last_name: str, user_email: str,
                user_password: str) -> bool:
    if user_password:
        password_hashing = utils.hash_password(password_raw = user_password)
        password_hash = password_hashing.get('password_hash')
        password_salt = password_hashing.get('password_salt')
        return crud_user.update_user(user_auth_token,
                                     user_first_name,
                                     user_last_name,
                                     user_email,
                                     password_hash,
                                     password_salt)
    else:
        return crud_user.update_user(user_auth_token,
                                     user_first_name,
                                     user_last_name,
                                     user_email)


def get_user(user_auth_token: str) -> User:
    return crud_user.get_user(user_auth_token)


def delete_user(user_auth_token: str) -> bool:
    return crud_user.delete_user(user_auth_token)


def get_auth_token(user_email: str, user_password: str) -> str:
    user = User(crud_user.get_user(user_email = user_email, user_password = user_password))
    
    if not user:
        raise Unauthorized
    
    return user.auth_token
