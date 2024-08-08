"""  es un metodo init que en el tiene un constructor que recibe todos los datos de la taba user de la base de datos, tambien se cifra la password """
from werkzeug.security import generate_password_hash, check_password_hash

import hashlib

class User:
    def __init__(self, id, username, password, fullname=None):
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

    @classmethod
    def hash_password(cls, password):
        return generate_password_hash(password)

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)


