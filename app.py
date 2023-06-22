from flask import Flask
from flask.views import MethodView

from flask_smorest import Api, Blueprint, abort
from flask_sqlalchemy import SQLAlchemy

upload_folder = "C:\Users\HP\Documents\scissor_project/qr_code"

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['UPLOAD_FOLDER'] = upload_folder
api = Api(app)

db = SQLAlchemy(app)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)