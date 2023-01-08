import datetime
from flask import Blueprint, request, jsonify

from src.db.dbmodels.post import Post
from src.db.dbmodels.user import User
from src.shared.auth import auth_required
from app_source import app

blueprint = Blueprint("post_api", __name__)

@blueprint.route("/", methods=["GET"])
def get_all_posts():
    try:
        posts = Post.get_all_posts()
        posts_list = []

        for post in posts:
            posts_list.append(post)
        
        return jsonify(posts), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

@blueprint.route("/<post_id>", methods=["GET"])
def get_post_by_id(post_id):
    try:
        post = Post.get_post_by_id(post_id)

        if not post:
            return jsonify({"message": "Post not found"}), 404
        
        return jsonify(post.json()), 200
    except Exception as e:
        msg = {"message": "Server error"}
        return jsonify(msg), 500

@blueprint.route("/", methods=["POST"])
@auth_required()
def create_post(user: User):
    try:
        post_data = request.get_json()

        post = Post(
            user_id=user.id,
            created_at=datetime.datetime.now(tz=datetime.timezone.utc)
        )
        
        if "title" in post_data:
            post.title = post_data["title"]
        
        if "content" in post_data:
            post.content = post_data["content"]

        post.save()

        return jsonify(post.json())
    except Exception as e:
        msg = {"message": "Error when creating post"}
        return jsonify(msg), 500