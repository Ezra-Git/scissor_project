from flask import request, make_response
from flask_smorest import Blueprint, abort
from datetime import datetime
from flask.views import MethodView
from models.user import usermodel
from random import choice
import string
import qrcode

from db import db
from models.url import urlmodel
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_access_cookies, get_jwt

blp = Blueprint("url", "url", url_prefix="/url_shortener", description="Operations on url")

def generate_short_url():
    """Function to generate short_url"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(7))

def generate_qr_code(input_url):
    """Function to generate qr_code"""
    img = qrcode.make(input_url)
    return img

@blp.route("/")
class ShortUrl(MethodView):
    def post(self):
        """shorten url"""
        url_info = request.get_json()
        short_url = ""
        if url_info["custom_url"] and urlmodel.find_custom_url(url_info["custom_url"]) is not None:
            return {"message":"Custom URL already taken. Enter a new one"}
        if not url_info["url"]:
            return {"message":"Enter a URL to shorten or customize"}
        if not url_info["custom_url"]:
            short_url = generate_short_url()
        qr_code = generate_qr_code(url_info['url'])
        # qr_code.
        new_link = urlmodel(
            long_url=url_info["url"], short_url=short_url, custom_url=url_info["custom url"], created_at=datetime.now())
        db.session.add(new_link)
        db.session.commit()

    def get(self):
        qr_code = generate_qr_code('Hello')
        print(dir( qr_code))
        return qr_code
    