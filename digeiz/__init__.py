from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


from digeiz.routes_get_all import get_all
from digeiz.routes_get_one import get_one
from digeiz.routes_post_one import post_one

app.register_blueprint(get_all)
app.register_blueprint(get_one)
app.register_blueprint(post_one)
