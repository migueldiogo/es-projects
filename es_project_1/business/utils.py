import hashlib, uuid

def generate_uuid() -> str:
    return uuid.uuid4().hex

def hash_password(password_raw: str, salt: str) -> dict:
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password_raw + salt).hexdigest()
    
    return {'password_salt': salt, 'password_hash': hashed_password}
