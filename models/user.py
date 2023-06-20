import marshmallow as ma
from passlib.hash import pbkdf2_sha256
from db import db

class usermodel(db.Model):
    __tablename__ = "user"
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)

    url_linker = db.relationship("urlmodel", back_populates = "user_linker")

    def __init__(self, new_user_data) -> None:
        self.id = None
        self.name = new_user_data["name"]
        self.email = new_user_data["email"]
        self.password = new_user_data["password"]


    @classmethod
    def create_user(cls, new_user_data):
        if "name" not in new_user_data:
            return False
        if "email" not in new_user_data:
            return False
        if usermodel.query.filter(usermodel.email == new_user_data["email"]).first():
            return False
        
        hashed_password = pbkdf2_sha256.hash(new_user_data["password"])
        user_signup = usermodel({
            "name" : new_user_data["name"],
            "password" : hashed_password,
            "email" : new_user_data["email"]
        })
        db.session.add(user_signup)
        db.session.commit()

        return True
    
    @classmethod
    def find_by_email(cls, email):
        user_email = cls.query.filter_by(email=email).first()
        return user_email