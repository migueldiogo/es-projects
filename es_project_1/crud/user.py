from crud import Session
from sqlalchemy import exists

from models import User


def create_user(session: Session,
                user_first_name: str,
                user_last_name:str,
                user_email:str,
                user_password:str,
                user_password_salt: str,
                user_auth_token: str) -> bool:
    result = session.query(exists().where(User.email == user_email)).scalar()
    if result:
        return False

    user = User(first_name=user_first_name,
                last_name=user_last_name,
                email=user_email,
                password_hashed=user_password,
                password_salt = user_password_salt,
                auth_token = user_auth_token)
    session.add(user)
    session.commit()
    return True


def update_user(session: Session,
                user_id: str,
                user_first_name: str,
                user_last_name:str,
                user_email:str,
                user_password:str,
                user_password_salt: str) -> bool:
    user = session.query(User).filter_by(id = user_id).first()
    if not user:
        return False

    user.first_name = user_first_name if user_first_name else user.first_name
    user.last_name = user_last_name if user_last_name else user.last_name
    user.email = user_email if user_email else user.email
    user.password = user_password if user_password else user.password
    user.password_salt = user_password_salt if user_password_salt else user.password_salt
    session.commit()
    return True


def get_user_by_email(session: Session, user_email: str) -> User:
    return session.query(User).filter_by(email = user_email).first()


def get_user_by_token(session: Session, user_auth_token: str) -> User:
    return session.query(User).filter_by(auth_token = user_auth_token).first()


def delete_user(session: Session, user_id: str) -> bool:
    rows_affected = session.query(User).filter_by(id = user_id).delete()
    session.commit()
    return rows_affected > 0
    


