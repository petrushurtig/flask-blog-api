import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flasgger import Swagger
from flask import redirect

from src.db.config.db import db, bcrypt
from src.dependency.containers import Container

from src.web.routes import (
    user_routes,
    post_routes,
    comment_routes,
    auth_routes,
    admin_user_routes
)
from app_source import app

from src.db.dbmodels import * 

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SWAGGER"] = {"title": "Blog API"}

#Register routes

app.register_blueprint(user_routes.blueprint, url_prefix='/api/users')
app.register_blueprint(auth_routes.blueprint, url_prefix='/api/auth')
app.register_blueprint(post_routes.blueprint, url_prefix='/api/posts')
app.register_blueprint(comment_routes.blueprint, url_prefix='/api/comments')
app.register_blueprint(admin_user_routes.blueprint, url_prefix='/api/admin/users')
@app.route('/docs')
def documentation():
    return redirect('/static/docs.html')

migrate = Migrate(app, db, compare_type=True)
swagger = Swagger(app, template_file="api.yml")

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