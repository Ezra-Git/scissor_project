from flask import Flask
from flask.views import MethodView
from db import db

from flask_smorest import Api, Blueprint, abort
from flask_jwt_extended import JWTManager

import marshmallow
import datetime

from resources.healthstatus import blp as health_blp
from resources.url import blp as url_blp
from resources.user import blp as user_blp

upload_folder = "C:/Users/HP/Documents/scissor_project/qr_code"

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['UPLOAD_FOLDER'] = upload_folder
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=25)
api = Api(app)

db.init_app(app)
jwt = JWTManager(app)

api.register_blueprint(url_blp)
api.register_blueprint(user_blp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)