from flask import request, make_response, redirect
from flask_smorest import Blueprint, abort
from datetime import datetime
from flask.views import MethodView
from models.user import usermodel
from random import choice
from flask_jwt_extended import get_jwt_identity
import string
import qrcode

from db import db
from models.url import urlmodel
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_access_cookies, get_jwt

blp = Blueprint("url", "url", url_prefix="", description="Operations on url")

def generate_short_url():
    """Function to generate short_url"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(7))

def generate_qr_code(input_url):
    """Function to generate qr_code"""
    img = qrcode.make(input_url)
    img_bytes = img.to_bytes()
    return img_bytes

@blp.route("/")
class ShortUrl(MethodView):
    def post(self):
        """shorten url"""
        url_info = request.get_json()
        short_url = ""
        if len (url_info ["custom_url"]) > 0 and urlmodel.find_custom_url(url_info["custom_url"]) is not None:
            return {"message":"Custom URL already taken. Enter a new one"}
        if not url_info["url"]:
            return {"message":"Enter a URL to shorten or customize"}
        if not url_info["custom_url"]:
            short_url = generate_short_url()
        qr_code = generate_qr_code(url_info['url'])
        new_link = urlmodel(
            long_url=url_info["url"], short_url=short_url, custom_url=url_info["custom_url"])
        db.session.add(new_link)
        db.session.commit()
        return {"message":"Link shortened successfully",
                "link": url_info["custom_url"] or short_url}

@blp.route("/url_history")
class url_history(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        links = urlmodel.find_user_long_url(user_id)
        return {"links": links}
    
@blp.route("/<string:short_url>")
class retreive_url(MethodView):
    def get(self, short_url):
        long_url_info = urlmodel.find_long_url(short_url)
        long_url_info.short_url_count += 1
        db.session.commit()
        print(long_url_info.short_url_count)
        return redirect(long_url_info.long_url)
       
