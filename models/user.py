
from db import db
from passlib.hash import pbkdf2_sha256

class UserModel(db.Model):

    __tablename__ = 'users'

    userId = db.Column(db.String(255), primary_key = True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))

    def __init__(self, username, password, email, firstName, lastName):
        self.userId = username
        self.password = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        self.email = email
        self.firstName = firstName
        self.lastName = lastName

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self,password):
        return pbkdf2_sha256.verify(password, self.password)

    def change_password(self, newPassword):
        self.password = pbkdf2_sha256.encrypt(newPassword, rounds=200000, salt_size=16)
        db.session.add(self)
        db.session.commit()

    @classmethod #visto que nao usamos o self
    def find_by_username(cls, username):
        return cls.query.filter_by(userId=username).first()
