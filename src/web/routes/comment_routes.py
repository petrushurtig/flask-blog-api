import datetime
from flask import Blueprint, request, jsonify

from src.db.dbmodels.comment import Comment
from src.db.dbmodels.post import Post
from src.db.dbmodels.user import User
from src.shared.auth import auth_required
from app_source import app

blueprint = Blueprint("comment_api", __name__)

@blueprint.route("/", methods=["GET"])
def get_all_comments():
    try:
        comments = Comment.get_all_comments()
        comments_list = []

        for comment in comments:
            comments_list.append(comment)
        
        return jsonify(comments), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

@blueprint.route("/<comment_id>", methods=["GET"])
def get_comment_by_id(comment_id):
    try:
        comment = Comment.get_comment_by_id(comment_id)

        if not comment:
            return jsonify({"message": "Comment not found"}), 404

        return jsonify(comment.json()), 200
    except Exception as e:
        msg = {"message": "Server error"}
        return jsonify(msg), 500

@blueprint.route("/<post_id>", methods=["POST"])
def add_comment_to_post(post_id):
    try:

        post = Post.get_post_by_id(post_id)

        if not post:
            return jsonify({"message": "Post not found"}), 404
        
        comment_data = request.get_json()

        if "content" not in comment_data:
            msg = {"message": "Content missing"}
            return jsonify(msg, comment_data), 400

        if "username" not in comment_data:
            msg = {"message": "Username missing"}
            return jsonify(msg, comment_data), 400

        comment = Comment(
            content = comment_data["content"],
            username = comment_data["username"],
            post_id=post.id,
            created_at=datetime.datetime.now(tz=datetime.timezone.utc)
        )
        
        comment.save()

        return jsonify(comment.json())
    except Exception as e:
        msg = {"message": "Error when creating comment"}
        return jsonify(msg), 500

