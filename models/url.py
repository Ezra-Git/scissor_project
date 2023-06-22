import marshmallow as ma
from passlib.hash import pbkdf2_sha256
from db import db

class urlmodel(db.Model):
    __tablename__ = "url"
    long_url = db.Column(db.String(50), nullable=False)
    short_url = db.Column(db.String(50), nullable=True)
    custom_url = db.Column(db.String(50), nullable=True)
    url_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.Foreignkey('user.id'),foreign_keys=True)
    img_bytes = db.Column(db.Integer(255), nullable=False)

    user_linker = db.relationship("usermodel", back_populates = "url_linker")

    def __init__(self, new_url_data) -> None:
        self.id = None
        self.long_url = new_url_data["long url"]
        self.short_url = new_url_data["short url"]
        self.custom_url = new_url_data["custom url"]


    @classmethod
    def find_custom_url(cls, short_id):
        return cls.query.filter(urlmodel.custom_url == short_id).first()