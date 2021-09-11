from digeiz import app
from digeiz import db


if __name__ == '__main__':
    if app.config["RESET_DB"]:
        db.drop_all()
    db.create_all()
    app.run(debug=app.config["DEBUG"])
