import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flasgger import Swagger
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)

from src.db.config.db import db, bcrypt
from src.common.containers import Container

from src.web.routes import (
    admin_routes,
    user_routes,
    post_routes,
    comment_routes,
    auth_routes
)
from src.db.models import * 

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Register routes
app.register_blueprint(user_routes.blueprint, url_prefix='/v1/users')
app.register_blueprint(auth_routes.blueprint, url_prefix='/v1/auth')
app.register_blueprint(post_routes.blueprint, url_prefix='/v1/posts')
app.register_blueprint(comment_routes.blueprint, url_prefix='/v1/comments')
app.register_blueprint(admin_routes.blueprint, url_prefix='/v1/admin/users')

response = Response()

@app.after_request
def add_header(response):
    response.cache_control.max_age = 3600
    return response

migrate = Migrate(app, db, compare_type=True)
swagger = Swagger(app, template_file="api.yml")
CORS(app, origins="*")

bcrypt.init_app(app)
db.init_app(app)

container = Container()
app.container = container
container.wire(
    modules=[
        user_routes,
        post_routes,
        comment_routes,
        auth_routes,
        admin_routes
    ]
)

@app.cli.command("seed")
def command_seed():
    container.seed_command().execute()