import datetime
from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide

from src.db.dbmodels.comment import Comment
from src.db.dbmodels.post import Post
from src.db.dbmodels.user import User
from src.interfaces.models.user import IUser
from src.interfaces.repositories.comment_repository import ICommentRepository
from src.db.services.comment_service import CommentService
from src.db.services.post_service import PostService
from src.web.middleware.auth_middleware import auth_required
from src.dependency.containers import Container
from app_source import app

blueprint = Blueprint("comment_api", __name__)

@blueprint.route("/", methods=["GET"])
@inject
#admin_required
def get_all_comments(
    comment_service: CommentService = Provide[Container.comment_service]
):
    try:
        comments = comment_service.get_all_comments()
        
        return jsonify(comments), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

@blueprint.route("/<comment_id>", methods=["GET"])
@inject
@auth_required()
def get_comment_by_id(
    comment_id: int,
    comment_service: CommentService = Provide[Container.comment_service]
):
    try:
        comment = comment_service.get_comment_by_id(comment_id)

        if not comment:
            return jsonify({"message": "Comment not found"}), 404

        return jsonify(comment.json()), 200
    except Exception as e:
        msg = {"message": "Server error"}
        return jsonify(msg), 500

@blueprint.route("/<post_id>", methods=["POST"])
@inject
@auth_required()
def add_comment_to_post(
    user: IUser,
    post_id: str,
    comment_service: CommentService = Provide[Container.comment_service],
    post_service: PostService = Provide[Container.post_service]
):
    try:
        post = post_service.get_post_by_id(post_id)

        if not post:
            return jsonify({"message": "Post not found"}), 404
        
        comment_data = request.get_json()

        if "content" not in comment_data:
            msg = {"message": "Content missing"}
            return jsonify(msg, comment_data), 400

        comment_data["post_id"] = post.id
        comment_data["user_id"] = user.id

        comment = comment_service.create_comment(comment_data)
    
        return jsonify(comment.json())
    except Exception as e:
        app.logger.info(e)
        msg = {"message": "Error when creating comment"}
        return jsonify(msg), 500

