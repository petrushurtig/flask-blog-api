import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flasgger import Swagger
from flask import Flask, redirect
from flask_cors import CORS

app = Flask(__name__)
from src.db.config.db import db, bcrypt
from src.common.containers import Container

from src.web.routes import (
    user_routes,
    post_routes,
    comment_routes,
    auth_routes,
    admin_user_routes
)

from src.db.models import * 

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


#Register routes

app.register_blueprint(user_routes.blueprint, url_prefix='/v1/users')
app.register_blueprint(auth_routes.blueprint, url_prefix='/v1/auth')
app.register_blueprint(post_routes.blueprint, url_prefix='/v1/posts')
app.register_blueprint(comment_routes.blueprint, url_prefix='/v1/comments')
app.register_blueprint(admin_user_routes.blueprint, url_prefix='/v1/admin/users')
@app.route('/docs')
def documentation():
    return redirect('/static/docs.html')

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
        admin_user_routes
    ]
)


@app.cli.command("seed")
def command_seed():
    container.seed_command().execute()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"