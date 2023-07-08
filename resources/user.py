from flask import request, make_response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models.user import usermodel

from db import db
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_access_cookies


blp = Blueprint("user", "user", url_prefix="/user", description="Operations on user")

@blp.route("/signup")
class UserSignup(MethodView):
    def post(self):
        """Create a new user"""
        new_user_data = request.get_json()
        try:
            new_user = usermodel.create_user(new_user_data)
        except Exception as e:
            print(e)
            return {"message":"Unable to create user"}
        return {"message":"New user created successfully"}

@blp.route("/login")
class Login(MethodView):
    def post(self):
        """User Login"""
        user_data = request.get_json()
        user = usermodel.find_by_email(user_data["email"])
        if user:
            if pbkdf2_sha256.verify(user_data["password"], user.password):
                access_token = create_access_token(user.id)
                response = make_response("User logged in")
                set_access_cookies(response, access_token)
                return response
            return "Email or password is incorrect"
        return "User not found"
    
@blp.route("/logout")
class Logout(MethodView):
    def post(self):
        """Logout"""
        response = make_response("Logout successful")
        unset_access_cookies(response)
        return response