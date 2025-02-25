from flask import Flask
from backend.models import db


app = None

def setup_app():
    global app
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz_info.sqlite3"
    db.init_app(app)
    app.app_context().push()
    print("Congrats, Your Server is Started....")

setup_app()

if __name__ == "__main__":
    app.run(debug=True)