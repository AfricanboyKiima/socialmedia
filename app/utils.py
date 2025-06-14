from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


#hash password
def password_hasher(password:str):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify(plain_password, hashed_password):
    verified_passwords = pwd_context.verify(plain_password, hashed_password)
    return verified_passwords