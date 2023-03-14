from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide

from app import app
from src.db.models.post import Post
from src.db.models.user import User
from src.interfaces.models.post import IPost
from src.services.post_service import PostService
from src.web.middleware.auth_middleware import auth_required
from src.common.hateoas import pagination_links
from src.common.containers import Container

blueprint = Blueprint("post_api", __name__)

@blueprint.route("/", methods=["GET"])
@inject
def get_all_posts(
    post_service: PostService = Provide[Container.post_service]
):
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)


        posts = post_service.get_all_posts(page, per_page)


        return jsonify(pagination_links(posts, page, per_page, '.get_all_posts')), 200
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
        
        post: IPost = post_service.get_post_by_id(post_id)
        if not post:
            msg = {"message": "Post not found"}
            return jsonify(msg), 404

        #add +1 to post.views every time it is fetched
        post_service.increment_views(post_id)

        return jsonify(post.json()), 200

    except Exception as e:
        app.logger.info(e)
        msg = {"message": "Server error"}
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
        print(f"user: {user}")
        app.logger.info(e)
        print(f"app.logger.info: {e}")
        msg = {"message": "Server error"}
        return jsonify(msg), 500

@blueprint.route("/<post_id>", methods=["PUT"])
@inject
@auth_required()
def update_post(
    user: User, 
    post_id: int,
    post_service: PostService = Provide[Container.post_service] 
):
    try:
        post_data = request.get_json()
        post: IPost = post_service.get_post_by_id(post_id)

        if not post:
            msg = {"message": "Post not found"}
            return jsonify(msg), 404
        
        if user.id != post.user_id:
            msg = {"message": "Unauthorized"}
            return jsonify(msg), 401

        post: IPost = post_service.update_post(post_id, post_data)
    
        return jsonify(post.json()), 200

    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Server error"}), 500

@blueprint.route("/<post_id>", methods=["DELETE"])
@inject
@auth_required()
def delete_post(
    user: User, 
    post_id: int,
    post_service: PostService = Provide[Container.post_service]
    ):

    try:
        post: IPost = post_service.get_post_by_id(post_id)

        if not post:
            msg = {"message": "Post not found"}
            return jsonify(msg), 404
        
        if user.id != post.user_id:
            msg = {"message": "Unauthorized"}
            return jsonify(msg), 401
        
        deleted = post_service.delete_post(post_id)

        return jsonify({"deleted": deleted})

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

@blueprint.route("/search/<string:tag>", methods=["GET"])
@inject
def get_posts_by_tag(
    tag: str,
    post_service: PostService = Provide[Container.post_service]
):
    try:
        posts_list = post_service.get_posts_by_tag(tag)

        return jsonify(posts_list)

    except Exception as e:
        app.logger.info(e)
        msg = {"message": "Server error"}
        return jsonify(msg), 500

