from business import session
from models import User


def users_post(firstName, lastName, email, password):
    """
    Create a new user

    :param firstName: User&#39;s first name
    :type firstName: str
    :param lastName: User&#39;s last name
    :type lastName: str
    :param email: User&#39;s email
    :type email: str
    :param password: User&#39;s password
    :type password: str

    :rtype: None
    """
    result = session.query(User).filter(User.email.like(email))
    if result:
        return False

    user = User(firstName=firstName, lastName=lastName, email=email, password=password)
    session.add(user)
    session.commit()
    return True

