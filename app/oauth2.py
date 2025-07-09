from datetime import datetime, timedelta
import jwt


SECRET_KEY = "99d0d3a40c2d64c6fff249b78c6e0424ef6510c6b8595f1881c7995833d55396"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30



def create_access_token(data:dict): #access token has a short lifespan
    to_encode = data.copy()  #data to be encoded in the JWT token
    expire = datetime.now() + timedelta(minutes= EXPIRATION_MINUTES)
    to_encode.update({"exp":expire}) #add token expiration time through exp property

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt