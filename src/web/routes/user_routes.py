import datetime
from flask import request, json, Response, Blueprint, jsonify
from dependency_injector.wiring import inject, Provide
from flask_bcrypt import generate_password_hash


from app import app
from src.interfaces.models.user import IUser
from src.services.user_service import UserService
from src.services.post_service import PostService
from src.common.containers import Container
from src.web.middleware.auth_middleware import auth_required
from src.common.exceptions.request_data_exception import RequestDataException


blueprint = Blueprint('users', __name__)

#Register user

@blueprint.route('/', methods=['POST'])
@inject
def create(
    user_service: UserService = Provide[Container.user_service]
):
    try:
        user_data = request.get_json()
        user: IUser = user_service.create_user(user_data)

        return jsonify(user.json()), 201
    except RequestDataException as e:
        app.logger.info(e)
        msg = {"message": str(e)}
        return jsonify(msg), 400
    except Exception as e:
        app.logger.info(e)
        app.logger.info(user_data)

        return jsonify({"message": "Server error"}), 500   

@blueprint.route('/<user_id>/posts', methods=['GET'])
@inject
def get_user_posts(
    user_id: int,
    user_service: UserService = Provide[Container.user_service],
    post_service: PostService = Provide[Container.post_service]
):
    try:
        user: IUser = user_service.find_by_id(user_id)

        if not user:
            return jsonify({"message": "user not found"}), 404

        posts = post_service.get_user_posts_json(user.id)
        return jsonify(posts), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500


@blueprint.route('/profile', methods=['GET'])
@inject
@auth_required()
def get_user_profile(
    user: IUser,
    user_service: UserService = Provide[Container.user_service]
):
    try:
        user = user_service.find_by_id(user.id)

        if not user:
            return jsonify({"message": "user not found"}), 404

        return jsonify(user.json())
    except Exception as e:
        app.logger.info(e)
        
        return jsonify({"message": "Server error"}), 500


@blueprint.route('/profile', methods=['PUT'])
@inject
@auth_required()
def update_user(
    user: IUser,
    user_service: UserService = Provide[Container.user_service]
):

    try:

        user_data = request.get_json()
        #user not found
        if "roles" in user_data:
            return jsonify({"message": "Unauthorized"}), 401

        updated_user: IUser = user_service.update_user(user.id, user_data)

        return jsonify(updated_user.json()), 200
    except RequestDataException as e:
        app.logger.info(e)
        msg = {"message": str(e)}
        return jsonify(msg), 400
    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Server error"}), 500
    

@blueprint.route('/profile', methods=['DELETE'])
@inject
@auth_required()
def delete_user(
    user: IUser,
    user_service: UserService = Provide[Container.user_service]
):

    try:
        deleted: bool = user_service.delete_user(user=user)
        
        if not deleted:
            return jsonify({"message": "Server error", "deleted": False}), 500

        return jsonify({"deleted": True})
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500
""""
#Get users

@user_api.route('/', methods=['GET'])
@auth_required()
def get_all_users(user: User):
    
    try:
        users = User.get_all_users()
        users_list = []

        for user in users:
            users_list.append(user)
        
        return jsonify(users), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500
"""
""""
@user_api.route('/<user_id>', methods=['GET'])
@auth_required()
def get_user_by_id(user: User, user_id: str):
    
    try:
        user = User.get_user_by_id(user_id)
        
        if not user:
            return jsonify({"message": "user not found"})
        
        return jsonify(user.json()), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

@user_api.route('/me', methods=['GET'])
@auth_required()
def get_user_details(user: User):

    auth_header = "Authorization"

    if auth_header not in request.headers:
        return jsonify({"message": "Token missing"}), 401

    token = request.headers[auth_header]

    try:
        user = Auth.get_user_by_token(token)

        if not user:
            return jsonify("Token invalid")

        return jsonify(user.json())
    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Unauthorized"}), 401

@user_api.route("/me", methods=["PUT"])
@auth_required()
def update_user(user: User):

    auth_header = "Authorization"

    if auth_header not in request.headers:
        return jsonify({"message": "Token missing"}), 401

    token = request.headers[auth_header]

    try:
        user = Auth.get_user_by_token(token)

        if not user:
            return jsonify("Token invalid")

        user_data = request.get_json()

        updated_user = User.update(user.id, user_data)
        

        return jsonify(updated_user.json())

    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Server error"}), 401

"""