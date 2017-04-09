import hashlib, uuid


def generate_uuid() -> str:
    return uuid.uuid4().hex


def hash_password(password_raw: str, salt: str) -> str:
    hashed_password = hashlib.sha512(password_raw.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    
    return hashed_password
