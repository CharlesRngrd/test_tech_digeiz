from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

from digeiz import routes
