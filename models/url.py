import marshmallow as ma
from passlib.hash import pbkdf2_sha256
from db import db

class urlmodel(db.Model):
    __tablename__ = "url"
    long_url = db.Column(db.String(50), nullable=False)
    short_url = db.Column(db.String(50), nullable=True)
    short_url_count = db.Column(db.Integer, default=0)
    custom_url = db.Column(db.String(50), nullable=True)
    url_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img_bytes = db.Column(db.LargeBinary, nullable=True)

    user_linker = db.relationship("usermodel", back_populates = "url_linker")

    def __init__(self, long_url, short_url, custom_url) -> None:
        self.long_url = long_url
        self.short_url = short_url
        self.custom_url = custom_url
        
    @classmethod
    def find_custom_url(cls, short_id):
        return cls.query.filter(urlmodel.custom_url == short_id).first()
    
    @classmethod
    def find_short_url(cls, short_id):
        return cls.query.filter(urlmodel.short_url == short_id).first()
    
    @classmethod
    def find_long_url(cls, short_id):
        custom_url = cls.find_custom_url(short_id)
        if not custom_url:
            short_url = cls.find_short_url(short_id)
            return short_url
        return custom_url
    
    @classmethod
    def find_user_long_url(cls, user_id):
        cls.query.filter(urlmodel.User.id == user_id).scalars()