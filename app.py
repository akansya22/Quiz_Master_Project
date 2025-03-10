from flask import Flask
from backend.models import *
from backend.api_controllers import *


app = None

def setup_app():
    global app
    app = Flask(__name__)
    app.secret_key = "your_secret_key"  # Required for session handling
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz_info.sqlite3"
    db.init_app(app)
    api.init_app(app)
    app.app_context().push()
    print("Congrats, Your Server is Started....")

    
setup_app()

from backend.controllers import *

if __name__ == "__main__":
    app.run(debug=True)