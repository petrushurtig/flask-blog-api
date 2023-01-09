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

        #increment post.views by 1
        post = Post.add_one_to_views(post_id)

        return jsonify(post.json()), 200
    except Exception as e:
        msg = {"message": "Server error"}
        return jsonify(msg), 500

@blueprint.route("/", methods=["POST"])
@auth_required()
def create_post(user: User):
    try:
        post_data = request.get_json()

        if "title" not in post_data:
            msg = {"message": "Title missing"}
            return jsonify(msg, post_data), 400
        
        if "content" not in post_data:
            msg = {"message": "Content missing"}
            return jsonify(msg, post_data), 400

        post = Post(
            title = post_data["title"],
            content = post_data["title"],
            user_id=user.id,
            created_at=datetime.datetime.now(tz=datetime.timezone.utc)
        )

        post.save()

        return jsonify(post.json())
    except Exception as e:
        msg = {"message": "Error when creating post"}
        return jsonify(msg), 500

@blueprint.route("/<post_id>", methods=["PUT"])
@auth_required()
def update_post(user: User, post_id: int):

    try:
        post_data = request.get_json()
        post = Post.get_post_by_id(post_id)

        if not post:
            msg = {"message": "Post not found"}
            return jsonify(msg), 404
        
        if user.id != post.user_id:
            msg = {"message": "Unauthorized"}
            return jsonify(msg), 401

        updated_post = Post.update(post_id, post_data)
    
        return jsonify(updated_post.json()), 200

    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Server error"}), 500

@blueprint.route("/<post_id>", methods=["DELETE"])
@auth_required()
def delete_post(user: User, post_id: int):

    try:
        post = Post.get_post_by_id(post_id)

        if not post:
            msg = {"message": "Post not found"}
            return jsonify(msg), 404
        
        if user.id != post.user_id:
            msg = {"message": "Unauthorized"}
            return jsonify(msg), 401
        
        post.delete()

        return jsonify({"message": "Removed post"})

    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

@blueprint.route("/<post_id>/comments", methods=["GET"])
def get_comments_of_post(post_id: int):
    try:
        post = Post.get_post_by_id(post_id)

        if not post:
            msg = {"message": "Post not found"}
            return jsonify(msg), 404

        comment_list = []
        for comment in post.comments:
            comment_list.append(comment.json())
        return jsonify(comment_list)

    except Exception as e:
        app.logger.info(e)
        msg = {"message": "Server error"}
        return jsonify(msg), 500
