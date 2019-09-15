import jwt
from AILab.settings import SECRET_KEY


def generateToken(data):
    encoded_token = jwt.encode(data, SECRET_KEY, algorithm='HS256')
    token = encoded_token.decode("utf-8")
    return token

def decodeToken(token):
    data= jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return data
