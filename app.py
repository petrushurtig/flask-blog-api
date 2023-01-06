import os
from dotenv import load_dotenv
from flask_migrate import Migrate

from src.db.config.db import db
from app_source import app


load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db, compare_type=True)

db.init_app(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"