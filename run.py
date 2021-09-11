from digeiz import app
from digeiz import db


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=app.config["DEBUG"])
