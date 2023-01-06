import os
from dotenv import load_dotenv
from flask_migrate import Migrate

from src.db.config.db import db, bcrypt
from app_source import app

from src.db.dbmodels import * 

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db, compare_type=True)

bcrypt.init_app(app)
db.init_app(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"