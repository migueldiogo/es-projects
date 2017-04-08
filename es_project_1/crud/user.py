from business import session
from models import User


def create_user(user_first_name: str,
                user_last_name:str,
                user_email:str,
                user_password:str,
                user_password_salt: str,
                user_auth_token: str) -> bool:
    result = session.query(User).filter(User.email.like(user_email))
    if result:
        return False

    user = User(first_name=user_first_name,
                last_name=user_last_name,
                email=user_email,
                password=user_password,
                user_password_salt = user_password_salt,
                user_auth_token = user_auth_token)
    session.add(user)
    session.commit()
    return True


def update_user(user_auth_token: str,
                user_first_name: str,
                user_last_name:str,
                user_email:str,
                user_password:str,
                user_password_salt: str) -> bool:
    user = session.query(User).filter(User.auth_token == user_auth_token)
    if not user:
        return False

    user.first_name = user_first_name if user_first_name else user.first_name
    user.last_name = user_last_name if user_last_name else user.last_name
    user.email = user_email if user_email else user.email
    user.password = user_password if user_password else user.password
    user.password_salt = user_password_salt if user_password_salt else user.password_salt
    session.commit()
    return True


def get_user(user_auth_token: str) -> User:
    return session.query(User).filter(User.auth_token == user_auth_token)


def get_user(user_email: str, user_password:str) -> User:
    return session.query(User).filter(User.email == user_email, User.password_hashed == user_password)


def delete_user(user_auth_token: str) -> bool:
    rows_affected = session.query(User).filter(User.auth_token == user_auth_token).delete()
    session.commit()
    return rows_affected > 0
    


