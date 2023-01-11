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
    comment_routes
)
from app_source import app

from src.db.dbmodels import * 

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SWAGGER"] = {"title": "Blog API"}

#Register routes

app.register_blueprint(user_routes.user_api, url_prefix='/api/v1/users')
app.register_blueprint(post_routes.blueprint, url_prefix='/api/v1/posts')
app.register_blueprint(comment_routes.blueprint, url_prefix='/api/v1/comments')
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
        comment_routes
    ]
)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"