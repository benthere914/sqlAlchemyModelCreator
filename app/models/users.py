from .db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), primary_key=False, nullable=False)
    email = db.Column(db.String(255), primary_key=False, nullable=False)
    hashed_password = db.Column(db.String(255), primary_key=False, nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

    def valid_password(self, password):
        if (not (any([char for char in password if char in '01234567890']))):
            return [False, 'a number']
        if (not (any([char for char in password if char in '`~!@#$%^&*()_-+={[}]|\;:\'",<.>/?']))):
            return [False, 'any special characters']
        if (not any([char for char in password if char in [letter.upper() for letter in 'abcdefghijklmnoppqrstuvwxyz']])):
            return [False, 'any upper case letters']
        if (len(password) < 8):
            return [False, 'at least 8 characters']
        return [True, '']

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = password

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(email=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active

