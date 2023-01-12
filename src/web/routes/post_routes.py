import datetime
from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide

from app_source import app
from src.db.dbmodels.post import Post
from src.db.dbmodels.user import User
from src.interfaces.models.user import IUser
from src.interfaces.models.post import IPost
from src.db.services.post_service import PostService
from src.db.repositories.post_repository import PostRepository
from src.shared.auth import auth_required
from src.dependency.containers import Container

blueprint = Blueprint("post_api", __name__)

@blueprint.route("/", methods=["GET"])
@inject
def get_all_posts(
    post_service: PostService = Provide[Container.post_service]
):
    try:
        posts = post_service.get_all_posts()
        
        return jsonify(posts), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

@blueprint.route("/<post_id>", methods=["GET"])
@inject
def get_post_by_id(
    post_id: int,
    post_service: PostService = Provide[Container.post_service]
):
    try:
        #add +1 to post.views every time it is fetched
        post_service.increment_views(post_id)

        post: IPost = post_service.get_post_by_id(post_id)
        if not post:
            return jsonify({"message": "Post not found"}), 404

        return jsonify(post.json()), 200

    except Exception as e:
        app.logger.info(e)
        msg = {"message": "Server error e"}
        return jsonify(msg), 500

@blueprint.route("/", methods=["POST"])
@inject
@auth_required()
def create_post(
    user: User,
    post_service: PostService = Provide[Container.post_service]
):
    try:
        post_data = request.get_json()
        post = post_service.create_post(user.id, post_data)
        
        return jsonify(post.json()), 201
    except Exception as e:
        msg = {"message": "Server error"}
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
