from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")



def password_hasher(password:str): #hash password
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify(plain_password, hashed_password): #verify if incoming password matches its hash in the database
    verified_password = pwd_context.verify(plain_password, hashed_password)
    return verified_password
